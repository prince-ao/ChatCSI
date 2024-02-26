from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from langchain_community.vectorstores import Milvus

# TODO: Convert the embeddings to to spacy
# TODO: Use an open source model


load_dotenv()

embeddings = SpacyEmbeddings(model_name="en_core_web_sm")

milvus_client = Milvus(embedding_function=embeddings,
                       collection_name='chatcsi_demo_3',
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
