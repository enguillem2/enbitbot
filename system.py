import os

import pickle

path="/home/guillem/python/enbitbot"
print(f"PATH::: {path}")
def save_picke(file_name,value):
    file=f"{path}/data/_{file_name}"
    pickle.dump(value,open(file,"wb"))

def load_pickle(file_name):
    file=f"{path}/data/_{file_name}"
    print(file)
    if os.path.isfile(file):
        value_saved=pickle.load(open(file,"rb"))
        return value_saved
    else:
        return 0
    
def is_pickle(file_name):
    file=f"{path}/data/_{file_name}"
    return os.path.isfile(file)


if __name__ == "__main__":
    print("trade")