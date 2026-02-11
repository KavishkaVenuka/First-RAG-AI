import os
import chromadb
import google.generativeai as genai
from fastapi import FastAPI
from dotenv import load_dotenv
import chromadb.utils.embedding_functions as embedding_functions


#load the .env file and get the GEMINI_API_KEY
load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")

#get the database path
db_path = os.path.join(os.getcwd() , "chroma_db")

#configure the Gemini brain
genai.configure(api_key=gemini_api)
llm = genai.GenerativeModel('gemini-2.5-flash')

#defininig the embedding function for embedding ther questions into mathematical embeddings...
google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=gemini_api,
    model_name="models/gemini-embedding-001"
)

#define the chromadb client
client = chromadb.PersistentClient(path=db_path)

#define the chromadb collection
collection = client.get_collection(name="k8s_knowledge", embedding_function=google_ef)

#define the answer generating function
def genAnswer(request:str):
    answer = collection.query(query_texts=[request], n_results=3)
    # Extract the chunks and join them into one big string of background context
    retrieved_chunks = "\n".join(answer['documents'][0])
    prompt = f"Act as you are Kubernetes expert. I need you to generate answer the following request questions using ONLY USING the retrieved_chunks. request : {request}. retrieved_chunks : {retrieved_chunks}"

    #generate human readable asnwer
    response = llm.generate_content(prompt)
    return response.text

app = FastAPI()

@app.get("/")
def read_root():
    return {"message":"The RAG AI backend is running!"}

@app.get("/query")
def query(request):
    try:
        answer = genAnswer(request)
        return answer
    except Exception as e:
        return f"An error occured. {e}"