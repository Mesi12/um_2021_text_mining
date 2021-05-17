from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
import json


class CoreNLPHelper:
    
    def __init__(self, core_nlp_server_url):
        self.core_nlp_server_url = core_nlp_server_url
        # general parser for non-implemented features
        self.parser = CoreNLPParser(url=core_nlp_server_url)
        # Neural Dependency Parser
        self.dep_parser = CoreNLPDependencyParser(url=core_nlp_server_url)

    def is_sentence_passive(self, sentence) -> bool:
        """
        returns bool

        Uses dep parser to identify whether a sentence has passive dependencies.
        Then it is considered in passive writing style.
        """
        parses = self.dep_parser.parse(sentence.split())
        for parse in parses:
            for governor, dep, dependent in parse.triples():
                if dep.endswith(":pass"):
                    return True
        return False

    def get_sentiment_value(self, sentence) -> int:
        """
        returns integer sentiment value 0-4 (negative to positive)
        """
        properties = {
            'annotators': 'sentiment',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }
        annotation = self.parser.api_call(sentence, properties=properties)
        
        # in case of multiple sentences, just returning the first to avoid issues.
        # returns a value from 0-4
        return int(annotation['sentences'][0]['sentimentValue'])

    def get_sentiment_distribution(self, sentence) -> list:
        """
        returns a list of sentiment distributions from negative to positive.
        """
        properties = {
            'annotators': 'sentiment',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }
        annotation = self.parser.api_call(sentence, properties=properties)
        
        # in case of multiple sentences, just returning the first to avoid issues.
        return annotation['sentences'][0]['sentimentDistribution']

    def get_coreferences(self, sentence) -> json:
        """
        return json object of coreference entities as is.
        """
        properties = {
            'annotators': 'coref',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
            }
        annotation = self.parser.api_call(sentence, properties=properties)
        return annotation['corefs']
