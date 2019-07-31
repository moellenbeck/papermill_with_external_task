#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json

import asyncio
import papermill as pm

from external_task_api_client.external_task_api_client_service import ExternalTaskApiClientService
from external_task_api_client.external_task_worker import ExternalTaskWorker

from external_task_api_client.external_task_api_client_service import ExternalTaskApiClientService
from external_task_api_client.external_task_worker import ExternalTaskWorker


from external_task_api_client.external_task_results.finished import ExternalTaskFinished
from external_task_api_client.external_task_results.bpmn_error import ExternalTaskBpmnError

@asyncio.coroutine
def _start_worker(worker, identity, topic, handle_action):
    return worker.wait_for_handle(
        identity=identity,
        topic=topic,
        max_tasks=10,
        long_polling_timeout=10_000,
        handle_action=handle_action
    )

async def _handle_work(task):
    try:
        print(json.dumps(task, sort_keys=True, indent=2))

        input_filename = 'input_papermill.ipynb'
        output_filename = 'output_papermill.ipynb'

        hello_param = task['payload']['a key']
        #hello_param = task.payload['a key'] # with error

        pm.execute_notebook(
            input_filename,
            output_filename,
            parameters=dict(hello=hello_param)
        )

        task_result = {"output_filename": output_filename}

        return ExternalTaskFinished(task["id"], task_result)
    except Exception as e:
        print('Raised a exception: ', e)
        return ExternalTaskBpmnError(task["id"], "error_message", {'hello': 'world'})

def handle_external_task(process_engine_url, identity, topic, worker_func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)

    print('Using ProcessEngine at "{}"'.format(process_engine_url))
    external_task_client = ExternalTaskApiClientService(process_engine_url)

    worker = ExternalTaskWorker(external_task_client)

    loop_runner = _start_worker(worker, identity, topic, worker_func)

    loop.run_until_complete(loop_runner)

def main():
    process_engine_location = sys.argv[1] if len(sys.argv) == 2 else 'http://localhost:8000'

    identity = {"token": "ZHVtbXlfdG9rZW4="}

    topic = 'PapermillTopic'

    handle_external_task(process_engine_location, identity, topic, _handle_work)

main()
