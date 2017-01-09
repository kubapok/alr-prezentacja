import os

log = list()
dir_list = os.listdir()

for i in range(1,20):
    if  str(i) in dir_list:
        log.extend(open(str(i), 'r').readlines())

log = sorted(log)

clients = list()
l = open('log', 'w+')
for i in log:
    client = i[16]
    print(client)
    l.write(i)
    if client in clients:
        c = 0
        l.write('-'*40+'\n')
        print('-'*40)
        clients = list()
    clients.append(i[16])
# import pdb; pdb.set_trace()
