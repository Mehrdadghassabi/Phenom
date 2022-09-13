from __future__ import unicode_literals
from hazm import *
import sys

sentence=sys.argv[1]
normalizer=Normalizer()
tagger = POSTagger(model='resources/postagger.model')
r=tagger.tag(word_tokenize(normalizer.normalize(sentence)))
stemmer=Stemmer()
result=""
for t in r:
    if(t[1]=='PRO'):
        if(t[0]=="تو"):
            result+="من "
        elif(t[0]=="من"):
            result+="تو "
    elif(t[1]=='V'):
        if(t[0][len(t[0])-1]=="ی"):
            result+=(t[0][:len(t[0])-1]+"م ")
        elif(t[0][len(t[0])-1]=="م"):
            result+=(t[0][:len(t[0])-1]+"ی ")
    elif(t[1]=='N'):
        if(t[0]!=stemmer.stem(t[0])):
            if(t[0][len(t[0])-1]=="ت"):
                result+=(t[0][:len(t[0])-1]+"م ")
            elif(t[0][len(t[0])-1]=="م"):
                result+=(t[0][:len(t[0])-1]+"ت ") 
        else:
            result+=(t[0]+" ")
    else:
        result+=(t[0]+" ")
print(result)




