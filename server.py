from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import List
from models import Sprint, History, Entity

import csv
import os


app = FastAPI()



@app.get('/get_sprint/{name}')
def get_sprint(name: str):
    with open('files/sprints.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for sprint in map(Sprint.model_validate, reader):
            if sprint.sprint_name == name:
                return {"result": sprint.model_dump()}
    return "Not found!"


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload/")
async def upload_files(request: Request, csv_files: List[UploadFile]):
    if len(csv_files) != 3:
        return {"error": "Вы можете загрузить 3 файла (sprints.csv, history.csv, entities.csv)"}

    for csv_file in csv_files:
        with open(os.path.join("files", csv_file.filename), "wb") as f:
            f.write(await csv_file.read())

    return {"message": "Файлы успешно загружены!"}


