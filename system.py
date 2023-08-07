import os

import pickle


def save_picke(file_name,value):
    file=f"data/_{file_name}"
    pickle.dump(value,open(file,"wb"))

def load_pickle(file_name):
    file=f"data/_{file_name}"
    if os.path.isfile(file):
        value_saved=pickle.load(open(file,"rb"))
        return value_saved
    else:
        return 0
    
def is_pickle(file_name):
    file=f"data/_{file_name}"
    return os.path.isfile(file)


if __name__ == "__main__":
    print("trade")