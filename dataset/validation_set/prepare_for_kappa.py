import os
import random
import re
import nltk

# todo  how should the final validation set look like?
#       i.e. how will we use it later on?


if __name__ == "__main__":

    with open("../original/novels/stud.txt") as fp:
        data = fp.read()

    data = data.replace("\n", " ")
    data = re.sub(r" +", " ", data)
    sent = nltk.tokenize.sent_tokenize(data)

    random.Random().shuffle(sent)

    with open("./validation_set.txt", "w") as fp:
        for item in sent[:10]:
            fp.write(f"{item}\n")