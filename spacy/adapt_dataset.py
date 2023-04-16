import spacy
import json
import argparse
import os

from spacy.tokens import DocBin

def adapt_dataset(dataset:str, dev_ratio:float, output:str):
  nlp = spacy.blank("pt")
  print("Loading dataset from: ", dataset)
  full_data = []
  with open(dataset, 'r', encoding='utf8') as f:
      data = json.load(f)
      for doc in data:
        if doc["isDone"] != True:
          continue
        full_data.append((
          doc["report"], [(entity["begin"], entity["end"], entity["entity"]) for entity in doc["entities"] if entity["entity"] != "NoduleDescription"] # ignore NoduleDescription entity since it collide with others.
        ))


  print("Using validation ratio: ", dev_ratio)
  train_ratio = 1-dev_ratio
  train_amount = int(train_ratio * len(full_data))

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
  if not os.path.exists(output):
    os.makedirs(output)
  train_output = os.path.join(output, "train.spacy")
  print("Writing train dataset to: ", train_output)
  db.to_disk(train_output)

  db = DocBin()
  for text, annotations in test_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
  dev_output = os.path.join(output, "dev.spacy")
  print("Writing dev dataset to: ", dev_output)
  db.to_disk(dev_output)

def parse_args():
    parser = argparse.ArgumentParser(description='Adapt dataset to spacy format.')
    parser.add_argument('--input', help="Dataset's path", default='./corpus/processed_documents.json')
    parser.add_argument('--dev_ratio', help="Percentage of dataset used to validation.", default=0.2)
    parser.add_argument('--output', help="Output path", default='./corpus')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    adapt_dataset(args.input, args.dev_ratio, args.output)
