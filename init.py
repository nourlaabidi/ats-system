from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    HnswParameters,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchAlgorithmKind,
    VectorSearchProfile,
    SemanticField,
    SemanticConfiguration,
    SemanticSearch,
    SemanticPrioritizedFields,
)
from config import index_name, search_api_key, search_endpoint, semantic_config
#init.py is the first thing to run when you create this project, it wil create the index in azure cognitive search and the semantic configuration 

search_index_client = SearchIndexClient(endpoint=search_endpoint, credential=AzureKeyCredential(search_api_key))

#create the index
index = SearchIndex(
    name=index_name,
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="name", type=SearchFieldDataType.String),
        SimpleField(name="file_path", type=SearchFieldDataType.String),
        SearchField(name="skills",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                    searchable=True),
        SearchField(name="skillsEmb",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True, vector_search_dimensions=1536, vector_search_profile_name="skillsEmb_profile"),
        SearchField(name="technologies",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                    searchable=True),
        SearchField(name="technologiesEmb",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True, vector_search_dimensions=1536, vector_search_profile_name="technologiesEmb_profile"),
        SearchField(name="language",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                    searchable=True),
        SearchField(name="WorkExperiences",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                    searchable=True),
        SearchField(name="WorkExperiencesEmb",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True, vector_search_dimensions=1536, vector_search_profile_name="WorkExperiencesEmb_profile"),
    ],
    vector_search=VectorSearch(
        algorithms=[HnswAlgorithmConfiguration( # Hierachical Navigable Small World, IVF
                            name="hnsw_config",
                            kind=VectorSearchAlgorithmKind.HNSW,
                            parameters=HnswParameters(metric="cosine"),
                        )],
        profiles=[
            VectorSearchProfile(name="skillsEmb_profile", algorithm_configuration_name="hnsw_config"),
            VectorSearchProfile(name="technologiesEmb_profile", algorithm_configuration_name="hnsw_config"),
            VectorSearchProfile(name="WorkExperiencesEmb_profile", algorithm_configuration_name="hnsw_config")
        ]
    ),
    
)
semantic_config = SemanticConfiguration(
        name=semantic_config,
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="name"),
            keywords_fields=[
                SemanticField(field_name="skills"),
                SemanticField(field_name="technologies"),
                SemanticField(field_name="WorkExperiences"),
                SemanticField(field_name="language"),
            ],
            content_fields=[
                SemanticField(field_name="skills"),
                SemanticField(field_name="technologies"),
                SemanticField(field_name="WorkExperiences"),
                SemanticField(field_name="language"),
            ]
            
        )
    )
index.semantic_search = SemanticSearch(configurations=[semantic_config])
index_client = SearchIndexClient(endpoint=search_endpoint, credential=AzureKeyCredential(search_api_key))
index_client.create_or_update_index(index)
