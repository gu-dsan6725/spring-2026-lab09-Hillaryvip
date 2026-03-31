from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid

from agent import Agent

app = FastAPI()

_session_cache: Dict[str, Agent] = {}

class InvocationRequest(BaseModel):
    user_id: str
    query: str
    run_id: Optional[str] = None

class InvocationResponse(BaseModel):
    response: str
    run_id: str

def get_or_create_agent(user_id: str, run_id: str) -> Agent:
    if run_id in _session_cache:
        return _session_cache[run_id]

    agent = Agent(user_id=user_id, run_id=run_id)
    _session_cache[run_id] = agent
    return agent

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Memory Agent API is running"}

@app.post("/invocation", response_model=InvocationResponse)
def invoke(request: InvocationRequest):
    run_id = request.run_id or str(uuid.uuid4())
    agent = get_or_create_agent(request.user_id, run_id)
    response = agent.chat(request.query)
    return {"response": response, "run_id": run_id}