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
__version__ = 1, 0, 'dev1'

import paramiko


def __init__(
        hostname: str,
        *,
        port=22,
        username=None,
        password=None,
        pkey=None,
        key_filename=None,
        timeout=None,
        allow_agent=None,
        look_for_keys=True,
        compress=False,
        sock=None,
        gss_auth=False,
        gss_kex=False,
        gss_deleg_creds=True,
        gss_host=None,
        banner_timeout=None,
        auth_timeout=None,
        gss_trust_dns=True,
        passphrase=None,
        disabled_algorithms=None,
        gname: str = None,
) -> 'GqylpySSH':
    """Get a GqylpySSH object.

    @param gname:
        Assigns the initialized GqylpySSH object to
        a variable in the current module, if not None.

    @return: GqylpySSH(**@param)
    """
    gobj = GqylpySSH(
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        pkey=pkey,
        key_filename=key_filename,
        timeout=timeout,
        allow_agent=allow_agent,
        look_for_keys=look_for_keys,
        compress=compress,
        sock=sock,
        gss_auth=gss_auth,
        gss_kex=gss_kex,
        gss_deleg_creds=gss_deleg_creds,
        gss_host=gss_host,
        banner_timeout=banner_timeout,
        auth_timeout=auth_timeout,
        gss_trust_dns=gss_trust_dns,
        passphrase=passphrase,
        disabled_algorithms=disabled_algorithms
    )

    if gname is not None:
        this = sys.modules[__name__]
        if not hasattr(this, '__default__'):
            this.__default__ = gobj
        setattr(this, gname, gobj)

    return gobj


class GqylpySSH(paramiko.SSHClient):

    def __init__(self, **params):
        super().__init__()
        self.connect(**params)
        self.params = params

    def __del__(self):
        self.close()

    def cmd(
            self,
            command: str,
            *,
            timeout: int = None,
            bufsize: int = None,
            get_pty: bool = None,
            env: dict = None
    ) -> 'Command':
        """
        @param command: A command string.
        @param timeout: Execute command timeout, default N.
        @param bufsize: Buffer size, default N.
        @param get_pty: Whether to enable pseudo-terminal, default False.
        @param env: A dictionary of environment variables.
                    Indication: The server may reject environment variables.
        """
        if command[-1] == '&':
            return self.cmd_async(
                command=command,
                timeout=timeout,
                bufsize=bufsize,
                get_pty=get_pty,
                env=env
            )
        _, stdout, stderr = self.exec_command(
            command=command,
            timeout=timeout,
            bufsize=bufsize,
            get_pty=get_pty,
            environment=env
        )
        return Command(command, stdout, stderr)

    def cmd_many(
            self,
            commands: 'Union[list, tuple]',
            *,
            timeout: int = None,
            bufsize: int = None,
            get_pty: bool = None,
            env: dict = None
    ) -> 'Generator':
        """
        @param commands: A commands tuple or list.
        @param timeout: Execute command timeout, default N.
        @param bufsize: Buffer size, default N.
        @param get_pty: Whether to enable pseudo-terminal, default False.
        @param env: A dictionary of environment variables.
                    Indication: The server may reject environment variables.
        """
        if isinstance(commands, list):
            yield from (self.cmd(
                command=c,
                timeout=timeout,
                bufsize=bufsize,
                get_pty=get_pty,
                env=env
            ) for c in commands)
        elif isinstance(commands, tuple):
            yield from (
                raise_if_command_exec_error(
                    self.cmd(
                        command=c,
                        timeout=timeout,
                        bufsize=bufsize,
                        get_pty=get_pty,
                        env=env
                    )
                ) for c in commands)
        else:
            raise TypeError

    def cmd_async(
            self,
            command: str,
            *,
            timeout: int = None,
            bufsize: int = None,
            get_pty: bool = None,
            env: dict = None
    ) -> 'threading.Thread':
        """
        @param command: A command string.
        @param timeout: Execute command timeout, default N.
        @param bufsize: Buffer size, default N.
        @param get_pty: Whether to enable pseudo-terminal, default False.
        @param env: A dictionary of environment variables.
                    Indication: The server may reject environment variables.
        """
        thread = threading.Thread(
            target=self.cmd,
            kwargs={
                'command': command,
                'timeout': timeout,
                'bufsize': bufsize,
                'get_pty': get_pty,
                'env': env
            },
            name=f'AsyncSSHCommand({command})',
            daemon=True
        )
        thread.start()
        return thread


