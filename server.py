from fastapi import FastAPI, UploadFile, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import List
from datetime import datetime
from models import Sprint, History, Entity
import Aggregations

import csv
import os


app = FastAPI()




templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/sprints", response_class=HTMLResponse)
async def upload_files(request: Request, csv_files: List[UploadFile]):
    if len(csv_files) != 3:
        return "Нужно 3 файла!"

    file_names = []
    for csv_file in csv_files:
        with open(os.path.join("files", csv_file.filename), "wb") as f:
            file_names.append(os.path.join('files', csv_file.filename))
            f.write(await csv_file.read())
    result = Aggregations.parse_data(*sorted(file_names))  # TODO кривое отправление через сортировку
    print(result)
    return templates.TemplateResponse("sprints.html", 
                                      {"request": request, 
                                       "sprints": result['teams']['sprints']})

@app.get('/sprint/{name}')
def get_sprint_by_name(request: Request, name: str, selected: str | None = None, 
                       sprint_end_date: str | None = None):
    sprint_df = Aggregations.get_sprint_by_name(name)

    sprint_status = Aggregations.analyze_sprint(sprint_df)
    sprint_status.update(Aggregations.parse_sprint(sprint_df))
    all_teams = sprint_status['teams']

    if selected:
        selected = selected.split(',')
        sprint_df = Aggregations.select_teams(sprint_df, selected)
    
    if sprint_end_date:
        sprint_end_date = datetime.strptime(sprint_end_date, '%Y-%m-%d')
        Aggregations.limit_date(sprint_df, sprint_end_date)
        
    sprint_status = Aggregations.analyze_sprint(sprint_df)
    sprint_status.update(Aggregations.parse_sprint(sprint_df))
    sprint_name = sprint_df["sprint_name"].iloc[0]
    sprint_status['teams'] = all_teams
    return templates.TemplateResponse("sprint.html", {"request": request, 
                                                      "name": sprint_name, 
                                                      "info": sprint_status, 
                                                      'selected': selected}) 
