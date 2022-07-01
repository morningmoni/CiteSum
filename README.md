# CiteSum
This repo provides the dataset, model checkpoints, and code for paper ["CiteSum: Citation Text-guided Scientific Extreme Summarization and Low-resource Domain Adaptation"](https://arxiv.org/abs/2205.06207).

TLDR: By pretraining on (automatically extracted) citation sentences in scientific papers, we achieve SOTA on SciTLDR, XSum, and Gigaword in zero-shot and/or few-shot settings.

## How to run (Huggingface)
Our [CiteSum dataset](https://huggingface.co/datasets/nbroad/citesum) is on Huggingface Hub. You can load it simply by the following (credit @nbroad1881):
```
from datasets import load_dataset

ds = load_dataset("nbroad/citesum")
```

To use our model pretrained on citation texts:
```
from transformers import pipeline
summarizer = pipeline("summarization", model="yuningm/bart-large-citesum")

article = ''' We describe a convolutional neural network that learns\
 feature representations for short textual posts using hashtags as a\
  supervised signal. The proposed approach is trained on up to 5.5 \
  billion words predicting 100,000 possible hashtags. As well as strong\
   performance on the hashtag prediction task itself, we show that its \
   learned representation of text (ignoring the hashtag labels) is useful\
    for other tasks as well. To that end, we present results on a document\
     recommendation task, where it also outperforms a number of baselines.
'''
summarizer(article)
# [{'summary_text': 'REF proposed a convolutional neural network 
# that learns feature representations for short textual posts 
# using hashtags as a supervised signal.'}]

```

To use our model further pretrained on paper titles:
```
from transformers import pipeline
summarizer = pipeline("summarization", model="yuningm/bart-large-citesum-title")

article = ''' We describe a convolutional neural network that learns\
 feature representations for short textual posts using hashtags as a\
  supervised signal. The proposed approach is trained on up to 5.5 \
  billion words predicting 100,000 possible hashtags. As well as strong\
   performance on the hashtag prediction task itself, we show that its \
   learned representation of text (ignoring the hashtag labels) is useful\
    for other tasks as well. To that end, we present results on a document\
     recommendation task, where it also outperforms a number of baselines.
'''
summarizer(article)
# [{'summary_text': 'Learning Text Representations from Hashtags using Convolutional Neural Networks'}]
```



## How to run (DIY)
We also provide the [dataset](https://drive.google.com/file/d/1ndHCREXGSPnDUNllladh9qCtayqbXAfJ/view?usp=sharing) and checkpoints pretrained on its [citation sentences](https://drive.google.com/drive/folders/1M76z4GDToTPEUzsQLfqKHP4p44t2tSls?usp=sharing) and [titles](https://drive.google.com/drive/folders/1Hr4EiMsmsQZb2HG4KF0jw4Anx9Ds8_Wp?usp=sharing) in Google Drive.

Check out example scripts under `script/` to see how to train/evaluate on different datasets.




