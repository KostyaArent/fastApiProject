from pydantic import BaseModel
from typing import Literal, List, Union


class Array(BaseModel):
    array: List[Union[int, None]]

    def get_cleaned_array(self):
        return list(filter(None, self.array))

    def get_array_sum(self):
        return sum(self.get_cleaned_array())


class Result(BaseModel):
    result: int


class TaskId(BaseModel):
    id: str


class SumTask(BaseModel):
    id: str
    status: Literal['STARTED', 'RETRY', 'SUCCESS', 'FAILURE', 'INPROGRESS']
    result: Union[int, None]
