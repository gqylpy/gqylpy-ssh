[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Release](https://img.shields.io/github/release/gqylpy/gqylpy-ssh.svg?style=flat-square")](https://github.com/gqylpy/gqylpy-ssh/releases/latest)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_ssh)](https://pypi.org/project/gqylpy_ssh)
[![License](https://img.shields.io/pypi/l/gqylpy_ssh)](https://github.com/gqylpy/gqylpy-ssh/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_ssh/month)](https://pepy.tech/project/gqylpy_ssh)

# gqylpy-ssh

> 在远程服务器执行命令并得到执行结果，它是对 paramiko 库的二次封装。在 `Command` 对象中，提供了多种方法用于判断命令执行结果是否如期。

<kbd>pip3 install gqylpy_ssh</kbd>

```python
>>> from gqylpy_ssh import GqylpySSH, Command

>>> ssh = GqylpySSH('192.168.1.7', 22, username='gqylpy', password=...)
>>> c: Command = ssh.cmd('echo Hi, GQYLPY')

>>> c.status_output
(True, 'Hi, GQYLPY')
```
