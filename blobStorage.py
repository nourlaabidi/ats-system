import os
# function to upload the resumes from blob storage account 
def download_blob(blob_service_client, download_folder, container_name):
    container_client = blob_service_client.get_container_client(container_name)
    blobs_list = container_client.list_blobs()
    for blob in blobs_list:
        download_file_path = os.path.join(download_folder, blob.name)
        if not os.path.exists(download_file_path):
            blob_client = container_client.get_blob_client(blob)
            with open(download_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            print(f"Blob {blob.name} downloaded successfully to {download_file_path}")
        else:
            print(f"Blob {blob.name} already exists in the download folder. Skipping download.")

#function to check existing resumes in the search index so we will not be having redundant resumes in the index
def get_existing_resumes(search_client):
    existing_resumes = []
    if search_client.get_document_count() > 0:
        existing_documents = search_client.search(search_text="*", select="file_path")
        existing_resumes = [document["file_path"] for document in existing_documents]
    return existing_resumes


                