import argparse
from rag_ollama import RAGPipeline
import sys
from typing import Optional

def print_colored(text: str, color: str = "green") -> None:
    """Print colored text to terminal."""
    colors = {
        "green": "\033[92m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "end": "\033[0m"
    }
    print(f"{colors.get(color, colors['green'])}{text}{colors['end']}")

def interactive_mode(rag: RAGPipeline) -> None:
    """Run the RAG system in interactive mode."""
    print_colored("\n=== RAG System Interactive Mode ===", "blue")
    print_colored("Type 'exit' or 'quit' to end the session", "yellow")
    print_colored("Type 'help' for available commands", "yellow")
    print_colored("Type your question to get started!\n", "green")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYour question: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit']:
                print_colored("\nThank you for using the RAG system. Goodbye!", "blue")
                break
            
            # Check for help command
            if user_input.lower() == 'help':
                print_help()
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Get response from RAG system
            print_colored("\nSearching for relevant information...", "yellow")
            response = rag.query(user_input)
            
            # Print response
            print_colored("\nResponse:", "blue")
            print(response)
            
        except KeyboardInterrupt:
            print_colored("\n\nExiting...", "red")
            break
        except Exception as e:
            print_colored(f"\nError: {str(e)}", "red")

def print_help() -> None:
    """Print help information."""
    print_colored("\nAvailable Commands:", "blue")
    print_colored("  help    - Show this help message", "green")
    print_colored("  exit    - Exit the program", "green")
    print_colored("  quit    - Exit the program", "green")
    print_colored("\nExample Questions:", "blue")
    print_colored("  - What are the key policies regarding academic affairs?", "green")
    print_colored("  - Explain the policy on academic misconduct", "green")
    print_colored("  - What are the requirements for undergraduate admission?", "green")

def main():
    """Main function to run the CLI."""
    parser = argparse.ArgumentParser(description="RAG System Command Line Interface")
    parser.add_argument(
        "--model",
        type=str,
        default="llama2",
        help="Ollama model to use (default: llama2)"
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
        "--force-recreate",
        action="store_true",
        help="Force recreate the collection if it exists"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize RAG pipeline
        print_colored("Initializing RAG system...", "yellow")
        rag = RAGPipeline(
            chroma_db_path=args.db_path,
            collection_name=args.collection,
            model_name=args.model,
            force_recreate=args.force_recreate
        )
        
        # Start interactive mode
        interactive_mode(rag)
        
    except Exception as e:
        print_colored(f"Error initializing RAG system: {str(e)}", "red")
        sys.exit(1)

if __name__ == "__main__":
    main() 