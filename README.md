# Wir kann man die ProcessEngine+ExternalTask mit Jupyter-Notebooks verbinden
Jupyter-Notebooks sind eine gute Möglichkeit Quellcode mit Dokumentation zu verbinden und direkt ausführen. Dabei können auch Grafiken, die durch den Quellcode generiert werden, in die Ausgabe bzw. das Notebook eingebettet werden.

## Installation
* [GitHub - pyenv/pyenv: Simple Python version management](https://github.com/pyenv/pyenv)
* [ProcessEngine.io](https://www.process-engine.io/)

### Notwendige Bibliotheken für Python

`python3 -m pip install —user —requirement requirements.txt`

### ProcessEngine

* BPMN-Studio öffnen
* Solution für diesen Ordner öffnen
* Prozess *sample_papermill.bpmn* auf die lokale Process-Engine veröffentlichen

### Optional: Anpassen von Jupyter-Notebook

Durch die Verwendung von  [https://github.com/mwouts/jupytext](https://github.com/mwouts/jupytext)  kann die Versionsverwaltung von Jupyter-Notebook deutlich verbessert werden. Normalerweise werden Notebooks als JSON abgespeichert, da sie sowohl Eingaben wie auch die erzeugten Ausgaben erhalten. Jupytext trennt dies, da es Eingaben (hier in .Rmd) und Ausgaben (weiterhin in .ipynd)  verwaltet.

Tutorial zur einfachen und korrekten Installation: [Installation — Jupytext  documentation](https://jupytext.readthedocs.io/en/latest/install.html)

## Anwendung
### ExternalTask

Der externe Task verarbeitet Anfragen für das Topic *PapermillTopic* wobei erwartet wird, dass das Payload einen Schlüssel *a key*  hat und dieser wird an das Jupyter-Notebook *input_papermill.ipynb* übergeben und daraus wird dann das Jupyter-Notebook *output_papermill.ipynb* mit dem eingesetzten Werten erstellt.

Gestartet wird der External-Task-Worker wie folgt:

`python3 external_worker.py`

Die folgende Ausgabe zeigt das erfolgreiche Starten des Workers an:

`Using ProcessEngine at "http://localhost:8000"`

### Prozess

Der Beispiel-Prozess besteht aus einem Start- und End-Event, sowie einen Service-Task, der nach dem „External-Task-Pattern“ konfiguriert ist.

Nachdem der Prozess deployed ist, kann er gestartet werden und über den LET wird die Verarbeitung angezeigt. In der Console des Workers wird die Ausgaben des aktuellen JSON ausgegeben:

```JSON
{
  "correlationId": "e0c21d54-c9c1-41ee-b019-bf386762ab9d",
  "createdAt": "2019-07-29T15:25:23.606Z",
  "error": null,
  "finishedAt": null,
  "flowNodeInstanceId": "98bcffe2-d9e0-4caa-91de-d3b6d035b0da",
  "id": "dbfb0491-6e17-45b4-9543-e80fa107cf6a",
  "identity": {
    "token": "ZHVtbXlfdG9rZW4=",
    "userId": "dummy_token"
  },
  "lockExpirationTime": "2019-07-29T15:25:53.632Z",
  "payload": {
    "a key": "hello this is a key from a process"
  },
  "processInstanceId": "1535912c-c428-4599-867c-0fdf9c07d908",
  "processModelId": "sample_papermill",
  "state": "pending",
  "topic": "PapermillTopic",
  "workerId": "699ddca4-7155-429b-a1be-a68d99ad348d"
}
```

### Ergebnis

Wenn der Prozess erfolgreich durchgelaufen ist, dann kann man unter Jupyter-Notebook die Ausgabe *output_papermill.ipynb* angesehen werden.


* *In [2] injected-parameters*: die einfügten Parameter aus dem Prozess
* *In [3]*: Die Ausgabe … hier `a name from a process` 

## Weiterführende Links
* [https://papermill.readthedocs.io/en/latest/](https://papermill.readthedocs.io/en/latest/) 
* [ProcessEngine.io - Getting Started](https://www.process-engine.io/docs/getting-started/)

#processengine/external_task# #technik/jupyter-notebook#