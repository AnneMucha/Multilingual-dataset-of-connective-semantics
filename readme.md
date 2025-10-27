# MultiCoS: A Multilingual Dataset of Connective Semantics with Context–Sentence Compatibility

This repository stores data in MultiCoS: A Multilingual Dataset of Connective Semantics with Context–Sentence Compatibility. Please refer to the associated paper (under review) for the description of the data as well as the data collection methodology.

## Basic repository structure

- `readme.md`  
- `language_files`  
  - lang1  
    - `lang1-metadata.yml`  
    - `lang1-examples.csv`  
    - `lang1-evidence.csv`  
    - `lang1-summary.csv`  
  - lang2  
    - `lang2-metadata.yml`  
    - `lang2-examples.csv`  
    - `lang2-evidence.csv`  
    - `lang2-summary.csv`  
  - lang3  
    - ...  
- `questionnaire`  
  - `connectives_questionnaire.csv`  
- `utilities`  
  - `generalization_checker.py`
  - `felicity_judgments_benchmark`
  - `merge.R`  
  - `merged_output_vertical.csv`  
  - `summarizer.py`

## Format of the CSV tables

The language file for each language consists of four files: **the metadata YAML file** and three CSV tables: **the examples table**, **the evidence table**, and **the summary table**. In a nutshell, the examples table lists all relevant example sentences while the evidence table records felicity judgements regarding the examples in the example table with respect to the contexts recorded in `connectives_questionnaire.csv`. The summary table summarizes the inventory of connectives in the language, with information about relevant semantic properties and morpho-syntactic of each connective element in the language.

### Summary table

Each row in a summary table records compatibility between a specific connective and a specific context type. The columns correspond to the following features of the connective full form or of the context type.

- `expression`: the core form of the connective expression;  
- `full_form`: the full form of the connective expression. Please refer to the associated paper for the distinction between the core form and the full form;  
- `shorthand`: the shorthand of the context type  
- `kboth`: in the relevant context type, the speaker believes both clauses;  
- `kneither`: in the relevant context type, the speaker believes neither clause;  
- `contrast`: in the relevant context type, there is a contrast between the clauses;  
- `stative`: in the relevant context type, the clauses describe states rather than dynamic events;  
- `negated_p`: the first clause has overt negation;  
- `Kp`: in the relevant context type, for either clause, the speaker believes its truth;  
- `question`: the sentence is a question;  
- `fc`: free choice inference is licensed;  
- `can_express`: the compatibility of the connective full form with the context type  
- `evidence`: reference to the pieces of evidence in the **evidence table** supporting the judgment in `can_express`  
- `negation`: whether the full form of the connective morpho-syntactically contains negation.  
  - `neither`: the full form does not contain negation;  
  - `above`: the full form appears syntactically above the coordination (as in NEG\[p *CONN* q\]);  
  - `below`: the full form appears syntactically below the coordination (as in \[NEG p *CONN* NEG q\]).

## Scripts

The repository contains several scripts for data manipulation and analysis.

- `utilities/merge.R`: merges all the summary tables with an additional column corresponding to the language name. It requires the relevant summary tables to be in the same directory.  
- `utilities/generalization_checker.py`: checks the below four cross-linguistic generalizations based on the merged summary table:  
  - The absence of lexicalized NAND;  
  - NOR is unlikely to be lexicalized as a morpho-logically simple connective;  
  - Juxtaposition without any irrealis marking cannot express disjunction (Mauri, 2008);  
  - There is no lexicalization for XOR. See Sect. 5.1 of the associated paper for discussion.  
- `utilities/summarizer.py`: creates a summary table (without the Negation column) for a language based on the questionnaire table, the example table, and the evidence table.  
- `utilities/felicity_judgments_benchmark`: This folder contains the data files and the R script used to compare the felicity judgments with those of GPT5 (discussed in Sect. 5.3 of the associated paper)

