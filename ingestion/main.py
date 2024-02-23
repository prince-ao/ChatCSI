import requests
import re
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag import milvus_client


class CSIIngestor:

    MODEL_CHUNK_SIZE = 819

    csi_sitemap_urls = ["https://www.csi.cuny.edu/sitemap.xml",
                        "https://library.csi.cuny.edu/sitemap.xml"]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=MODEL_CHUNK_SIZE,
        chunk_overlap=MODEL_CHUNK_SIZE // 10
    )

    def __init__(self, milvus_client):
        self.milvus_client = milvus_client

    def get_html_sitemap(self, url):
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "xml")

        links = []

        locations = soup.find_all("loc")

        for location in locations:
            url = location.get_text()
            links.append(url)

        return links

    def get_html_body_content(self, url):
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        body = soup.body
        inner_text = body.get_text()
        return inner_text

    def clean_string(self, input_string):
        cleaned_string = re.sub(r'[\n\t]+', ' ', input_string)
        cleaned_string = re.sub(r'\s+', ' ', cleaned_string)
        return cleaned_string

    def insert_embedding(self, text, path):
        self.milvus_client.add_texts(
            texts=[text.page_content], metadatas=[{"path": path}]
        )

    def add_html_to_vectordb(self, content, path):

        docs = self.text_splitter.create_documents([content])

        for doc in docs:
            self.insert_embedding(doc, path)

    def index_website(self, sitemap_url):
        links = self.get_html_sitemap(sitemap_url)

        for link in links:
            print(f'- indexing {link}...')
            try:
                content = self.get_html_body_content(link)
                content = self.clean_string(content)
                self.add_html_to_vectordb(content, link)
            except Exception as e:
                print(f'- - unable to process {link}')
                print(e)

    def index_websites(self):

        for url in self.csi_sitemap_urls:
            print(f"Starting url: {url}")
            self.index_website(url)


if __name__ == '__main__':
    csi_ingestor = CSIIngestor(milvus_client)
    csi_ingestor.index_websites()
