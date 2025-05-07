import os
import requests
import json
from typing import List, Dict, Any
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OllamaRAG:
    def __init__(
        self,
        model_name: str = "llama2",
        api_base: str = "http://localhost:11434",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        Initialize the RAG system with Ollama.
        
        Args:
            model_name: Name of the Ollama model to use
            api_base: Base URL for Ollama API
            temperature: Temperature for generation (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
        """
        self.model_name = model_name
        self.api_base = api_base
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text using Ollama."""
        try:
            response = requests.post(
                f"{self.api_base}/api/embeddings",
                json={"model": self.model_name, "prompt": text}
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            logger.error(f"Error getting embedding from Ollama: {str(e)}")
            return [0.0] * 4096  # Fallback to zero vector
    
    def generate_response(
        self,
        query: str,
        context: List[str],
        system_prompt: str = None
    ) -> str:
        """
        Generate a response using Ollama with RAG.
        
        Args:
            query: User's question
            context: List of relevant context chunks
            system_prompt: Optional system prompt to guide the model
            
        Returns:
            Generated response
        """
        # Construct the prompt with context
        context_text = "\n\n".join(context)
        
        if system_prompt is None:
            system_prompt = """You are a helpful AI assistant. Use the provided context to answer the user's question. 
            If the context doesn't contain enough information to answer the question, say so. 
            Always be truthful and don't make up information."""
        
        prompt = f"""Context information is below.
---------------------
{context_text}
---------------------
Given the context information, please answer the following question:
{query}

Answer:"""
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "system": system_prompt,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {str(e)}")
            return "I apologize, but I encountered an error while generating the response."

class RAGPipeline:
    def __init__(
        self,
        chroma_db_path: str = "./chroma_db",
        collection_name: str = "pdf_embeddings",
        model_name: str = "llama2",
        force_recreate: bool = False
    ):
        """
        Initialize the complete RAG pipeline.
        
        Args:
            chroma_db_path: Path to ChromaDB directory
            collection_name: Name of the ChromaDB collection
            model_name: Name of the Ollama model to use
            force_recreate: If True, will delete and recreate the collection if it exists
        """
        import chromadb
        from chromadb.utils import embedding_functions
        
        # Initialize Ollama RAG
        self.ollama = OllamaRAG(model_name=model_name)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=chroma_db_path)
        
        # Create custom embedding function using Ollama
        class OllamaEmbeddingFunction:
            def __init__(self, ollama_instance):
                self.ollama = ollama_instance
            
            def __call__(self, texts: List[str]) -> List[List[float]]:
                return [self.ollama.get_embedding(text) for text in texts]
        
        # Get or create collection
        try:
            if force_recreate:
                try:
                    self.chroma_client.delete_collection(collection_name)
                    logger.info(f"Deleted existing collection: {collection_name}")
                except Exception as e:
                    logger.warning(f"Could not delete collection: {str(e)}")
            
            self.collection = self.chroma_client.get_collection(
                name=collection_name,
                embedding_function=OllamaEmbeddingFunction(self.ollama)
            )
            logger.info(f"Connected to existing collection: {collection_name}")
        except ValueError:
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                embedding_function=OllamaEmbeddingFunction(self.ollama)
            )
            logger.info(f"Created new collection: {collection_name}")
    
    def query(self, query: str, n_results: int = 5) -> str:
        """
        Query the RAG system.
        
        Args:
            query: User's question
            n_results: Number of context chunks to retrieve
            
        Returns:
            Generated response
        """
        # Get relevant context from ChromaDB
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Extract context from results
        context = results["documents"][0] if results["documents"] else []
        
        # Generate response using Ollama
        response = self.ollama.generate_response(query, context)
        
        return response

# Example usage
if __name__ == "__main__":
    # Initialize the RAG pipeline
    rag = RAGPipeline()
    
    # Example query
    query = "What are the key policies regarding academic affairs?"
    response = rag.query(query)
    print(f"Query: {query}")
    print(f"Response: {response}") 