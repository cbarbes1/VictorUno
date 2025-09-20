from fastapi import FastAPI
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
import os
import uvicorn

app = FastAPI()

def respond(state: dict):
    # model should exist in your host's Ollama (e.g., `ollama pull llama3.1:8b`)
    model = os.getenv("OLLAMA_MODEL", "gemma3:27b")
    llm = ChatOllama(model=model)
    reply = llm.invoke(state.get("message", ""))
    return {"message": str(reply)}

# graph = StateGraph(dict)
# graph.add_node("respond", respond)
# graph.set_entry_point("respond")
# graph.add_edge("respond", END)
# compiled = graph.compile()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(payload: str):
    print(payload)
    out = respond({"message": payload})
    return {"reply": out["message"]}

def main():
    # Keep port configurable for containers
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("victoruno.app:app", host=host, port=port)
