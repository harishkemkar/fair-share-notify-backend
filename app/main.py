from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # ✅ this was missing
from pydantic import BaseModel
from typing import List


app = FastAPI()


# Allow frontend (localhost:3000) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Friend(BaseModel):
    name: str
    contact: str

class SplitRequest(BaseModel):
    amount: float
    friends: List[Friend]

@app.post("/split")
async def split_bill(request: SplitRequest):
    if not request.friends:
        return {"error": "No friends provided"}

    per_person = request.amount / len(request.friends)
    result = [
        {"name": f.name, "contact": f.contact, "owes": per_person}
        for f in request.friends
    ]
    return result