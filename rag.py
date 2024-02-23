from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Milvus

# TODO: Convert the embeddings to to spacy
# TODO: Use an open source model


load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

milvus_client = Milvus(embedding_function=embeddings,
                       collection_name='chatcsi_demo_1',
                       collection_description="chatcsi demo collection",
                       auto_id=True,
                       connection_args={
                           "address": "localhost:19530",
                       }
                       )

retriever = milvus_client.as_retriever(
    search_type="mmr",
    search_kwargs={
        'k': 8,
        'fetch_k': 30
    }
)
