from fastapi import FastAPI
from typing import List
from models import Sprint, History, Entity
import csv


app = FastAPI()


@app.get('/get_sprint/{name}')
def get_sprint(name: str):
    with open('files/sprints.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for sprint in map(Sprint.model_validate, reader):
            if sprint.sprint_name == name:
                return {"result": sprint.model_dump()}
    return "Not found!"


@app.post('/save_data')
def save_data(sprints: List[Sprint], history: List[History], entities: List[Entity]):
    # TODO придумать как поменять формат datetime в нормальную строку.
    with open('files/sprints.csv', mode='w', encoding='utf-8') as f:
        writer = csv.DictWriter(f)
        for sprint in sprints:
            writer.writerow(sprint.model_dump())

    with open('files/history.csv', mode='w', encoding='utf-8') as f:
        writer = csv.DictWriter(f)
        for record in history:
            writer.writerow(record.model_dump())

    with open('files/entities.csv', mode='w', encoding='utf-8') as f:
        writer = csv.DictWriter(f)
        for entity in entities:
            writer.writerow(entity.model_dump())
