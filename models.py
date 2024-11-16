from pydantic import BaseModel
from typing import Optional


class Sprint(BaseModel):
    sprint_name: str
    sprint_status: str
    sprint_start_date: str
    sprint_end_date: str
    entity_ids: str # TODO сделать адекватный парсинг.


class History(BaseModel):
    entity_id: Optional[int]
    history_property_name: Optional[str]
    history_date: Optional[str]
    history_version: Optional[int]
    history_change_type: Optional[str]
    history_change: Optional[str]


class Entity(BaseModel):
    entity_id: int
    area: str
    type: str
    status: str
    state: str
    priority: str
    ticket_number: str
    name: str
    create_date: str
    created_by: str
    update_date: str # 
    updated_by: str
    parent_ticket_id: Optional[int]
    assignee: str
    owner: str
    due_date: Optional[str]
    rank: Optional[int]
    estimation: Optional[float]
    spent: Optional[float] 
    workgroup: str
    resolution: str