class Command:

    def __init__(self, command: str, *a):
        self.command: str = command

    def raise_if_error(self):
        if not self.status:
            raise SSHCommandError(f'({self.command}) {self.output}')

    @property
    def status(self) -> bool:
        return True if command_exitcode == 0 else False

    @property
    def output(self) -> str:
        return process(command_output)

    @property
    def status_output(self) -> 'Tuple[bool, str]':
        return self.status, self.output

    @property
    def output_else_raise(self) -> str:
        self.raise_if_error()
        return self.output

    @property
    def output_else_define(self, define=None):
        return self.output if self.status else define

    def contain_string(self, string: str) -> bool:
        return string in self.output

    def output_if_contain_string_else_raise(self, string: str) -> str:
        if self.contain_string(string):
            return self.output
        raise SSHCommandError

    def table_output_to_dict(self, split: str = None) -> list:
        """Used to turn the command output result with a title
        into a dictionary, such as `kubectl get nodes`."""
        return table2dict(self.output_else_raise, split=split)


def cmd(
        command: str,
        *,
        timeout: int = None,
        bufsize: int = None,
        get_pty: bool = None,
        env: dict = None,
        gname: 'Union[str, GqylpySSH]' = None
) -> Command:
    """
    @param command: A command string.
    @param timeout: Execute command timeout, default N.
    @param bufsize: Buffer size, default N.
    @param get_pty: Whether to enable pseudo-terminal, default False.
    @param env: A dictionary of environment variables.
                Indication: The server may reject environment variables.
    @param gname: A GqylpySSH object or pointer to a GqylpySSH object.
    """
    return (gname or __default__).cmd(
        command=command,
        timeout=timeout,
        bufsize=bufsize,
        get_pty=get_pty,
        env=env
    )


def cmd_many(
        commands: 'Union[list, tuple]',
        *,
        timeout: int = None,
        bufsize: int = None,
        get_pty: bool = None,
        env: dict = None,
        gname: 'Union[str, GqylpySSH]' = None
) -> 'Generator':
    """
    @param commands: A commands tuple or list.
    @param timeout: Execute command timeout, default N.
    @param bufsize: Buffer size, default N.
    @param get_pty: Whether to enable pseudo-terminal, default False.
    @param env: A dictionary of environment variables.
                Indication: The server may reject environment variables.
    @param gname: A GqylpySSH object or pointer to a GqylpySSH object.
    """
    return (gname or __default__).cmd_many(
        commands=commands,
        timeout=timeout,
        bufsize=bufsize,
        get_pty=get_pty,
        env=env
    )


def cmd_async(
        command: str,
        *,
        timeout: int = None,
        bufsize: int = None,
        get_pty: bool = None,
        env: dict = None,
        gname: 'Union[str, GqylpySSH]' = None
) -> 'threading.Thread':
    """
    @param command: A command string.
    @param timeout: Execute command timeout, default N.
    @param bufsize: Buffer size, default N.
    @param get_pty: Whether to enable pseudo-terminal, default False.
    @param env: A dictionary of environment variables.
                Indication: The server may reject environment variables.
    @param gname: A GqylpySSH object or pointer to a GqylpySSH object.
    """
    return (gname or __default__).cmd_async(
        command=command,
        timeout=timeout,
        bufsize=bufsize,
        get_pty=get_pty,
        env=env
    )


__default__: GqylpySSH


class _______i________s________d_______d_______c_______:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gpack = sys.modules[__name__]
    gcode = globals()[f'g {__name__[7:]}']

    for gname in globals():
        if gname[0] != '_' and hasattr(gcode, gname):
            setattr(gpack, gname, getattr(gcode, gname))

    setattr(gpack, '__init__', gcode.__init__)


import threading
from typing import Union, Tuple, Generator
