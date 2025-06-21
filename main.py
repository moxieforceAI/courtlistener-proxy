from fastapi import FastAPI, HTTPException
import httpx
import os, traceback, logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()
COURTLISTENER_API_KEY = os.getenv("CL_API_KEY")

@app.get("/search")
async def search_cases(q: str = ""):
    try:
        if not q:
            raise HTTPException(status_code=400, detail="Missing query parameter 'q'")

        url = f"https://www.courtlistener.com/api/v4/opinions/?search={q}&order_by=date_filed desc&page_size=3"
        headers = {"Authorization": f"Token {COURTLISTENER_API_KEY}", "Accept": "application/json"}
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        return res.json()

    except Exception as e:
        logging.error("Error processing request: " + traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Proxy error: {str(e)}")
