import gqylpy_ssh as gssh

ssh = gssh.__init__(
    hostname='10.121.118.101',
    username='root',
    timeout=15
)

x = ssh.cmd('hostname', timeout=4)
print(x.status_output)
