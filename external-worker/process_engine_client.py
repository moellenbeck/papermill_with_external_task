#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import inspect
import json
import signal

from external_task_api_client.external_task_api_client_service import ExternalTaskApiClientService
from external_task_api_client.external_task_worker import ExternalTaskWorker

from external_task_api_client.external_task_results.finished import ExternalTaskFinished
from external_task_api_client.external_task_results.bpmn_error import ExternalTaskBpmnError

class BpmnError(Exception):

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

class ProcessEngineClient:

    def __init__(self, process_engine_url, identity=None):
        self._process_engine_url = process_engine_url

        if identity is None:
            self._identity = {"token": "ZHVtbXlfdG9rZW4="}
        else:
            self._identity = identity

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

        print('Using ProcessEngine at "{}"'.format(self._process_engine_url))
        external_task_client = ExternalTaskApiClientService(self._process_engine_url)

        self._worker = ExternalTaskWorker(external_task_client)

        self._tasks = []

    async def _start_external_task(self, topic, handle_action, options={}):
        max_tasks = options.get('max_tasks', 10)
        long_polling_timeout = options.get('long_polling_timeout', 10_000)
        dump_task = options.get('dump_task', True)

        #TODO: try to handle meta-data of task not only the payload
        #handle_action_spec = inspect.getfullargspec(handle_action)
        arg_count = 1 #len(handle_action_spec.args)

        async def wrapper_handle_action(task):
            print(json.dumps(task, sort_keys=True, indent=2)) is dump_task

            payload = task['payload']
            task_id = task['id']

            try:
                result = None

                if arg_count == 1:
                    result = handle_action(payload)
                else:
                    result = handle_action(payload, task)

                return ExternalTaskFinished(task_id, result)
            except BpmnError as be:
                print('bpmn error raised: ', be)
                return ExternalTaskBpmnError(task_id, be.error_code, {'message': be.error_message})
            except Exception as e:
                print('Unspecified exception raised: ', e)
                return ExternalTaskBpmnError(task_id, "GenericError", {'message': str(e)})

        return await self._worker.wait_for_handle(
            identity=self._identity,
            topic=topic,
            max_tasks=max_tasks,
            long_polling_timeout=long_polling_timeout,
            handle_action=wrapper_handle_action
        )
    
    def _create_task(self, topic, worker_func):
        worker = self._start_external_task(topic, worker_func)
        task = self._loop.create_task(worker)
        self._tasks.append(task)

    def subscribe_to_external_task_for_topic(self, topic, worker_func):
        self._create_task(topic, worker_func)

    def _register_shutdown(self):
        async def shutdown(signal, loop):
            print(f"Received exit signal {signal.__name__}...") #TODO: using logging instead of print

            for task in self._tasks:
                try:
                    task.cancel()
                except Exception as e:
                    print(e)

            loop.stop()

        signal_handler = lambda signal=signal: asyncio.create_task(shutdown(signal, self._loop))
        signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT, signal.SIGQUIT)

        for s in signals:
            self._loop.add_signal_handler(s, signal_handler)

    def start(self):
        try:    
            self._register_shutdown()
            self._loop.run_forever()
        finally:
            #self._loop.close()
            pass
