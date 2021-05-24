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