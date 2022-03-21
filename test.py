import gqylpy_ssh as gssh
from gqylpy_ssh import Command

ssh = gssh.__init__(
    hostname='10.121.118.101',
    username='root',
    password='passw0rd',
    timeout=15,
)

x: Command = ssh.cmd('hostname', timeout=4)
print(x.status_output)
