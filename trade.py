from system import *

def set_max_percent(value):
    file_name="percent"
    save_picke(file_name,value)

def get_max_percent():
    value=0
    file_name="percent"
    if is_pickle(file_name):
        value=load_pickle(file_name)
    return value




if __name__ == "__main__":
    print("trade")