# Puntuguese - A Corpus of Puns in Portuguese with Micro-editions

Puntuguese is a corpus of punning texts in Portuguese, including jokes in Brazilian and European Portuguese. The data has been manually gathered and curate according to our [guidelines](data/GUIDELINES.md). It also contains some layers of annotation:

- Every pun is classified as homophonic, homographic, both, or none according to their specific punning signs;
- The punning and alternative signs were made explicit for every joke;
- We also mark potentially problematic puns from an ethical perspective, so it is easier to filter them out if needed.

Additionally, every joke in the corpus has a non-humorous counterpart, obtained via micro-editing, to enable Machine Learning systems to be trained.

## General statistics

The general statistics of the corpus are:

|    Language variety    |   Number of puns   |
| ---------------------- | -----------------  |
|  Brazilian Portuguese  |       4,106        |
|  European Portuguese   |         797        |
|        **Total**       |       4,903        |

Regarding the pun types, the statistics are:

|           Type of pun           | Quantity |
| ------------------------------- | -------- |
|          Only homophonic        |    953   |
|         Only homographic        |     10   |
| Both homophonic and homographic |    672   |
| Not homophonic nor homographic  |  3,352   |
|        Problematic jokes        |    106   |

## Repository organization

This repository contains all the data and experiments for the Puntuguese corpus of puns in Portuguese. The repository is organized as follows:

```
Puntuguese
├───data [Corpus and annotation files]
├───experiments [Scripts for Humor Recognition and Clustering analysis]
├───gathering [Corpus creation interface]
├───humicroedit [Pun editing interface]
├───results [Humor Recognition results]
└───utils [Utility scripts]
```

Each subfolder contains its own README file with general instructions on how to run the interfaces or annotation guidelines.

## How to cite

```
to be determined
```
