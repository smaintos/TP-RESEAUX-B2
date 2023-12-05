import time


start = time.time()

def count ():
    for i in range(10):
        print(i)
        time.sleep(0.5)

count()
count()
end = time.time()
print(end - start)
