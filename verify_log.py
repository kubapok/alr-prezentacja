log = open('log', 'r').readlines()

ok = True

broadcasting_clients = 0
for line in log:
    if '------' in line:
        if broadcasting_clients != 1:
            ok = False
        broadcasting_clients = 0
    if 'broadcasting' in line:
        broadcasting_clients += 1


if ok:
    print('test passed')
else:
    print('test failed')
