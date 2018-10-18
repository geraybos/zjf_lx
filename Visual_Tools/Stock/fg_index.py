
result=list()
with open('stoks.txt') as f:
    for line in f:
        result.append(str(line).replace('\n',''))


print(result)