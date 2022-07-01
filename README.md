# CiteSum
This repo provides the dataset, model checkpoints, and code for paper ["CiteSum: Citation Text-guided Scientific Extreme Summarization and Low-resource Domain Adaptation"](https://arxiv.org/abs/2205.06207).

TLDR: By pretraining on (automatically extracted) citation sentences in scientific papers, we achieve SOTA on SciTLDR, XSum, and Gigaword in zero-shot and/or few-shot settings.

## Data & Checkpoints
Our data is on [Huggingface Hub](https://huggingface.co/datasets/nbroad/citesum)! You can load it simply by the following (credit @nbroad1881):
```
from datasets import load_dataset

ds = load_dataset("nbroad/citesum")
```

We also provide the [dataset](https://drive.google.com/file/d/1ndHCREXGSPnDUNllladh9qCtayqbXAfJ/view?usp=sharing) and checkpoints pretrained on its [citation sentences](https://drive.google.com/drive/folders/1M76z4GDToTPEUzsQLfqKHP4p44t2tSls?usp=sharing) and [titles](https://drive.google.com/drive/folders/1Hr4EiMsmsQZb2HG4KF0jw4Anx9Ds8_Wp?usp=sharing) in Google Drive.

## How to run
Check out example scripts under `script/` to see how to train/evaluate on different datasets.




