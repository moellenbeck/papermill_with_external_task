#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json

import asyncio
import papermill as pm

from external_task_api_client.external_task_api_client_service import ExternalTaskApiClientService
from external_task_api_client.external_task_worker import ExternalTaskWorker

from external_task_api_client.external_task_finished import ExternalTaskFinished
from external_task_api_client.external_task_bpmn_error import ExternalTaskBpmnError

async def _handle_work(task):
    print(json.dumps(task, sort_keys=True, indent=2))

    input_filename = 'input_papermill.ipynb'
    output_filename = 'output_papermill.ipynb'

    hello_param = task['payload']['a key']

    pm.execute_notebook(
        input_filename,
        output_filename,
        parameters=dict(hello=hello_param)
    )

    task_result = {"output_filename": output_filename}

    return ExternalTaskFinished(task["id"], task_result)

@asyncio.coroutine
def _start_worker(worker):
    return worker.wait_for_handle(
        identity={"token": "ZHVtbXlfdG9rZW4="},
        topic="PapermillTopic",
        max_tasks=10,
        long_polling_timeout=10_000,
        handle_action=_handle_work
    )

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)

    process_engine_location = sys.argv[1] if len(sys.argv) == 2 else 'http://localhost:8000'

    print('Using ProcessEngine at "{}"'.format(process_engine_location))
    external_task_client = ExternalTaskApiClientService(process_engine_location)

    worker = ExternalTaskWorker(external_task_client)

    loop.run_until_complete(_start_worker(worker))


main()
