import time
import traceback
from typing import List, Union

from celery import states

from worker import celery


@celery.task(name="sum_task", bind=True)
def sum_task(self, array: List[Union[int, None]]) -> int:
    try:
        self.update_state(state='INPROGRESS')
        result = sum(list(filter(None, array)))
        return result

    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex
