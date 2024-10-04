from azure.search.documents.models import VectorizedQuery
from azure.search.documents import SearchClient
from typing import Dict, List
from fastapi import HTTPException
from config import index_name, search_api_key, search_endpoint, semantic_config
from config import  semantic_config
from textProcessing import get_embedding
from azure.core.credentials import AzureKeyCredential
#search.py includes the function of the search in the index, it gets the query(the job description) as an input and return the resumes that matches
#that job description, the search is done using two different ways (hybrid) we used the vector search wich means searching in embedeedings and we used 
#the semantic search wich is based on the search depending onkey words and content.
search_client = SearchClientsearch_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=AzureKeyCredential(search_api_key))
def search_resumes(query: str) -> List[Dict]:
    search_vector = get_embedding(query)
    fields_to_search = ["skillsEmb", "technologiesEmb", "WorkExperiencesEmb"]
    
    try:
        results = search_client.search(
            search_text=query,
            top=20,
            vector_queries=[
                VectorizedQuery(vector=search_vector, k_nearest_neighbors=20, fields=",".join(fields_to_search))
            ],
            query_type="semantic",
            semantic_configuration_name=semantic_config
        )
        return [doc for doc in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))