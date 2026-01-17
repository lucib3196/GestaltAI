import os
from langchain_openai import OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from .document_loader import TopicDocumentLoader

if __name__ == "__main__":
    print("Adding topics to vectorstore")
    embeddings = OpenAIEmbeddings(
        model=os.getenv("EMBEDDINGS", ""),
    )

    vector_store = AstraDBVectorStore(
        collection_name="topic_data",
        embedding=embeddings,
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT", None),
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN", None),
        namespace=os.getenv("ASTRA_DB_KEYSPACE", None),
    )

    documents = TopicDocumentLoader().load()
    vector_store.add_documents(documents)
