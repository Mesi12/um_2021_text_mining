STANFORD_CORENLP_HOME="../../libraries/stanford-corenlp-4.2.2/"

java -mx3g -cp "$STANFORD_CORENLP_HOME/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props 3a_corenlp.properties