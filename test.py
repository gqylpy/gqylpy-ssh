import gqylpy_ssh as gssh

ssh = gssh.__init__(
    hostname='192.168.1.7',
    username='gqylpy',
    password=...,
    timeout=15
)

x = ssh.cmd('hostname', timeout=4)
print(x.status_output)
