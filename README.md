# Wiki-Generation

This is the repo for NLPDL 2023 Fall Final Project: Wiki Generation. In this project, we make an attempt to use GPT-4 to generate wiki documents with high quality. We test GPT-4 on 6 different keywords chosen from various areas and domains, and compare the performance over four methods. We collect proper datasets based on the keywords, adding with denoising techniques. We evaluate both the denoised passages and the generated documents with proper metrics, and results show that GPT-4 has the ability of generating wiki documents with high quality overall. We also apply some prompting techniques, including CoT and ICL, which have demonstrated effectiveness in enhancing the ability of LLMs for better wiki generation.

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
