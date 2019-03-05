from users import *

def apply():
    for i in range(1,5):
        for j in range((i-1)*10+1,i*10+1):
            apply_job(j,i)
apply()
