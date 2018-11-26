import pymongo
import numpy as np
from nltk import word_tokenize

def username(first,last,domain):
    first=first.lower()
    last=last.lower()
    user_patterns = [ first+last,
                    last+first,
                    first+'.'+last,
                    last+'.'+first,
                    first+'_'+last,
                    last+'_'+first,
                    first[0]+last,
                    last[0]+first,
                    first+last[0],
                    last+first[0],
                    first[0]+'.'+last,
                    last[0]+'.'+first,
                    first[:3]+last[:2],
                    last[:3]+first[:2],
                    last+first[:3],
                    first+last[:3] ]

    email_patterns= []
    for patn in user_patterns:
        email_patterns.append(patn+'@'+domain)
    #print(email_patterns)
    return email_patterns
