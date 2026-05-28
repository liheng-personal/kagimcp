import os
import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.routing import Route

UPSTREAM = "http://localhost:8081"
KAGI_API_KEY = os.environ["KAGI_API_KEY"]

async def proxy(request: Request):
    headers = dict(request.headers)
    headers["authorization"] = f"Bearer {KAGI_API_KEY}"
    headers.pop("host", None)

    url = UPSTREAM + str(request.url.path)
    if request.url.query:
        url += "?" + request.url.query

    body = await request.body()
    client = httpx.AsyncClient(timeout=120.0)
    req = client.build_request(
        method=request.method,
        url=url,
        headers=headers,
        content=body,
    )
    response = await client.send(req, stream=True)

    async def stream_body():
        async for chunk in response.aiter_bytes():
            yield chunk
        await client.aclose()

    return StreamingResponse(
        stream_body(),
        status_code=response.status_code,
        headers=dict(response.headers),
    )

app = Starlette(routes=[
    Route("/", proxy, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]),
    Route("/{path:path}", proxy, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]),
])
