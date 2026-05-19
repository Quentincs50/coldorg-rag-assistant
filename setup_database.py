import argparse
import shutil
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from helper import get_embedding
from langchain_chroma import Chroma
import os


CHROMA_PATH = "chroma"
DOCS_PATH = "data/docs"
JSON_PATH="data"
JSON_FILE_NAME="interventions.json"

""" def main():

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("Clearing Database")
        clear_database()

    
    docs = load_txt_docs()
    interventions = load_interventions()
    all_docs = docs + interventions
    chunks = split_documents(all_docs)
    add_to_chroma(chunks) """
    

def load_txt_docs():
    # Format text file to Document 
    docs = []
    for file in os.listdir(DOCS_PATH):
        file_path = os.path.join(DOCS_PATH, file)  
        with open(file_path, "r") as doc:
            content = doc.read()
            docs.append(Document(
                page_content=content,
                metadata={"source": file_path}))
    return docs

def load_interventions():
    loader = JSONLoader(
    file_path=f"{JSON_PATH}/{JSON_FILE_NAME}",
    jq_schema=".[]",
    text_content=False,
    )
    docs = loader.load()
    return docs

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

    
def calculate_chunk_ids(chunks):
    # This will format chunks metadata like {"source": "data/docs/fiche.txt", "id": "data/docs/fiche.txt:6:2"}.
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("seq_num", 0)
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default.
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("No new documents to add")

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

""" if __name__ == "__main__":
    main() """
