import spacy
import argparse

def test_model(model: str):
    print("Loading model ", model, "...\n")
    nlp = spacy.load(model)
    report = "Nódulo não calcificado, contornos regulares, no segmento anterior do lobo superior esquerdo, medindo 0,3 cm, indeterminado."
    doc = nlp(report)

    print("Evaluating text:")
    print(report, end='\n\n')

    print("Entities found:")
    for ent in doc.ents:
        text = "'" + ent.text + "'"
        print(f"{ent.label_:<15}: {text:<35} ({ent.start_char}, {ent.end_char}) ")

def parse_args():
    parser = argparse.ArgumentParser(description='Test a NER model')
    parser.add_argument('--model', help="Model's path", default='./output/model-best')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    test_model(args.model)
