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
"""
__version__ = 1, 0, 'dev4'

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
    """Get a GqylpySSH instance.

    @param gname:
        Create a pointer to the GqylpySSH instance
        in the gqylpy_ssh module, if not None.

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

    if not hasattr(gpack, '__first__'):
        gpack.__first__ = gobj

    if gname is not None:
        setattr(gpack, gname, gobj)

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

    def output_else_define(self, define=None):
        return self.output if self.status else define

    def contain_string(self, string: str) -> bool:
        return string in self.output

    def output_if_contain_string_else_raise(self, string: str) -> str:
        if self.contain_string(string):
            return self.output
        raise SSHCommandError

    def output2dict(self, split: str = None) -> 'Generator':
        """Used to turn the command output result with a title
        into a dictionary, such as `kubectl get nodes`."""
        return table2dict(self.output_else_raise, split=split)


def gname2gobj(func):
    def inner(*a, gname: 'Union[str, GqylpySSH]' = None, **kw) -> Command:
        if gname is None:
            gobj: GqylpySSH = __first__
        elif gname.__class__ is str:
            gobj: GqylpySSH = getattr(gpack, gname)
        elif gname.__class__ is GqylpySSH:
            gobj: GqylpySSH = gname
        else:
            raise TypeError
        return func(*a, gname=gobj, **kw)
    return inner


@gname2gobj
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
    @param gname: GqylpySSH instance or pointer name of GqylpySSH instance.
    """
    return (gname or __first__).cmd(
        command=command,
        timeout=timeout,
        bufsize=bufsize,
        get_pty=get_pty,
        env=env
    )


@gname2gobj
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
    @param gname: GqylpySSH instance or pointer name of GqylpySSH instance.
    """
    return (gname or __first__).cmd_many(
        commands=commands,
        timeout=timeout,
        bufsize=bufsize,
        get_pty=get_pty,
        env=env
    )


@gname2gobj
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
    @param gname: GqylpySSH instance or pointer name of GqylpySSH instance.
    """
    return (gname or __first__).cmd_async(
        command=command,
        timeout=timeout,
        bufsize=bufsize,
        get_pty=get_pty,
        env=env
    )


import sys
import threading
from typing import Union, Tuple, Generator

__first__: GqylpySSH
gpack = sys.modules[__name__]


class ______歌______琪______怡______玲______萍______云______:
    __import__(f'{__name__}.g {__name__[7:]}')
    gcode = globals()[f'g {__name__[7:]}']

    for gname in globals():
        if gname[0] != '_' and hasattr(gcode, gname):
            setattr(gpack, gname, getattr(gcode, gname))

    setattr(gpack, '__init__', gcode.__init__)
