# slpc_vectordb_builder.py

import json
import os

from dotenv import load_dotenv
from langchain_community.docstore.document import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def load_slpc_data(file_path: str) -> list[dict]:
    """
    Load SLPC data from a JSON file.

    Args:
        file_path (str): Path to the SLPC JSON file.

    Returns:
        list[dict]: List of SLPC sections as dictionaries.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def prepare_documents(slpc_data: list[dict]) -> list[Document]:
    """
    Convert SLPC JSON entries to LangChain Document objects.

    Args:
        slpc_data (list[dict]): SLPC data loaded from JSON.

    Returns:
        list[Document]: LangChain-compatible documents.
    """
    return [
        Document(
            page_content=f"Section {entry['Section']}: {entry['section_title']}\n\n{entry['section_desc']}",
            metadata={
                "chapter": entry["chapter"],
                "chapter_title": entry["chapter_title"],
                "section": entry["Section"],
                "section_title": entry["section_title"]
            }
        )
        for entry in slpc_data
    ]


def build_slpc_vectordb():
    """
    Build and persist a Chroma vectorstore for SLPC sections.
    """
    # Load environment variables
    load_dotenv()
    slpc_json_path = os.getenv("SLPC_JSON_PATH")
    persist_dir_path = os.getenv("PERSIST_DIRECTORY_PATH")
    collection_name = os.getenv("SLPC_COLLECTION_NAME")

    if not all([slpc_json_path, persist_dir_path, collection_name]):
        raise EnvironmentError("❌ Missing one or more required environment variables.")

    # Load and process data
    slpc_data = load_slpc_data(slpc_json_path)
    documents = prepare_documents(slpc_data)

    # Initialize embeddings and vectorstore
    embeddings = HuggingFaceEmbeddings()
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir_path,
        collection_name=collection_name
    )

    print(f"✅ Vectorstore successfully created in collection '{collection_name}' at '{persist_dir_path}'")


if __name__ == "__main__":
    build_slpc_vectordb()
