import spacy
import argparse

from spacy.tokens import DocBin

# This is used to expose cases when the model failed to predict,
# in order to find clear annotation typos/missclicks on the dataset.
# eg.: - Entities annotated with the wrong type;
#      - Entities annotated with wrong boundaries;
#      - Entities annotated with different patterns.
def print_model_misses(model: str, corpus:str, quantity_diff:bool):
    print("Loading model ", model, "...\n")
    nlp = spacy.load(model)
    doc_bin = DocBin().from_disk(corpus).get_docs(nlp.vocab)
    corpus = []
    for doc in doc_bin:
        text = doc.text
        annotated_ents = [(ent.text, ent.label_) for ent in list(doc.ents)]
        corpus.append((text, annotated_ents))

    predicted_corpus = []
    for text, _ in corpus:
        doc = nlp(text)
        predicted_ents = [(ent.text, ent.label_) for ent in list(doc.ents)]
        predicted_corpus.append(predicted_ents)

    assert len(corpus) == len(predicted_corpus)
    
    for i in range(len(corpus)):
        annotated_ents = corpus[i][1]
        predicted_ents = predicted_corpus[i] 

        if len(annotated_ents) != len(predicted_ents):
            if quantity_diff:
                print("Diff in number of entities - ")
                print("Annotated:")
                for ent in annotated_ents:
                    print(" ", ent)
                print("Predicted:")
                for ent in predicted_ents:
                    print(" ", ent)
                print()
            continue
        annotated_ents = sorted(annotated_ents, key=lambda x : x[1])
        predicted_ents = sorted(predicted_ents, key=lambda x : x[1])
        for j in range(len(annotated_ents)):
            annotated_ent = annotated_ents[j]
            predicted_ent = predicted_ents[j]
            if annotated_ent != predicted_ent:
                print(f"Diff in entity - ")
                print(f"Annotated: ({annotated_ent[0]}, {annotated_ent[1]})")
                print(f"Predicted: ({predicted_ent[0]}, {predicted_ent[1]})")
                print()

def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate a NER model entity')
    parser.add_argument('--model', help="Model's path", default='./output/model-best')
    parser.add_argument('--corpus', help="Corpus to evaluate", default='./corpus/test.spacy')
    parser.add_argument('--quantity_diff', help="Print when annotated count has diff", default=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print_model_misses(args.model, args.corpus, args.quantity_diff)
