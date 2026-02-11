# FIRST RAG AI Project

This project is a custom-built Retrieval-Augmented Generation (RAG) system designed to answer user questions about Kubernetes based on a specific, private text document (k8s.txt). It uses ChromaDB as the vector database for memory, Google's Gemini API as the "Brain" for text generation, and FastAPI to serve everything as a modern web API.

# What is RAG?

>RAG (Retrieval-Augmented Generation) is an AI architecture that connects a Large Language Model (LLM) to a private database of facts.

>Instead of relying on the AI's general training data (which might be outdated or hallucinated), RAG forces the AI to read specific, retrieved documents before answering. Think of it like a two-step "Open Book" test:

Phase 1: 
    Ingestion (Stocking the Library) We take a large text document (k8s.txt), chop it into smaller "chunks," and translate those chunks into mathematical vectors (embeddings). We store these vectors in a local database (ChromaDB). This usually runs just once.

Phase 2: 
    Retrieval & Generation (Answering the User) When a user asks a question, we translate their English question into math, search the database for the closest matching text chunks (Retrieval), and then send the question plus the retrieved chunks to the AI (Generation) with strict instructions to only use the provided facts.


# Prerequisites

> Python 3.12+ installed on your system.

> A Google Gemini API Key (from Google AI Studio).


    
# Installation & Setup

1. Clone or Create the Project Folder Ensure you have all your files in one central directory, including your source knowledge file named k8s.txt.

2. Create & Activate a Virtual Environment Keep your project dependencies isolated from your main system

    > Create the environment (if you haven't already)
    
        python3 -m venv .venv


    > Activate the environment
    
        source .venv/bin/activate

3. Install Dependencies Install the necessary libraries for vector search, the LLM, and the web server

    pip install chromadb langchain-text-splitters google-generativeai python-dotenv fastapi uvicorn

4. Configure Environment Variables Create a .env file in the root of your project directory and add your Google API key

    GEMINI_API_KEY=your_actual_api_key_here



# How to Run the Project

Running the application happens in two distinct steps.

Step 1: Ingest the Data
We need to populate our vector database before we can search it. Run the ingestion script once:

    python3 chroma.py

Note: We use Google's models/gemini-embedding-001 to create these mathematical embeddings. If you ever change the embedding model, you must delete your chroma_db folder and run this script again to prevent database corruption.

Step 2: Start the FastAPI Server
With the database populated, start the backend API server:

    uvicorn main:app --reload



# Testing the API

FastAPI automatically generates an interactive testing dashboard for us.

    Open your web browser and navigate to: http://127.0.0.1:8000/docs

    Expand the green GET /query endpoint.

    Click "Try it out".

    In the request field, type a question related to your k8s.txt file (e.g., "What is a pod?").

    Click Execute.

    Scroll down to see the AI's response in the "Server response" body!



# Project File Structure

1. chroma.py (The Ingestion Script)
This script reads k8s.txt, splits the text, and stores it in the vector database.

2. main.py (The FastAPI Backend)
This script runs the live server, catches user requests, searches ChromaDB, and generates an answer using Google's gemini-2.5-flash model.