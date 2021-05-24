# %%
from nltk.parse import CoreNLPParser
from nltk.sentiment.sentiment_analyzer import 
import json

core_nlp_server_url = "http://localhost:9000"
parser = CoreNLPParser(url=core_nlp_server_url)

properties = {
    'annotators': 'quote',
    'pipelineLanguage': 'en',
    'outputFormat': 'json'
}
sentence = """"My dear fellow," said Sherlock Holmes as we sat on either side of the fire in his lodgings at Baker Street, "life is infinitely stranger than anything which the mind of man could invent.""""
annotation = parser.api_call(sentence, properties=properties)


# %%
with open("annot.json", "w") as f:
    pretty = json.dumps(annotation, indent=4)
    f.write(pretty)

# %%
import nltk
nltk.__file__
# %%

# #########################################


import json

with open("../../libraries/a_case_of_identity.txt.json", "r") as f:
    data = json.load(f)

# %%
relations = []
for sentence in data['sentences']:
    if sentence['kbp']:
        relations.append(sentence['kbp'])
        print(f"{sentence['kbp']['']}")
# %%
