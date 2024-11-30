import os
from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache
from lightrag.utils import EmbeddingFunc
from dotenv import load_dotenv
import asyncio
from langfuse.decorators import observe
import aiohttp
import numpy as np
import streamlit as st

# Load environment variables from .env file if it exists (local development)
load_dotenv()

# Get environment variables with fallback to Streamlit secrets
def get_env_var(var_name: str) -> str:
    """Get environment variable with fallback to Streamlit secrets."""
    # Try getting from environment first (local development)
    value = os.getenv(var_name)
    if value is None:
        # Fallback to Streamlit secrets (cloud deployment)
        try:
            value = st.secrets[var_name]
        except:
            raise ValueError(f"Missing required environment variable: {var_name}")
    return value

WORKING_DIR = "./bible"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

async def jina_embedding(texts, embed_model="jina-embeddings-v2-base-en"):
    """
    Get embeddings from Jina AI API for the given texts.

    Args:
        texts (Union[str, List[str]]): Text or list of texts to get embeddings for
        embed_model (str): Model name to use for embeddings

    Returns:
        List[List[float]]: List of embeddings, one for each input text
    """
    # Convert single text to list
    if isinstance(texts, str):
        texts = [texts]

    # Prepare the request
    url = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_env_var('JINA_API_KEY')}"
    }
    data = {
        "model": embed_model,
        "normalized": True,
        "embedding_type": "float",
        "input": texts
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response.raise_for_status()  # Raise exception for error status codes
            result = await response.json()

    # Extract embeddings from response
    embeddings = [item["embedding"] for item in result["data"]]

    return embeddings

async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:
    return await openai_complete_if_cache(
        base_url="https://api.naga.ac/v1",
        model="gpt-4o-mini",
        prompt=prompt,
        api_key=get_env_var('NAGA_API_KEY'),
        system_prompt=system_prompt,
        history_messages=history_messages,
        **kwargs,
    )

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=llm_model_func,
    # Use Jina embedding function
    embedding_func=EmbeddingFunc(
        embedding_dim=768,  # Jina embeddings v2 base has 768 dimensions
        max_token_size=8192,  # Jina supports up to 8192 tokens
        func=jina_embedding
    ),
)
