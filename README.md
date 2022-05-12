# CiteSum
This repo provides the dataset and code for paper ["CiteSum: Citation Text-guided Scientific Extreme Summarization and Low-resource Domain Adaptation"](#).

TLDR: By pretraining on (automatically extracted) citation sentences in scientific papers, we achieve SOTA on SciTLDR, XSum, and Gigaword in zero-shot and/or few-shot settings.


## How to run
We provide the pretraining dataset [CiteSum](https://drive.google.com/file/d/1ndHCREXGSPnDUNllladh9qCtayqbXAfJ/view?usp=sharing) and checkpoints pretrained on [citation sentences](https://drive.google.com/drive/folders/1M76z4GDToTPEUzsQLfqKHP4p44t2tSls?usp=sharing) and [titles](https://drive.google.com/drive/folders/1Hr4EiMsmsQZb2HG4KF0jw4Anx9Ds8_Wp?usp=sharing).

Check out example scripts under `script/` to see how to train/evaluate on different datasets.




