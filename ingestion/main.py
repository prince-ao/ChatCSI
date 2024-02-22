import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()


class CSIIngestor:

    MODEL_CHUNK_SIZE = 819
    sitemap_url = "https://www.csi.cuny.edu/"

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

    def insert_embedding(self, embedding, text, path):
        row = {}

    def add_html_to_vectordb(self, content, path):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.MODEL_CHUNK_SIZE,
            chunk_overlap=self.MODEL_CHUNK_SIZE // 10
        )

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        docs = text_splitter.create_documents([content])

        for doc in docs:
            query_result = embeddings.embed_query(doc)

    def index_website(self):
        links = self.get_html_sitemap(self.sitemap_url)

        for link in links:
            print(f'indexing {link}...')
            try:
                content = self.get_html_body_content(link)
                self.add_html_to_vectordb(content, link)
            except Exception:
                print(f'unable to process {link}')
