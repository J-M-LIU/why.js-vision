from time import sleep
from variable import globalvar
def test():
    i=0;
    while True:
        globalvar.set_global_frame(i)
        # print("hah",globalvar.get_global_frame())
        i=i+1
        sleep(0.5)