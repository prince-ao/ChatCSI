import requests
import re
import os
import math
from multiprocessing import Pool
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag import milvus_client_csi
# from rag import milvus_client_admissions


def add_link_to_vectordb(link):
    process_id = os.getpid()

    print(f'- - process {process_id} indexing website: {link}')

    try:
        content = get_html_body_content(link)
        content = clean_string(content)

        add_html_to_vectordb(content, link)
    except Exception as e:
        print(f'- - - unable to process {link} from process {process_id}:',
              e
              )


def spawn_processes():
    for url in csi_sitemap_urls:
        print(f'- indexing sitemap: {url}...')
        links = get_html_sitemap(url)

        # links = [link for link in links if "admissions" in link.lower()]

        with Pool(math.ceil(os.cpu_count() * .80)) as pool:
            pool.map(add_link_to_vectordb, links)


MODEL_CHUNK_SIZE = 819

csi_sitemap_urls = ["https://www.csi.cuny.edu/sitemap.xml",
                    "https://library.csi.cuny.edu/sitemap.xml"]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=MODEL_CHUNK_SIZE,
    chunk_overlap=MODEL_CHUNK_SIZE // 10
)


def get_html_sitemap(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "xml")

    links = []

    locations = soup.find_all("loc")

    for location in locations:
        url = location.get_text()
        links.append(url)

    return links


def get_html_body_content(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    body = soup.body
    inner_text = body.get_text()
    return inner_text


def clean_string(input_string):
    cleaned_string = re.sub(r'[\n\t]+', ' ', input_string)
    cleaned_string = re.sub(r'\s+', ' ', cleaned_string)
    return cleaned_string


def insert_embedding(text, path):
    milvus_client_csi.add_texts(
        texts=[text.page_content], metadatas=[{"path": path}]
    )


# def insert_embeddings(text, path):
    # milvus_client_admissions.add_texts(
    # texts=[text.page_content], metadatas=[{"path": path}]
    # )


def add_html_to_vectordb(content, path):

    docs = text_splitter.create_documents([content])

    for doc in docs:
        insert_embedding(doc, path)


def index_website(sitemap_url):
    links = get_html_sitemap(sitemap_url)

    for link in links:
        print(f'- indexing {link}...')
        try:
            content = get_html_body_content(link)
            content = clean_string(content)
            add_html_to_vectordb(content, link)
        except Exception as e:
            print(f'- - unable to process {link}')
            print(e)


def index_websites():

    for url in csi_sitemap_urls:
        print(f"Starting url: {url}")
        index_website(url)


if __name__ == '__main__':
    spawn_processes()
