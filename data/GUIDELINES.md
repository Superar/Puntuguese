# Guidelines for the corpus collection

This corpus will bear short punning texts in Portuguese, regardless of the language variety. The collection will occur online and manually from different websites, social media, videos, other related corpora, and books. All sources are listed in the [SOURCES.md](./SOURCES.md) file.

This document aims at defining the guidelines to be followed during the data collection process.

## 1. Textual format

- All texts should have one to two sentences;
- The sentences can be of any kind: affirmatives, questions, exclamations, etc.;
- The texts can be in the form of riddles;
- The texts **should not** contain any kind of dialogue between characters;
- The texts **should not** contain a narrative arc, or tell a story;
- The whole focus of the text should be the pun in question according to its definition.

## 2. Definition of pun

The working definition of pun for this work is the one presented by Miller et al. (2017); it reads as follows:

> "A pun is a form of wordplay in which one sign (e.g., a word or phrase) suggests two or more meanings by exploiting polysemy, homonymy, or phonological similarity to another sign, for an intended humorous or rhetorical effect."

Every selected pun must satisfy this definition. Some hints for the collection are:

- A sign can be a single word (or token), a phrase (a sequence of tokens), or a part of a word (a subtoken);
- The humorous effect must rely on the ambiguity of said sign;
- The ambiguity must originate from the word's form (written or spoken);
- Every pun must have a "pun word" (the ambiguous sign that is in the text) and an "alternative word" (the sign's ambiguous interpretation) identified. If it is not possible to identify both, the text is not considered a pun and should not be included.

## 3. Taxonomy of puns

The puns are to be classified according to the taxonomy defined by Hempelmann and Miller (2017):

- Homograph vs. Heterograph $\rightarrow$ Wheter the pun word and the alternative word are written the same;
- Homophone vs. Heterophone $\rightarrow$ Wheter the pun word and the altenative word are pronounced the same.

Since the homo\* and hetero\* categories are mutually exclusive to each other, in this corpus only the homo\* classifications will be used. **Every text should have both markups with either true or false values**, according to the formatting presented next.

## 4. Corpus format

The corpus will be made available using the JSON format. Each text is an object in the corpus array with three members: `id`, `text`, and `signs`.

The `id` member should receive a nummerical identifier in the format `document.count`: indicating the `document` number in [SOURCES.md](./SOURCES.md) and a count starting at `1` indicating the number of texts originating from that specific document.

The `text` member should contain the pun text in a single line.

The `signs` member is a list that represents each punning sign in the `text`. Usually the joke will have one single punning element, but there are cases with more than one source of punning humor. This list contains dictionaries with the following members: `homograph`, `homophone`, `pun sign`, and `alternative sign`.

The `homograph` and `homophone` members are to receive a boolean value `true` or `false`, according to the taxonomy defined before, representing the relations existing .

The `pun sign` member contains the sign in the text that creates the pun, as defined in section 2. This should be a string taken directly from the text in all lowercase, except with proper nouns and acronyms.

Conversely, the `alternative sign` will bear its ambiguous counterparts that are evoked through the polyssemy, homonymy and phonological relations according to the working definition of punning humor used in this work. As there can be multiple meanings on this matter, this member is a list of lowercased (with exception of proper nouns and acronyms) strings.

Some recent authors explicit the usage of idioms in puns. In such cases, in which the joke comes from a literal interpretation of the idiom, both `pun sign` and `alternative sign` must bear the whole idiom.

An example of this JSON structure, with some instances from the corpus, is shown below:

```JSON
[
    {
        "id": "1.1",
        "text": "Deve ser difícil ser professor de natação. Você ensina, ensina, e o aluno nada.",
        "signs": [
            {
                "homograph": true,
                "homophone": true,
                "pun sign": "nada",
                "alternative sign": ["nada"]
            }
        ]
    },
    {
        "id": "4.179",
        "text": "Que nome se dá a um grupo de lobos numa loja de telemóveis? Alcatéis.",
        "signs": [
            {
                "homograph": false,
                "homophone": false,
                "pun sign": "alcatéis",
                "alternative sign": ["Alcatel", "alcateia"]
            }
        ]
    },
    {
        "id": "4.185",
        "text": "Estão duas sapateiras num aquário, uma espirra e a outra diz: Santola!",
        "signs": [
            {
                "homograph": true,
                "homophone": true,
                "pun sign": "sapateiras",
                "alternative sign": ["sapateiras"]
            },
            {
                "homograph": false,
                "homophone": false,
                "pun sign": "santola",
                "alternative sign": ["santinho"]
            }
        ]
    }
]
```
