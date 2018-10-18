f = open('hs300.txt', 'r')
li=list()
for line in f:
    li.append(int(line.split('\n')[0]))

print(li)