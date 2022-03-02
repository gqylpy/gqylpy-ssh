"""
─────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─██████████████───████████──████████─██████─────────██████████████─████████──████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██───██░░░░██──██░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░██──██░░░░██─
─██░░██████████─██░░██████░░██───████░░██──██░░████─██░░██─────────██░░██████░░██─████░░██──██░░████─
─██░░██─────────██░░██──██░░██─────██░░░░██░░░░██───██░░██─────────██░░██──██░░██───██░░░░██░░░░██───
─██░░██─────────██░░██──██░░██─────████░░░░░░████───██░░██─────────██░░██████░░██───████░░░░░░████───
─██░░██──██████─██░░██──██░░██───────████░░████─────██░░██─────────██░░░░░░░░░░██─────████░░████─────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██████████───────██░░██───────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██───────────────██░░██───────
─██░░██████░░██─██░░██████░░████───────██░░██───────██░░██████████─██░░██───────────────██░░██───────
─██░░░░░░░░░░██─██░░░░░░░░░░░░██───────██░░██───────██░░░░░░░░░░██─██░░██───────────────██░░██───────
─██████████████─████████████████───────██████───────██████████████─██████───────────────██████───────
─────────────────────────────────────────────────────────────────────────────────────────────────────

Copyright © 2022 GQYLPY. 竹永康 <gqylpy@outlook.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys
import warnings
import threading
import functools

from paramiko import SSHClient, AutoAddPolicy
from paramiko.channel import ChannelFile, ChannelStderrFile

__default__: 'GqylpySSH'

gcode = sys.modules[__name__]
gpack = sys.modules[__name__[:-6]]


def __init__(hostname: str, *, gname: str = None, **params) -> 'GqylpySSH':
    gobj = GqylpySSH(hostname, **params)

    if gname is not None:
        if gname.__class__ is not str:
            x: str = gname.__class__.__name__
            raise TypeError(f'gname type must be a "str", not "{x}".')

        if not hasattr(gcode, '__default__'):
            gcode.__default__ = gobj

        setattr(gpack, gname, gobj)

    return gobj


class GqylpySSH(SSHClient):

    def __init__(self, hostname: str, **params):
        super().__init__()
        self.set_missing_host_key_policy(AutoAddPolicy())
        self.connect(hostname, **params)

    def __del__(self):
        self.close()

    def cmd(
            self,
            command: str,
            *,
            timeout: int = None,
            bufsize: int = -1,
            get_pty: bool = False,
            env: dict = None
    ) -> 'Command':
        if command.__class__ is not str:
            x: str = command.__class__.__name__
            raise TypeError(f'Parameter "command" type must be a "str", not "{x}".')
        if timeout is not None and timeout.__class__ not in (int, float):
            x: str = timeout.__class__.__name__
            raise TypeError(f'Parameter "timeout" type must be a "int" or "float", not "{x}".')
        if bufsize.__class__ not in (int, float):
            x: str = bufsize.__class__.__name__
            raise TypeError(f'Parameter "bufsize" type must be a "int" or "float", not "{x}".')
        if env is not None and env.__class__ is not dict:
            x: str = env.__class__.__name__
            raise TypeError(f'Parameter "env" type must be a "dict", not "{x}".')

        command: str = command.strip()

        if command[-1] == '&':
            return self.cmd_async(
                command=command,
                timeout=timeout,
                bufsize=bufsize,
                get_pty=get_pty,
                env=env
            )
        _, stdout, stderr = self.exec_command(
            command=f'{command} && echo 4289077',
            timeout=timeout,
            bufsize=bufsize,
            get_pty=get_pty,
            environment=env
        )
        return Command(command, stdout, stderr)

    def cmd_many(self, commands: (tuple, list), **kw) -> iter:
        if commands.__class__ is tuple:
            for c in commands:
                c: str = c.rstrip()
                if c[-1] == '&':
                    c = c[:-1]
                    warnings.warn(
                        'Note that running multiple commands '
                        'in tuple mode cannot use asynchrony "&".'
                    )
                co: Command = self.cmd(c, **kw)
                co.raise_if_error()
                yield co
        elif commands.__class__ is list:
            yield from (self.cmd(c, **kw) for c in commands)
        else:
            raise TypeError(
                'Parameter "commands" type must be a list or tuple. '
                'If list, execute command in order and return result list; '
                'If tuple, same as above, but next command is execute only '
                'when previous command is successfully executed.'
            )

    def cmd_async(self, command: str, **kw) -> threading.Thread:
        command: str = command.rstrip()

        if command[-1] == '&':
            command: str = command[:-1]

        thread = threading.Thread(
            target=self.cmd,
            kwargs={'command': command, **kw},
            name=f'AsyncSSHCommand({command})',
            daemon=True)
        thread.start()

        return thread


class Command:

    def __init__(self, command: str, stdout: ChannelFile, stderr: ChannelStderrFile):
        self.command = command
        self.stdout: bytes = stdout.read()
        self.stderr: bytes = stderr.read()

    def raise_if_error(self):
        if not self.status:
            raise SSHCommandError(f'({self.command}) {self.output}')

    @property
    def status(self) -> bool:
        return self.stdout[-9:] == b'\n4289077\n'

    @property
    def output(self) -> str:
        output: bytes = self.stdout[:-9] if self.status else self.stdout
        if self.stderr:
            join: bytes = b'; ' if self.stdout else b''
            output: bytes = self.stdout + join + self.stderr
        return output.decode()

    @property
    def status_output(self) -> tuple:
        return self.status, self.output

    @property
    def output_else_raise(self) -> str:
        if self.status:
            return self.output
        raise SSHCommandError(f'({self.command}) {self.output}')

    @property
    def output_else_define(self, define=None):
        return self.output if self.status else define

    def contain_string(self, string: str) -> bool:
        return string in self.output

    def output_if_contain_string_else_raise(self, string: str) -> str:
        if self.contain_string(string):
            return self.output
        raise SSHCommandError(f'({self.command}): "{self.output}"')

    def table_output_to_dict(self, split: str = None) -> list:
        return table2dict(self.output_else_raise, split=split)


def table2dict(table: str, *, split: str = None) -> list:
    result = [[value.strip() for value in line.split(split)]
              for line in table.splitlines()]
    keys = [key.lower() for key in result[0]]
    return [dict(zip(keys, values)) for values in result[1:]]


def gname2gobj(func):
    @functools.wraps(func)
    def inner(*a, gname: (str, GqylpySSH) = None, **kw):
        if gname is None:
            if not hasattr(gcode, '__default__'):
                raise RuntimeError('You did not create the default GqylpySSH object.')
            gobj: GqylpySSH = __default__
        elif gname.__class__ is str:
            gobj: GqylpySSH = getattr(gpack, gname, None)
            if gobj.__class__ is not GqylpySSH:
                raise NameError(f'gname "{gname}" not found in {gpack.__name__}.')
        elif gname.__class__ is GqylpySSH:
            gobj: GqylpySSH = gname
        else:
            x: str = gname.__class__.__name__
            raise TypeError(f'Parameter "gname" type must be a "str" or "GqylpySSH". not "{x}".')
        return func(*a, gobj=gobj, **kw)
    return inner


@gname2gobj
def cmd(command: str, *, gobj: GqylpySSH = None, **kw) -> Command:
    return gobj.cmd(command, **kw)


@gname2gobj
def cmd_many(commands: (tuple, list), *, gobj: GqylpySSH = None, **kw) -> list:
    return gobj.cmd_many(commands, **kw)


@gname2gobj
def cmd_async(command: str, *, gobj: GqylpySSH = None, **kw) -> threading.Thread:
    return gobj.cmd_async(command, **kw)


class SSHCommandError(Exception):
    __module__ = 'e'
