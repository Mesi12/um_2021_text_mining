# running from this folder

## preconditions

- Execute below commands from this folder in your terminal.
- It requires the stanford coreNLP files in this git repository under: libraries/stanford-corenlp-4.2.2/

## running from this folder

ONCE: First execute following command, to save the path to the coreNLP library into a variable:

```bash
STANFORD_CORENLP_HOME="../libraries/stanford-corenlp-4.2.2/"
```

Afterwards this can be executed by changing the property file's content and the input file (here: example.txt).

```bash
java -mx4g -cp "$STANFORD_CORENLP_HOME/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props corenlp.properties -file example.txt

# or a story

java -mx4g -cp "$STANFORD_CORENLP_HOME/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props corenlp.properties -file "../../dataset/processed/stories/1_the_adventures_of_sherlock_holmes/a_case_of_identity.txt"
```

Meaning:

- `-mx4g` gives 4GB of RAM. Try to change if necessary.
- `-cp "$STANFORD_CORENLP_HOME/*" edu.stanford.nlp.pipeline.StanfordCoreNLP` the java class path. don't change.
- `-props corenlp.properties` the properties file.
- `-file example.txt` the input file.


## output

The java code will create a "<input-file-name>.json" in this folder.


## duration of NER task

**stories/1_the_adventures_of_sherlock_holmes with coref & quote & kbp:**

```
Annotation pipeline timing information:
TokenizerAnnotator: 0.9 sec.
WordsToSentencesAnnotator: 0.2 sec.
POSTaggerAnnotator: 13.2 sec.
MorphaAnnotator: 0.7 sec.
DependencyParseAnnotator: 96.4 sec.
NERCombinerAnnotator: 154.4 sec.
CorefAnnotator: 719.5 sec.
QuoteAnnotator: 58.1 sec.
KBPAnnotator: 188.8 sec.
TOTAL: 1232.2 sec. for 127403 tokens at 103,4 tokens/sec.
Pipeline setup: 30.3 sec.
Total time for StanfordCoreNLP pipeline: 1273.5 sec.
```

**all stories and novels up until ner:**

```
Annotation pipeline timing information:
TokenizerAnnotator: 1.6 sec.
WordsToSentencesAnnotator: 0.5 sec.
POSTaggerAnnotator: 38.4 sec.
MorphaAnnotator: 1.8 sec.
NERCombinerAnnotator: 96.2 sec.
TOTAL: 138.6 sec. for 797063 tokens at 5752,0 tokens/sec.
Pipeline setup: 4.1 sec.
Total time for StanfordCoreNLP pipeline: 154.7 sec.
```