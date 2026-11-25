import warnings

from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load document
loader = TextLoader("data/raw/deskthority/alps_skcl_green.md", encoding="utf-8")
docs = loader.load()

# Split document
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
header_chunks = markdown_splitter.split_text(docs[0].page_content)
# Each chunk's metadata includes the headers that contain it.

size_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
chunks = size_splitter.split_documents(header_chunks)

# Embeddings
model = OllamaEmbeddings(model="qwen3-embedding:0.6b", dimensions=1024)
embeddings = model.embed_documents(
    [chunk.page_content for chunk in chunks]
)

print(len(embeddings))
print(len(chunks))
