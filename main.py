from typing import Dict, List
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from fastapi import FastAPI, HTTPException
from azure.storage.blob import BlobServiceClient
from config import connect_str, container_name, index_name, search_api_key, search_endpoint
from search import search_resumes
from blobStorage import download_blob, get_existing_resumes
from extractInfos import process_and_index_resume
#main.py implements the endpoints of the app
app = FastAPI()

@app.get('/')
async def root() -> Dict[str, str]:
    """
    Root endpoint.
    """
    return {'Greeting': 'Hello word!'}
#/uploadResumes will upload the resumes from blob storage account and extract the necessary informations of the resumes and store it in the index created
@app.get('/uploadResumes')
async def upload_resumes() -> None:
    """
    Upload resumes endpoint.
    """
   
    download_folder = "/resumes"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=AzureKeyCredential(search_api_key))

    download_blob(blob_service_client, download_folder, container_name)
    existed_resumes = get_existing_resumes(search_client)

    for file_name in os.listdir(download_folder):
        file_path = os.path.join(download_folder, file_name)
        process_and_index_resume(file_path, search_client, existed_resumes)
#/resumes will give the resumes that matches the given job description
@app.get('/resumes', response_model=List[Dict[str, str]])
async def show_result(query: str):
    try:
        search_results = search_resumes(query)
        filtered_list = []
        for doc in search_results:
            filtered_list.append({
                "name": doc.get("name", "").replace("\n", " ")[:150],
                "file_path": doc.get("file_path", "").replace("\n", " ")[:150],
                "score": f"{doc.get('@search.score', 0.0):.5f}",
                "reranker_score": f"{doc.get('@search.reranker_score', 0.0):.5f}"
            })
        return filtered_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#run uvicorn main:app --reload