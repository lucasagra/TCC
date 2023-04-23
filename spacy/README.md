# Spacy NER model

https://spacy.io/usage/training

# Instalation
Following procedures were tested on Ubuntu 20.04, using Python 3.8.10, and Pip 23.0.1.

## Enabling GPU

### Check CUDA version using
```
nvcc --version
```
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2020 NVIDIA Corporation
Built on Mon_Nov_30_19:08:53_PST_2020
Cuda compilation tools, release 11.2, V11.2.67
Build cuda_11.2.r11.2/compiler.29373293_0
```
In my case is 11.2. All the installed libs should have support to CUDA version <= than this.

### Install using appropriate CUDA version: 

```
python -m venv env
source env/bin/activate
pip install -U pip setuptools wheel
pip install -U 'spacy[cuda112,transformers,lookups]'
python -m spacy download pt_core_news_lg
```

Then replace PyTorch version to a older one, compatible with the installed CUDA version:
```
pip install torch==1.10.1+cu111 torchvision==0.11.2+cu111 torchaudio==0.10.1 -f https://download.pytorch.org/whl/cu111/torch_stable.html
```
You can find the list of versions here:
https://pytorch.org/get-started/previous-versions/

# Training

## Dataset
Run `python adapt_dataset.py --input=<dataset>` passing the dataset generated on the EntityProcessor module as input. A `corpus` folder will be created with the train/dev splitted dataset in the spacy format.

You can set a custom output using `--output` and a custom validation ratio with `--dev_ratio` (default is 20%).

## Configuration
The file `config.cfg` contains all the configuration and information of the model/pipeline/architecture to be used.

More info at https://spacy.io/usage/training#quickstart

## Training
```
python -m spacy train config.cfg --gpu-id 0 --output=output
```

# Testing model

Run `python test_model_example.py --model=output/model-best --report="Nódulo não calcificado, contornos regulares, no segmento anterior do lobo superior esquerdo, medindo 0,3 cm, indeterminado."`

Output example:

```
Loading model  ./output/model-best ...

Evaluating text:
Nódulo não calcificado, contornos regulares, no segmento anterior do lobo superior esquerdo, medindo 0,3 cm, indeterminado.

Entities found:
NoduleCount    : 'Nódulo'                            (0, 6) 
NoduleType     : 'não calcificado'                   (7, 22) 
NoduleInfo     : 'contornos regulares'               (24, 43) 
NoduleLocation : 'lobo superior esquerdo'            (69, 91) 
NoduleSize     : '0,3 cm'                            (101, 107)
```
