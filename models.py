from pydantic import BaseModel, field_validator, field_serializer
from typing import Optional, List
from datetime import datetime


class Sprint(BaseModel):
    sprint_name: str
    sprint_status: str
    sprint_start_date: datetime
    sprint_end_date: datetime
    entity_ids: List[int]

    @field_validator('sprint_start_date', 'sprint_end_date', mode='before')
    @classmethod
    def specify_sprint_date(cls, date: str) -> datetime:
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    
    @field_validator('entity_ids', mode='before')
    @classmethod
    def parse_entity_ids(cls, brackets_list: str) -> List[int]:
        try:
            return list(map(int, brackets_list.strip('{}').split(',')))
        except Exception as e:
            raise ValueError("List must be in {}, exception:", e)
        
    @field_serializer('sprint_start_date', 'sprint_end_date')
    @classmethod
    def save_date(cls, field: datetime, _info) -> str:
        return field.strftime('%Y-%m-%d %H:%M:%S.%f')


class History(BaseModel):
    entity_id: int
    history_property_name: str
    history_date: datetime
    history_version: int
    history_change_type: str
    history_change: datetime

    @field_validator('history_date', mode='before')
    @classmethod
    def specify_history_date(cls, date: str) -> datetime:
        return datetime.strptime(date, '%M/%d/%y %H:%M')

    @field_validator('history_change', mode='before')
    @classmethod
    def specify_sprint_date(cls, date: str) -> datetime:
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
     
    @field_serializer('history_change')
    @classmethod
    def save_change_date(cls, field: datetime, _info) -> str:
        return field.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    @field_serializer('history_date')
    @classmethod
    def save_date(cls, field: datetime, _info) -> str:
        return field.strftime('%M-%d-%y %H:%M')



class Entity(BaseModel):
    entity_id: int
    area: str
    type: str
    status: str
    state: str
    priority: str
    ticket_number: str
    name: str
    create_date: datetime
    created_by: str
    update_date: datetime
    updated_by: str
    parent_ticket_id: Optional[int]
    assignee: str
    owner: str
    due_date: Optional[datetime]
    rank: Optional[int]
    estimation: Optional[float]
    spent: Optional[float] 
    workgroup: str
    resolution: str

    @field_validator('create_date', 'update_date', 'due_date', mode='before')
    @classmethod
    def parse_datetime(cls, date: str) -> datetime:
        return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

    @field_serializer('create_date', 'update_date', 'due_date')
    @classmethod
    def save_date(cls, field: datetime, _info) -> str:
        return field.strftime('%Y-%m-%d %H:%M:%S.%f')
