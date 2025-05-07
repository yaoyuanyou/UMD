import os
import PyPDF2
import logging
from typing import Dict, List
from rag_ollama import RAGPipeline

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag = rag_pipeline
        
    def read_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return ""
        
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                logger.info(f"Reading {pdf_path} with {num_pages} pages")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    
                    # Log progress for large PDFs
                    if num_pages > 20 and (page_num + 1) % 10 == 0:
                        logger.info(f"Progress: {page_num + 1}/{num_pages} pages processed")
            
            # Clean the text
            text = self._clean_text(text)
            logger.info(f"Successfully extracted {len(text)} characters from {pdf_path}")
            return text
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {str(e)}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean the extracted text."""
        # Remove excessive whitespace
        text = text.replace('\n', ' ').strip()
        text = ' '.join(text.split())
        return text
    
    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """Split text into chunks with overlap."""
        if not text:
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            
            # If we're not at the end of the text, try to break at a logical point
            if end < len(text):
                # Look for good breakpoints: paragraph, sentence, or word
                paragraph_break = text.rfind('\n', start, end)
                sentence_break = text.rfind('. ', start, end)
                space_break = text.rfind(' ', start, end)
                
                if paragraph_break != -1 and paragraph_break > start + chunk_size // 2:
                    end = paragraph_break + 1
                elif sentence_break != -1 and sentence_break > start + chunk_size // 2:
                    end = sentence_break + 2
                elif space_break != -1:
                    end = space_break + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move the start position, accounting for overlap
            start = end - chunk_overlap if end - chunk_overlap > start else end
        
        return chunks
    
    def process_pdf(self, pdf_path: str) -> int:
        """Process a single PDF file and add it to ChromaDB."""
        # Extract filename from path
        filename = os.path.basename(pdf_path)
        
        # Read PDF
        text = self.read_pdf(pdf_path)
        if not text:
            logger.warning(f"No text extracted from {pdf_path}")
            return 0
        
        # Chunk the text
        chunks = self.chunk_text(text)
        if not chunks:
            logger.warning(f"No chunks created from {pdf_path}")
            return 0
        
        # Add chunks to ChromaDB
        try:
            # Create metadata for each chunk
            metadatas = [{
                "filename": filename,
                "source_path": pdf_path,
                "chunk_id": i
            } for i in range(len(chunks))]
            
            # Create unique IDs for each chunk
            ids = [f"{filename}_{i}" for i in range(len(chunks))]
            
            # Add to ChromaDB
            self.rag.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully added {len(chunks)} chunks from {filename} to ChromaDB")
            return len(chunks)
            
        except Exception as e:
            logger.error(f"Error adding chunks to ChromaDB: {str(e)}")
            return 0
    
    def process_directory(self, directory_path: str) -> Dict[str, int]:
        """Process all PDFs in a directory."""
        if not os.path.isdir(directory_path):
            logger.error(f"Directory not found: {directory_path}")
            return {}
        
        results = {}
        pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {directory_path}")
            return {}
        
        logger.info(f"Found {len(pdf_files)} PDF files in {directory_path}")
        
        for i, pdf_file in enumerate(pdf_files):
            pdf_path = os.path.join(directory_path, pdf_file)
            logger.info(f"Processing PDF {i+1}/{len(pdf_files)}: {pdf_file}")
            
            chunks_added = self.process_pdf(pdf_path)
            results[pdf_file] = chunks_added
        
        return results

def main():
    """Main function to process PDFs."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process PDFs and store in ChromaDB")
    parser.add_argument(
        "--pdf-dir",
        type=str,
        required=True,
        help="Directory containing PDF files"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="./chroma_db",
        help="Path to ChromaDB directory (default: ./chroma_db)"
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="pdf_embeddings",
        help="ChromaDB collection name (default: pdf_embeddings)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="llama2",
        help="Ollama model to use (default: llama2)"
    )
    parser.add_argument(
        "--force-recreate",
        action="store_true",
        help="Force recreate the collection if it exists"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize RAG pipeline
        print("Initializing RAG system...")
        rag = RAGPipeline(
            chroma_db_path=args.db_path,
            collection_name=args.collection,
            model_name=args.model,
            force_recreate=args.force_recreate
        )
        
        # Initialize PDF processor
        processor = PDFProcessor(rag)
        
        # Process PDFs
        print(f"Processing PDFs in {args.pdf_dir}...")
        results = processor.process_directory(args.pdf_dir)
        
        # Print results
        print("\nProcessing Results:")
        total_chunks = 0
        for filename, chunks in results.items():
            print(f"{filename}: {chunks} chunks")
            total_chunks += chunks
        print(f"\nTotal chunks processed: {total_chunks}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 