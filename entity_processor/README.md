This module processes the entity annotation `[<entity>](<marked_text>)` format, produced by the annotator app, to the `json format`.

for example:

    "report": "[NoduleCount](Nódulo) [NoduleType](não calcificado) ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun",
    "num1": "",
    "num2": "",
    "date": "",
    "id": "10001",
    "isDone": true


Will become: 


    "report": "Nódulo não calcificado ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun lorem ipsun",
    "num1": "",
    "num2": "",
    "date": "",
    "id": "10001",
    "isDone": true,
    "entities": [
      {
        "entity": "NoduleCount",
        "value": "Nódulo",
        "begin": 0,
        "end": 6
      },
      {
        "entity": "NoduleType",
        "value": "não calcificado",
        "begin": 7,
        "end": 22
      }
    ]

It is important to have both formats available since the first one is editable while the second one has the text report unchangeable due to the entities boundaries.