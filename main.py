from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

COURTLISTENER_API_KEY = os.getenv("CL_API_KEY")

@app.get("/search")
async def search_cases(q: str = ""):
    url = f"https://www.courtlistener.com/api/v4/opinions/?search={q}&order_by=date_filed desc&page_size=3"
    headers = {
        "Authorization": f"Token {COURTLISTENER_API_KEY}",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()
