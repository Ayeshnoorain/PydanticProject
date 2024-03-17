from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    user_id: str
    survey_i: int
    mid: int
    mid2: int
    sessionid: int
    date: datetime
    time: datetime
    daymonth: int
    weekday: int
    weeknum: int
    month: int
    quarter: int
    year: int

external_data = {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
user = User(**external_data)
print(user)
print(user.id)


user = User()