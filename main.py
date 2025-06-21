@app.get("/search")
async def search_cases(q: str = ""):
    try:
        if not q:
            raise HTTPException(status_code=400, detail="Missing query parameter 'q'")

        url = f"https://www.courtlistener.com/api/v4/opinions/?search={q}&order_by=date_filed+desc&page_size=3"
        headers = {
            "Authorization": f"Token {COURTLISTENER_API_KEY}",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=headers, timeout=15)

        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=f"Error from CourtListener: {res.text}")

        return res.json()

    except Exception as e:
        logging.error("Error processing request: " + traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Proxy error: {str(e)}")
