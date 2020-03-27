import pyPriceWatch

with open('list.txt') as f:
    line = f.readline()
    cnt = 1
    while line:
        # print(line)
        price = pyPriceWatch.call(line)
        print(price)
        print("")
        line = f.readline()