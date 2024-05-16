import os
from io import BytesIO

import httpx
import requests
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

origins = ["*"]
base_api = (
    "http://script-generation-prod-1695652430.eu-north-1.elb.amazonaws.com/api/v1"
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
    url = "http://script-generation-prod-1695652430.eu-north-1.elb.amazonaws.com/api/v1/syllabus/extract/"
    params = {
        "document_type": "research_paper",
        "use_llm": "false",
        "language": "British English",
    }
    files = {"pdf_file": (files.filename, files.file, "application/pdf")}

    try:
        response = requests.post(url, params=params, files=files)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"message": "API call failed"}
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {"message": "API call failed", "error": e}


@app.post("/script/generate")
async def script_generate(request: Request):
    try:
        data = await request.json()
        params = {
            "language": "British English",
        }
        response = requests.post(
            base_api + "/script/generate/",
            params=params,
            json=data,
        )
        print("this is response", response.json())
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
        params = {
            "language": "British English",
        }
        response = requests.post(base_api + "/qna/generate/", params=params, json=data)
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


# Syllabus update method
@app.patch("/syllabus/update")
async def syllabus_update(request: Request):
    try:
        data = await request.json()
        print(data["id"])
        params = {"heading_id": data["id"]}
        response = requests.patch(
            base_api + f"/syllabus/update/", params=params, json=data
        )
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return {
                "error": True,
                "message": "Api call failed",
                "code": "500",
                "type": "error",
            }
    except Exception as e:
        print("this is exception", e)
        return {"success": False, "error": True, "message": e}


# Syllabus delete method
@app.post("/syllabus/delete")
async def syllabus_delete(request: Request):
    try:
        data = await request.json()
        params = {"heading_id": data["id"]}
        response = requests.delete(base_api + f"/syllabus/delete/", params=params)
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return {
                "error": True,
                "message": "Api call failed",
                "code": "500",
                "type": "error",
            }
    except Exception as e:
        print("this is exception", e)
        return {"success": False, "error": True, "message": e}


@app.patch("/script/update")
async def script_update(request: Request, script_id):
    try:
        data = await request.json()
        response = requests.patch(
            base_api + f"/script/update?script_id={script_id}", json=data
        )
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return {"message": "Api call failed", "code": "500", "type": "error"}
    except Exception as e:
        return {"success": False, "error": e}


@app.patch("/qna/update")
async def script_update(request: Request, question_id: str):
    try:
        data = await request.json()
        response = requests.patch(
            base_api + f"/qna/update?question_id={question_id}", json=data
        )
        print("this is response", response.json())

        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return {"message": "Api call failed", "code": "500", "type": "error"}
    except Exception as e:
        return {"success": False, "error": e}


@app.post("/qna/delete")
async def script_update(question_id: str):
    try:
        response = requests.delete(base_api + f"/qna/delete?question_id={question_id}")
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
        try:
            files = {
                "pdf_file": (
                    file.filename,
                    BytesIO(contents),
                    "application/octet-stream",
                )
            }
            params = {
                "document_type": "research_paper",
                "use_llm": "false",
                "language": "British English",
            }

            response = await client.post(
                base_api + "/syllabus/extract/",
                params=params,
                files=files,
            )
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return None
        except Exception as e:
            print("this is error", e)
            return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
