# NLP Resources #

## IDP ##
(Beta) runs IDP on outcomes, finding association between linguistic features and a binary/categorical outcome.
Citation: Monroe et al. 2008 - Fightin' Words - Lexical Feature Selection and Evaluation for Identifying the Content of Political Conflict

## Lexica ##
Extract lexicon features from various lexica. Supported:
- LIWC 2007
- LIWC 2015
- NRC EmoLex v0.92

## Google 1billion LM ##
Use the `Google1BillionLM` directory.
run `python3 lm_1b/lm_1b_eval.py --mode eval2 ...` for getting perplexities written to a file
The file reads the entire line into the LM, so don't use csv, use plain text file.

