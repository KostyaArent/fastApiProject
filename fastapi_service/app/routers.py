import json

from fastapi import APIRouter, HTTPException

from worker import celery

from models import Array, Result, SumTask, TaskId

router = APIRouter(
    prefix="/sum",
    tags=["sum"],
)


@router.post('/sync',
             response_model=Result,
             responses={
                 200: {"description": "Return the JSON result of array's sum"}})
def get_sum(data: Array) -> Result:
    result = Result(result=data.get_array_sum())
    return result


@router.post('/async/create',
             response_model=TaskId,
             responses={
                 200: {"description": "Return the JSON with task's id"}})
async def get_sum(data: Array) -> TaskId:
    task_name = "sum_task"
    task = celery.send_task(task_name, args=[data.array])
    task_id = TaskId(id=task.id)
    return task_id


@router.get("/check_task/{id}",
            response_model=SumTask,
            responses={
                200: {"description": "Return the JSON with task's id, status, result"},
                404: {"detail": "Task not found"}})
def check_task(id: str) -> SumTask:
    task = celery.AsyncResult(id)
    if task.state == 'SUCCESS':
        sum_task = SumTask(
            id=task.id,
            status=task.state,
            result=task.result
        )
    elif task.state == 'FAILURE':
        response = json.loads(task.backend.get(task.backend.get_key_for_task(task.id)).decode('utf-8'))
        del response['children']
        del response['traceback']
    elif task.state == 'PENDING':
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        sum_task = SumTask(
            id=task.id,
            status=task.state,
            result=None
        )
    return sum_task
