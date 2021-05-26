# Validation set

- Using [tagtog.net](tagtog.net):
- our project: [https://www.tagtog.net/accordionmonkey/textmining-project/pool](https://www.tagtog.net/accordionmonkey/textmining-project/pool)

Questions:

- How should the validation dataset look like? What exactly is an annotation?

Example: "Sherlock entered the flat in Bakerstreet."

- Either
    - character: sherlock
    - location: Bakerstreet
- Or
    - character in sentence at index 0 to 7
    - location in sentence at index 29 to 39



## tagtog docs -> annotate with coreNLP command line tool

```
Annotation pipeline timing information:
TokenizerAnnotator: 0.2 sec.
WordsToSentencesAnnotator: 0.1 sec.
POSTaggerAnnotator: 0.9 sec.
MorphaAnnotator: 0.1 sec.
NERCombinerAnnotator: 11.4 sec.
TOTAL: 12.7 sec. for 3912 tokens at 309,0 tokens/sec.
Pipeline setup: 6.0 sec.
Total time for StanfordCoreNLP pipeline: 19.9 sec.
```