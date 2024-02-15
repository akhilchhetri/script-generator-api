import os
from io import BytesIO

import httpx
import requests
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]
base_api = (
    "http://script-generation-demo-1979457470.eu-north-1.elb.amazonaws.com/api/v1"
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.post("/upload")
async def upload_doc(files: UploadFile = File(...)):
    try:
        contents = await files.read()
        api_data = await upload_file(contents, files)
        if api_data:
            return api_data
        else:
            return {"message": "API call failed"}
    except Exception as e:
        return {"message": "API call failed", "error": e}


@app.post("/script/generate")
async def script_generate(request: Request):
    try:
        data = await request.json()
        response = requests.post(
            base_api + "/script/generate/",
            json=data,
        )
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return {"message": "Api call failed", "code": "500", "type": "error"}
    except Exception as e:
        return {"success": False, "error": e}


@app.post("/script/qna/generate")
async def qna_generate(request: Request):
    try:
        data = await request.json()
        response = requests.post(base_api + "/qna/generate/", json=data)
        print("this is response", response.json())
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return {"message": "Api call failed", "code": "500", "type": "error"}
    except Exception as e:
        return {"success": False, "error": e}


@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        print("this is data", data)
        response = requests.post(base_api + "/chat/", json=data)
        print("this is response", response.json())
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return {"message": "Api call failed", "code": "500", "type": "error"}
    except Exception as e:
        print("this is error", e)
        return {"success": False, "error": e}


@app.patch("/syllabus/update")
async def syllabus_update(request: Request):
    try:
        data = await request.json()
        response = requests.patch(base_api + "/syllabus/update/", json=data)
        print("this is response", response.json())
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return {"message": "Api call failed", "code": "500", "type": "error"}
    except Exception as e:
        return {"success": False, "error": e}


async def upload_file(contents, file):
    async with httpx.AsyncClient() as client:
        files = {
            "pdf_file": (file.filename, BytesIO(contents), "application/octet-stream")
        }

        response = await client.post(
            "http://script-generation-demo-1979457470.eu-north-1.elb.amazonaws.com/api/v1/syllabus/extract/",
            files=files,
        )
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
