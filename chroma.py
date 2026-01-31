import chromadb
import os
from dotenv import load_dotenv
import chromadb.utils.embedding_functions as embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

#load the .env file and get the API key 
load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")

#initialize a file for store database embeddings
db_path = os.path.join(os.getcwd(), "chroma_db")
print(f"DB is configured at {db_path}") 

#create teh Google Embedding Function
google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=gemini_api,
    model_name="models/text-embedding-004")


#initialize the ChromaDB client
client = chromadb.PersistentClient(path=db_path)

#initialize the chromaDB collection
collection = client.get_or_create_collection(name="k8s_knowledge", embedding_function=google_ef)

# Initialize the splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

try:
    with open("k8s.txt", "r") as f:
        text = f.read()

    chunks = text_splitter.split_text(text)
    ids = [f"k8s_{i}" for i in range(len(chunks))]

    collection.add(documents=chunks, ids=ids)

    print("Embedding stored in Chroma!")

except Exception as e:
    print(f"An error occurred: {e}")