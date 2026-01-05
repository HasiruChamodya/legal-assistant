# slpc_sections_search_tool.py

import os

from dotenv import load_dotenv
from crewai.tools import tool
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# Default number of results to return from similarity search
DEFAULT_TOP_K = 3


@tool("SLPC Sections Search Tool")
def search_slpc_sections(query: str) -> list[dict]:
    """
    Search SLPC vector database for sections relevant to the input query.

    Args:
        query (str): User query in natural language.

    Returns:
        list[dict]: List of matching SLPC sections with metadata and content.
    """
    # Load environment variables
    load_dotenv()

    # Resolve vector DB path
    persist_dir_path = os.getenv("PERSIST_DIRECTORY_PATH")
    if not persist_dir_path:
        raise EnvironmentError("❌ 'PERSIST_DIRECTORY_PATH' is not set in .env")

    collection_name = os.getenv("SLPC_COLLECTION_NAME")

    embedding_function = HuggingFaceEmbeddings()

    # Load vectorstore
    vector_db = Chroma(
        collection_name=collection_name,
        persist_directory=persist_dir_path,
        embedding_function=embedding_function
    )

    # Perform similarity search
    docs = vector_db.similarity_search(query, k=DEFAULT_TOP_K)

    # Format results
    return [
        {
            "section": doc.metadata.get("section"),
            "section_title": doc.metadata.get("section_title"),
            "chapter": doc.metadata.get("chapter"),
            "chapter_title": doc.metadata.get("chapter_title"),
            "content": doc.page_content
        }
        for doc in docs
    ]


# Example usage of the SLPC Section Search Tool - uncomment for testing the tool functionality
# query = "What is the SLPC section for Theft?"
# results = search_slpc_sections.func(query)
# for r in results:
#     print(r)

# NOTE: Retrieval is a bit slower. Can be improved by caching the vectordb and using GPU for embedding.
