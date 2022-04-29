[<img alt="LOGO" src="http://www.gqylpy.com/static/img/favicon.ico" height="21" width="21"/>](http://www.gqylpy.com)
[![Version](https://img.shields.io/pypi/v/gqylpy_ssh)](https://pypi.org/project/gqylpy_ssh/)
[![Python Versions](https://img.shields.io/pypi/pyversions/gqylpy_ssh)](https://pypi.org/project/gqylpy_ssh)
[![License](https://img.shields.io/pypi/l/gqylpy_ssh)](https://github.com/gqylpy/gqylpy_ssh/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/gqylpy_ssh/month)](https://pepy.tech/project/gqylpy_ssh)

本程序使用了 paramiko 库，这个库是基于 LGPL 协议发布的。

> 在远程服务器执行命令并得到命令结果，它是对 paramiko 库的二次封装。通过 `Command` 对象，你可以得到这条命令的执行结果，状态等信息。

<kbd>pip3 install gqylpy_ssh</kbd>

首先初始化 `GqylpySSH` 实例：
```python
import gqylpy_ssh as gssh

gssh.__init__(
    hostname='192.168.1.100',
    username='gqylpy',
    password=...
)
```

通过 `cmd` 函数在远程服务器执行命令，它返回一个 `Command` 对象：
```python
c = gssh.cmd('hostname')
```

若命令执行失败，调用此方法将抛出异常：
```python
c.raise_if_error()
```

获得命令状态或输出：
```python
status: bool = c.status
output: str = c.output
status, output = c.status_output
```

获得命令输出，若命令执行错误，将抛出异常
```python
output: str = c.output_else_raise
```

获得命令输出，若命令执行错误，将返回 "define value"：
```python
output: str = c.output_else_define('define value')
```

检查命令输出是否包含某个字符串，得到一个布尔值：
```python
x: bool = c.contain_string('string')
```

获得命令输出，如果输出包含某个字符串，否则抛出异常：
```python
output: str = c.output_if_contain_string_else_raise('string')
```

这个方法可将带有标题的输出转为字典：
```python
it = c.output2dict('kubectl get nodes')
```
___

如果你需要创建多个 `GqylpySSH` 实例：
```python
from gqylpy_ssh import GqylpySSH, Command

ssh = GqylpySSH('192.168.1.100', **params)
c: Command = ssh.cmd('hostname')
output: str = c.output_else_raise
```

```python
import gqylpy_ssh as gssh

gssh.__init__('192.168.1.100', **params, gname='1.100')
gssh.__init__('192.168.1.200', **params, gname='1.200')

output: str = gssh.cmd('hostname', gname='1.100').output_else_raise
output: str = gssh.cmd('hostname', gname='1.200').output_else_raise

gssh.cmd('hostname').output == gssh.cmd('hostname', gname='1.100').output
```
