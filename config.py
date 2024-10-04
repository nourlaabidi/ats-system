import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import openai

load_dotenv()

connect_str = os.getenv("AZURE_BLOB_STORAGE_CONNECTION_STRING")
container_name = os.getenv("CONTAINER_NAME")
openai.api_type = "azure"
openai.api_base = os.getenv("OPEN_API_BASE")
openai.api_version = "2024-05-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

azure_credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(azure_credential, "https://cognitiveservices.azure.com/.default")

index_name = os.getenv("INDEX_NAME")
search_endpoint = os.getenv("COGNITIVE_SEARCH_ENDPOINT")
search_api_key = os.getenv("COGNITIVE_SEARCH_API_KEY")
semantic_config = os.getenv("SEMANTIC_CONFIG_NAME")
