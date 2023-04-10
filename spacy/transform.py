import spacy
import json
from spacy.tokens import DocBin

nlp = spacy.blank("pt")
full_data = []
with open('./corpus/processed_documents100.json', 'r', encoding='utf8') as f:
    data = json.load(f)
    for doc in data:
      if doc["isDone"] != True:
        continue
      full_data.append((
        doc["report"], [(entity["begin"], entity["end"], entity["entity"]) for entity in doc["entities"] if entity["entity"] != "NoduleDescription"] # ignore NoduleDescription entity since it collide with others.
      ))

train_test_ratio = 0.8
train_amount = int(train_test_ratio * len(full_data))

train_data = full_data[:train_amount]
test_data = full_data[train_amount:]

# the DocBin will store the example documents
db = DocBin()
for text, annotations in train_data:
  doc = nlp(text)
  ents = []
  for start, end, label in annotations:
      span = doc.char_span(start, end, label=label)
      ents.append(span)
  doc.ents = ents
  db.add(doc)
db.to_disk("./corpus/train.spacy")

db = DocBin()
for text, annotations in test_data:
  doc = nlp(text)
  ents = []
  for start, end, label in annotations:
      span = doc.char_span(start, end, label=label)
      ents.append(span)
  doc.ents = ents
  db.add(doc)
db.to_disk("./corpus/dev.spacy")