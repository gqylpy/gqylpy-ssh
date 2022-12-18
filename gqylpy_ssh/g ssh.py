"""
Copyright (c) 2022 GQYLPY <http://gqylpy.com>. All rights reserved.

This file is part of gqylpy-ssh.

gqylpy-ssh is free software: you can redistribute it and/or modify it under the
terms of the GNU Lesser General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

gqylpy-ssh is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with gqylpy-ssh. If not, see <https://www.gnu.org/licenses/>.
"""
import sys
import builtins
import warnings
import functools
import threading

import paramiko

from paramiko import SSHClient
from paramiko import AutoAddPolicy

from paramiko.ssh_exception import SSHException
from paramiko.ssh_exception import NoValidConnectionsError

from paramiko.channel import ChannelFile
from paramiko.channel import ChannelStderrFile

first: 'GqylpySSH'

gpack, gcode = sys.modules[__package__], sys.modules[__name__]


def __init__(
        hostname: str,
        port:     int,
        *,
        gname:    str = None,
        **params
) -> 'GqylpySSH':
    gobj = GqylpySSH(hostname, port, **params)

    if gname is None:
        return gobj

    if gname.__class__ is not str:
        x: str = gname.__class__.__name__
        raise TypeError(f'gname type must be "str", not "{x}".')

    if not hasattr(gcode, 'first'):
        gcode.first = gobj

    setattr(gpack, gname, gobj)


class GqylpySSH(SSHClient):

    def __init__(self, hostname: str, port: int, **params):
        SSHClient.__init__(self)
        self.set_missing_host_key_policy(AutoAddPolicy())

        key_filename: str = params.get('key_filename')
        key_password: str = params.pop('key_password', None)

        if key_filename is not None and key_password is not None:
            pkey = paramiko.RSAKey.from_private_key_file(
                key_filename, key_password)
            del params['key_filename']
        else:
            pkey = None

        self.command_timeout: int  = params.pop('command_timeout', None)
        self.auto_sudo:       bool = params.pop('auto_sudo', False)
        self.reconnect:       bool = params.pop('reconnect', False)

        self.connect(hostname, port, **params, pkey=pkey)

        params['pkey'] = pkey
        self.hostname  = hostname
        self.params    = params

    def __del__(self):
        try:
            self.close()
        except AttributeError:
            pass

    def cmd(
            self,
            command: str,
            *,
            timeout: int  = None,
            bufsize: int  = -1,
            get_pty: bool = False,
            env:     dict = None
    ) -> 'Command':
        if command.__class__ is not str:
            x: str = command.__class__.__name__
            raise TypeError(
                f'parameter "command" type must be a "str", not "{x}".'
            )
        if timeout is not None and timeout.__class__ not in (int, float):
            x: str = timeout.__class__.__name__
            raise TypeError(
                'parameter "timeout" type must '
                f'be a "int" or "float", not "{x}".'
            )
        if bufsize.__class__ not in (int, float):
            x: str = bufsize.__class__.__name__
            raise TypeError(
                f'parameter "bufsize" type must '
                f'be a "int" or "float", not "{x}".'
            )
        if env is not None and env.__class__ is not dict:
            x: str = env.__class__.__name__
            raise TypeError(
                f'parameter "env" type must be a "dict", not "{x}".'
            )

        command: str = command.strip()

        if command[-1] == '&':
            return self.cmd_async(
                command=command,
                timeout=timeout,
                bufsize=bufsize,
                get_pty=get_pty,
                env=env
            )

        if self.auto_sudo and not command.startswith('sudo '):
            command = f'sudo {command}'

        command += '&& echo 4289077'
        timeout = timeout or self.command_timeout

        try:
            _, stdout, stderr = self.exec_command(
                command=command,
                timeout=timeout,
                bufsize=bufsize,
                get_pty=get_pty,
                environment=env
            )
        except (SSHException, ConnectionResetError) as e:
            if not self.reconnect:
                raise e
            try:
                self.connect(self.hostname, **self.params)
            except (TimeoutError, NoValidConnectionsError):
                raise e
            else:
                _, stdout, stderr = self.exec_command(
                    command=command,
                    timeout=timeout,
                    bufsize=bufsize,
                    get_pty=get_pty,
                    environment=env
                )

        return Command(command, stdout, stderr)

    def cmd_many(self, commands: (tuple, list), **kw):
        if commands.__class__ is tuple:
            for c in commands:
                c: str = c.rstrip()
                if c[-1] == '&':
                    c = c[:-1]
                    warnings.warn(
                        'note that running multiple commands '
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
            name  =f'AsyncSSHCommand({command})',
            daemon=True
        )
        thread.start()

        return thread


class Command:

    def __init__(
            self,
            command: str,
            stdout:  ChannelFile,
            stderr:  ChannelStderrFile
    ):
        self.command = command
        self.stdout: bytes = stdout.read()
        self.stderr: bytes = stderr.read()

    def raise_if_error(self):
        if not self.status:
            raise SSHCommandError(f'({self.command}) {self.output}')

    @property
    def status(self) -> bool:
        return self.stdout[-8:] == b'4289077\n'

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

    def output_else_raise(self) -> str:
        if self.status:
            return self.output
        raise SSHCommandError(f'({self.command}) {self.output}')

    def output_else_define(self, define=None):
        return self.output if self.status else define

    def contain(self, string: str) -> bool:
        return string in self.output

    def contain_string_else_raise(self, string: str):
        if string not in self.output:
            raise SSHCommandError(f'({self.command}): "{self.output}"')

    def output_if_contain_string_else_raise(self, string: str) -> str:
        output = self.output
        if string in output:
            return output
        raise SSHCommandError(f'({self.command}): "{self.output}"')

    def table2dict(self, *, split: str = None):
        lines = (
            line.split(split) for line in self.output_else_raise().splitlines()
        )
        titles = tuple(next(lines))
        return (dict(zip(titles, line)) for line in lines)

    def line2list(self, *, split: str = None):
        yield from (
            line.split(split) for line in self.output_else_raise().splitlines()
        )


def gname2gobj(func):
    @functools.wraps(func)
    def inner(*a, gname: (str, GqylpySSH) = None, **kw):
        if gname is None:
            if not hasattr(gcode, 'first'):
                raise RuntimeError(
                    'you did not create the default GqylpySSH instance.'
                )
            gobj: GqylpySSH = first
        elif gname.__class__ is str:
            gobj: GqylpySSH = getattr(gpack, gname, None)
            if gobj.__class__ is not GqylpySSH:
                raise NameError(
                    f'gname "{gname}" not found in {gpack.__name__}.'
                )
        elif gname.__class__ is GqylpySSH:
            gobj: GqylpySSH = gname
        else:
            x: str = gname.__class__.__name__
            raise TypeError(
                'parameter "gname" type must be a '
                f'str or GqylpySSH instance. not "{x}".'
            )
        return func(*a, gobj=gobj, **kw)
    return inner


@gname2gobj
def cmd(command: str, *, gobj: GqylpySSH = None, **kw) -> Command:
    return gobj.cmd(command, **kw)


@gname2gobj
def cmd_many(commands: (tuple, list), *, gobj: GqylpySSH = None, **kw):
    return gobj.cmd_many(commands, **kw)


@gname2gobj
def cmd_async(
        command: str, *, gobj: GqylpySSH = None, **kw
) -> threading.Thread:
    return gobj.cmd_async(command, **kw)


class SSHCommandError(Exception):
    __module__ = 'builtins'


builtins.SSHCommandError = SSHCommandError
