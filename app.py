from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import uvicorn
from react_agent.graph import graph  # Import the compiled graph
from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv
import json
import pandas as pd
import io
from fastapi import UploadFile, File
from src.react_agent.state import State
from chat_graph.state import ChatState

from src.react_agent.graph import graph 
from chat_graph.graph import chat_graph

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
# app.mount("/", StaticFiles(directory="../client/build", html=True), name="site")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    dataframe: str


# Route to create a chart based on user text
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Read Excel or CSV File
    print (f'filename{ file.filename}')
    contents = await file.read()
    # Check if file is CSV or Excel
    print (f'filename{ file.filename}')
    if file.filename.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(contents))
    else:
        # Explicitly specify the engine to handle Excel file formats
        try:
            df = pd.read_excel(io.BytesIO(contents), engine='openpyxl')  # For .xlsx files
        except Exception as e:
            try:
                df = pd.read_excel(io.BytesIO(contents), engine='xlrd')  # For older .xls files
            except Exception as inner_error:
                return {"error": f"Error reading Excel file: {inner_error}"}



    # Create a config with additional message
    config = RunnableConfig(metadata={"message": "Starting data cleaning process."})

    # Run LangGraph Workflow
    result = await graph.ainvoke(State(
        original_data=df,
        messages=["Initial message: Data uploaded."]
    ), config=config)


    return {
    "graphs_code": result["graphs_code"],  # Include generated graph code
    "cleaned_data": result["cleaned_data"].to_csv(index=False),  # Return cleaned data
    "statistical_summary": str(result["insights"]),  # Include statistical summary
    "sql": result["sql"]  # Include generated SQL
    }

@app.post("/chat/")
async def chat(request: QueryRequest):
    user_query = request.query
    df = pd.read_json(io.StringIO(request.dataframe))

    # Simulate analysis (replace with actual LLM call if needed)
    if not user_query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Here you could call a real model like LangChain, OpenAI, etc.
     # Create a config with additional message
    config = RunnableConfig(metadata={"message": "Starting data cleaning process."})

    # Run LangGraph Workflow
    result = await chat_graph.ainvoke(ChatState(
        messages=[user_query],
        df=df
    ), config=config)


    return {
        "answer": result["messages"][-1].content,  # Include generated graph code
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)