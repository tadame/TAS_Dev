import itertools
sel = ["polo", "pola", "Polos", "porloquesea"]
#sel = ["polo", "pola", "Polos", "porloquesea", "caramba"] # To be implemented future developments


def set_lenght(selection_list):
    """ Gimme the list and I will give you the minim lenght.
    """
    lenght = 0
    max_len = 0
    for item in sel:
        item_len = len(item)
        if max_len == 0:
            max_len = item_len
        else:
            if item_len <= max_len:
                max_len = item_len
    return max_len


def compare_items():
    max_len = set_lenght(sel)
    for item in sel:
        print item, max_len


#compare_items()
#===============================================================================
## Importing
import pymel.core as pm
import maya.cmds  as mc

#sel = pm.ls(sl=1)
sel = ['pSphere1', 'pSphere2', 'pSphere3', 'pSphe4', 'pSphere5', 'pSphere6']

for item in sel:
    print item

b = zip(*sel)
preffix = []
for x in b:
    capitalize = any(y.isupper() for y in x)
    letter_tuple = map(lambda y:y.lower(),x)
    char_tuple = list(set(letter_tuple))
    if len(char_tuple) == 1:
        if capitalize:
            preffix.append(char_tuple[0].upper())
        else:
            preffix.append(char_tuple[0])
    else:
        break

print preffix
result = "".join(preffix)
print result

### "pSphe"



