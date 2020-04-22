#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import papermill as pm

from process_engine_client import ProcessEngineClient, BpmnError

def _worker(payload):

    input_filename = 'input_papermill.ipynb' # flownode.bpmn_config.['input']
    output_filename = 'output_papermill.ipynb'

    pm.execute_notebook(
        input_filename,
        output_filename,
        parameters=payload
    )

    result = {"output_filename": output_filename}

    #raise BpmnError(300, 'bpmn fehler - auch provoziert')
    #raise Exception('provozierter unspezifischer Fehler')

    return result

def main():
    process_engine_stable = 'http://localhost:56000'
    process_engine_beta = 'http://localhost:56000'
    process_engine_alpha = 'http://localhost:56000'

    default_process_engine = process_engine_stable

    process_engine_location = sys.argv[1] if len(sys.argv) == 2 else default_process_engine
    topic = 'PapermillTopic'

    process_engine_client = ProcessEngineClient(process_engine_location)

    process_engine_client.subscribe_to_external_task_for_topic(topic, _worker)

    process_engine_client.start()
    
main()
