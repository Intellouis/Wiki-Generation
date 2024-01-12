# Wiki-Generation

This is the repo for NLPDL 2023 Fall Final Project: Wiki Generation.

## Setup
```
git clone https://github.com/Intellouis/Wiki-Generation
```
After creating a new virtual (conda) environment, run: 
```
pip install -r requirements.txt
```

## Usage

To ask GPT-4 for rewriting the corpuses and materials, run:
```
python GPT_denoising.py --file <filename>
```

To use rule-based denoising, run:
```
python rule_based_denoising.py 
```

To evaluate the ROUGE-L scores on denoised datasets, run:
```
python rouge_evaluate.py
```

To call GPT-4 to generate wiki documents, run:
```
python generate.py --method <method_number>
```
where ```<method_number>``` comes from:
```{1: vanilla baseline; 2: CoT; 3: ICL; 4: pre-defined template outline}```

To use GPT-4 to conduct rating on the generated documents, run:
```
python GPT_evaluate.py
```

To evaluate on both denoised datasets and generated documents using grammar errors and readability, run:
```
python DLA.py
```
