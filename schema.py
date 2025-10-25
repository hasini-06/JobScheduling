from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobSchema(BaseModel): 
    name:str 
    description:str 
    interval:str 
    last_run:Optional[datetime]=None
    next_run:datetime 
    status:str 

    class Config:
        orm_mode=True

