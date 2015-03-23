import csv

# loads file into dictionary
def load_data(infile):
    relations = {}
    with open(infile, 'rb') as tsvinfile:
        tsvin = csv.reader(tsvinfile, delimiter=',')
        for row in tsvin:
            relations[row[0]] = row[2]
    return relations

# word is in format LANGCODE: WORD
def get_origin(relations, word, path=False):
    # threshold to avoid loops, this is super hacky
    threshold = 5
    count = 0
    if not path:
        lookup = word
        #lookup = language + ': ' + word
        while lookup in relations and count < threshold:
            count += 1
            lookup = relations[lookup]
        return lookup
    else:
        lookup = [word]
        #lookup = [language + ': ' + word]
        while lookup[-1] in relations and count < threshold:
            count += 1
            lookup.append(relations[lookup[-1]])
        return lookup
            
# given a LANGUAGE: WORD origin string, gives all words which have that etymological origin at some point in their tree
# optional language filter: if given a string (language code), will filter results to only be of a certain language
def get_all_from_origin(relations, origin, language=None):
    cousins = []
    count = 0
    for word in relations:
        # if word is in any of the parent nodes, then count it
        if origin in get_origin(relations, word, True)[1:]:
            cousins.append(word)
    
    if language is not None:
        return [c for c in cousins if c.split(': ')[0] == language]
    return cousins

def get_cousins(relations, word, language=None):
    origin = get_origin(relations, word, path=False)
    cousins = get_all_from_origin(relations, origin, language=language)
    return [c for c in cousins if c != word]