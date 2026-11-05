# Puntuguese - A Corpus of Puns in Portuguese with Micro-editions

> [!IMPORTANT]
> **Recommended for new experiments: use the `pair_controlled` configuration on [Hugging Face Hub](https://huggingface.co/datasets/Superar/Puntuguese).**
> In the original splits, many puns and their micro-edited counterparts are in different splits, and this affects model evaluation, as discovered by [Sousa et al. (2026)](https://github.com/avelando/pun-detection-split-analysis). The `pair_controlled` configuration solves this by keeping each pair in the same split.
>
> ```python
> load_dataset("Superar/Puntuguese", "pair_controlled")
> ```

Puntuguese is a corpus of punning texts in Portuguese, including jokes in Brazilian and European Portuguese. The data has been manually gathered and curate according to our [guidelines](data/GUIDELINES.md). It also contains some layers of annotation:

- Every pun is classified as homophonic, homographic, both, or none according to their specific punning signs;
- The punning and alternative signs were made explicit for every joke;
- We also mark potentially problematic puns from an ethical perspective, so it is easier to filter them out if needed.

Additionally, every joke in the corpus has a non-humorous counterpart, obtained via micro-editing, to enable Machine Learning systems to be trained.

## 🤗 Hugging Face Hub

The dataset is also available in the [Hugging Face Hub](https://huggingface.co/datasets/Superar/Puntuguese).

```python
from datasets import load_dataset

ds = load_dataset("Superar/Puntuguese") # Uses the original splits
ds = load_dataset("Superar/Puntuguese", "pair_controlled") # Uses pair-preserving splits
```

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

```bibtex
@inproceedings{InacioEtAl2024,
    title = "Puntuguese: A Corpus of Puns in {P}ortuguese with Micro-edits",
    author = "In{\'a}cio, Marcio Lima  and
      Wick-Pedro, Gabriela  and
      Ramisch, Renata  and
      Esp{\'\i}rito Santo, Lu{\'\i}s  and
      Chacon, Xiomara S. Q.  and
      Santos, Roney  and
      Sousa, Rog{\'e}rio  and
      Anchi{\^e}ta, Rafael  and
      Goncalo Oliveira, Hugo",
    editor = "Calzolari, Nicoletta  and
      Kan, Min-Yen  and
      Hoste, Veronique  and
      Lenci, Alessandro  and
      Sakti, Sakriani  and
      Xue, Nianwen",
    booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.lrec-main.1167",
    pages = "13332--13343",
    abstract = "Humor is an intricate part of verbal communication and dealing with this kind of phenomenon is essential to building systems that can process language at large with all of its complexities. In this paper, we introduce Puntuguese, a new corpus of punning humor in Portuguese, motivated by previous works showing that currently available corpora for this language are still unfit for Machine Learning due to data leakage. Puntuguese comprises 4,903 manually-gathered punning one-liners in Brazilian and European Portuguese. To create negative examples that differ exclusively in terms of funniness, we carried out a micro-editing process, in which all jokes were edited by fluent Portuguese speakers to make the texts unfunny. Finally, we did some experiments on Humor Recognition, showing that Puntuguese is considerably more difficult than the previous corpus, achieving an F1-Score of 68.9{\%}. With this new dataset, we hope to enable research not only in NLP but also in other fields that are interested in studying humor; thus, the data is publicly available.",
}

```

If you use the dataset's pair-preserving version, please also cite [Sousa et al. (2026)](https://github.com/avelando/pun-detection-split-analysis):

**BibTeX:**

```bibtex
@inproceedings{SousaEtAl2026,
  title         = {When the Split Matters: Reorganizing Micro-Edited Pairs for Portuguese Pun Detection},
  author        = {Avelar Rodrigues de Sousa and Maykon Willyam de Sousa Ferreira and Victor Oliveira Lima Pontes and Rafael Torres Anchi\^{e}ta},
  booktitle     = {Anais do XXIII Encontro Nacional de Intelig\^{e}ncia Artificial e Computacional},
  location      = {Cuiab\'{a}/MT},
  year          = 2026,
  issn          = {2763-9061},
  pages         = {1792--1803},
  publisher     = {SBC},
  address       = {Porto Alegre, RS, Brasil},
  doi           = {10.5753/eniac.2026.31369},
  url           = {https://sol.sbc.org.br/index.php/eniac/article/view/46925}
}
```

**ACL:**

```
Avelar Rodrigues de Sousa, Maykon Willyam de Sousa Ferreira, Victor Oliveira Lima Pontes, and Rafael Torres Anchiêta. 2026. When the Split Matters: Reorganizing Micro-Edited Pairs for Portuguese Pun Detection. In Anais do XXIII Encontro Nacional de Inteligência Artificial e Computacional, pages 1792–1803, Porto Alegre, RS, Brasil. SBC.
```

