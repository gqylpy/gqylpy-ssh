from gqylpy_ssh import GqylpySSH, Command

ssh = GqylpySSH('192.168.1.7', 22, username='gqylpy', password=...)

c: Command = ssh.cmd('echo Hi, GQYLPY')
print(c.status_output)
