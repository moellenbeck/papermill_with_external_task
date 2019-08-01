#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import papermill as pm

from process_engine_client import ProcessEngineClient, BpmnError

def _worker(payload):

    input_filename = 'input_papermill.ipynb'
    output_filename = 'output_papermill.ipynb'

    hello_param = payload['a key']

    pm.execute_notebook(
        input_filename,
        output_filename,
        parameters=dict(hello=hello_param)
    )

    result = {"output_filename": output_filename}

    #raise BpmnError(300, 'bpmn fehler - auch provoziert')
    #raise Exception('provozierter unspezifischer Fehler')

    return result

def main():
    process_engine_location = sys.argv[1] if len(sys.argv) == 2 else 'http://localhost:8000'
    topic = 'PapermillTopic'

    process_engine_client = ProcessEngineClient(process_engine_location)

    process_engine_client.subscribe_to_external_tasks_with_topic(topic, _worker)

main()
