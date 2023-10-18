# Puntuguese data

The public data of the Puntuguese corpus is organized as follows:

```
data
├───split_annotation [Folder with micro-edited instances]
├───GUIDELINES.md [Guidelines used during the gathering process]
├───problematic.json [List of IDs for potentially problematic puns]
├───puns.csv [Corpus in CSV format - Easier to import in to a spreadsheet]
├───puns.json [Corpus in JSON format - Used originally in during gathering]
└───SOURCES.md [List of sources used during gathering]
```

Some observations about the corpus:

- The number of the source in `SOURCES.md` is used in the first part of each pun's ID, so it is easier to retrieve the source of each text. E.g. puns from UTC will always be in the form `5.XXXX`.

- The files `puns.csv` and `puns.json` have only the positive (humorous) instances collected following the `GUIDELINES.md`. The negative instances (from the micro-edition process) are in `split_annotation`. It can be converted into a more tractable CSV file using the script in `puntuguese/utils/create_classification_corpus.py`.
