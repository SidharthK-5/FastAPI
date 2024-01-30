from fastapi import FastAPI
from fastapi.responses import JSONResponse
from router import router as file_handling_router


app = FastAPI(title="File Handling", description="Upload, Read, Edit and Delete files")

app.include_router(router=file_handling_router, tags=["File Handling Routes"])


@app.get("/")
async def health_check():
    return JSONResponse(content={"response": "Health check successful..."})
