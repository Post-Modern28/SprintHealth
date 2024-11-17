from fastapi import FastAPI, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import List
from models import Sprint, History, Entity

import csv
import os


app = FastAPI()




templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload/", response_class=RedirectResponse)
async def upload_files(request: Request, csv_files: List[UploadFile]):
    if len(csv_files) != 3:
        return {"error": "Вы можете загрузить 3 файла (sprints.csv, history.csv, entities.csv)"}

    for csv_file in csv_files:
        with open(os.path.join("files", csv_file.filename), "wb") as f:
            f.write(await csv_file.read())
    
    # TODO: пока кривой переход к следующей страничке с передачей названия файла через url
    return RedirectResponse(url=f"/sprints/sprints_1.csv",
                            status_code=status.HTTP_302_FOUND)  


@app.get('/sprints/{csv_file}', response_class=HTMLResponse)
def get_sprints(request: Request, csv_file: str):
    with open(os.path.join('files', csv_file), 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        return templates.TemplateResponse("sprints.html", 
                                          {"request": request, 
                                           "sprints": map(Sprint.model_validate, reader)})

@app.get('/sprint/{name}')
def get_sprint_by_name(name: str):
    with open('files/sprints.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for sprint in map(Sprint.model_validate, reader):
            if sprint.sprint_name == name:
                return {"result": sprint.model_dump()}
    return "Not found!"
