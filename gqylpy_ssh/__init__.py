"""
Execute the command on the remote ssh server and get the result, it is secondary
encapsulation the `paramiko` library. In the `Command` object, multiple methods
are provided to determine whether the execution result of the command is as
expected.

    >>> from gqylpy_ssh import GqylpySSH, Command
    >>> ssh = GqylpySSH('192.168.1.7', 22, username='gqylpy', password=...)
    >>> c: Command = ssh.cmd('echo Hi, GQYLPY')
    >>> c.status_output
    (True, 'Hi, GQYLPY')

    @version: 1.2.1
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/gqylpy-ssh

────────────────────────────────────────────────────────────────────────────────
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
import paramiko


def __init__(
        hostname:        str,
        port:            int  = 22,
        *,
        username:        str  = None,
        password:        str  = None,
        key_filename:    str  = None,
        key_password:    str  = None,
        timeout:         int  = None,

        command_timeout: int  = None,
        banner_timeout:  int  = None,
        auth_timeout:    int  = None,
        allow_agent:     bool = True,
        look_for_keys:   bool = True,
        compress:        bool = False,
        gss_auth:        bool = False,
        gss_kex:         bool = False,
        gss_deleg_creds: bool = True,
        gss_host:        str  = None,
        gss_trust_dns:   bool = True,
        passphrase            = None,
        disabled_algorithms   = None,
        sock                  = None,
        auto_sudo:       bool = False,
        reconnect:       bool = False,

        gname:           str  = None
) -> 'GqylpySSH':
    """Get a GqylpySSH instance.

    @param hostname:     Remote host address.
    @param port:         Port of the remote host sshd server.
    @param username:     Defaults to the current local username.
    @param password:     Used for password authentication; is also used for
                         private key decryption if the parameter `passphrase` is
                         not given.
    @param key_filename: Default file ~/.ssh/{id_rsa,id_dsa,id_ecdsa}.
    @param key_password: If the key has a password.
    @param timeout:      TCP Connect timeout period (in seconds), default
                         permanent.

    @param command_timeout:     Execute command timeout, default permanent.
    @param banner_timeout:      Timeout to wait for SSH banner display (in
                                seconds), default permanent.
    @param auth_timeout:        Authentication timeout (in seconds), default
                                permanent.
    @param allow_agent:         Whether to use SSH proxy.
    @param look_for_keys:       Whether to allow key login.
    @param compress:            Whether to enable compression.
    @param gss_auth:            Whether to use GSS-API authentication.
    @param gss_kex:             Whether to Perform GSS-API Key Exchange and user
                                authentication.
    @param gss_deleg_creds:     Whether to delegate gSS-API client credentials.
    @param gss_host:            The target name in the kerberos database,
                                default hostname.
    @param gss_trust_dns:       Whether to trust DNS to securely normalize the
                                names connected hosts.
    @param passphrase:          Used for decrypting private keys.
    @param disabled_algorithms: An optional dictionary passed to `Transport` and
                                its namesake keyword argument.
    @param sock:                An open socket or socket-like object (such as a
                                `.Channel`) to use for communication to the
                                target host.
    @param auto_sudo:           Automatically add "sudo" to the front of the
                                command.
    @param reconnect:           If the ssh connection is disconnected when you
                                call method `self.cmd`, will attempt to
                                reconnect.

    @param gname: Create a pointer to an instance of `GqylpySSH` in the
                  `gqylpy_ssh` module, if not None.

    @return: GqylpySSH(**@param)
    """
    gobj = GqylpySSH(
        hostname           =hostname,
        port               =port,
        username           =username,
        password           =password,
        key_filename       =key_filename,
        key_password       =key_password,
        timeout            =timeout,
        command_timeout    =command_timeout,
        allow_agent        =allow_agent,
        look_for_keys      =look_for_keys,
        compress           =compress,
        sock               =sock,
        gss_auth           =gss_auth,
        gss_kex            =gss_kex,
        gss_deleg_creds    =gss_deleg_creds,
        gss_host           =gss_host,
        banner_timeout     =banner_timeout,
        auth_timeout       =auth_timeout,
        gss_trust_dns      =gss_trust_dns,
        passphrase         =passphrase,
        disabled_algorithms=disabled_algorithms,
        auto_sudo          =auto_sudo,
        reconnect          =reconnect
    )

    if gname is None:
        return gobj

    setattr(__gpack__, gname, gobj)

    if not hasattr(__gpack__, '__first__'):
        __gpack__.__first__ = gobj


class GqylpySSH(paramiko.SSHClient):

    def __init__(
        self,
        hostname:        str,
        port:            int  = 22,
        *,
        username:        str  = None,
        password:        str  = None,
        key_filename:    str  = None,
        key_password:    str  = None,
        timeout:         int  = None,
        command_timeout: int  = None,
        banner_timeout:  int  = None,
        auth_timeout:    int  = None,
        allow_agent:     bool = True,
        look_for_keys:   bool = True,
        compress:        bool = False,
        gss_auth:        bool = False,
        gss_kex:         bool = False,
        gss_deleg_creds: bool = True,
        gss_host:        str  = None,
        gss_trust_dns:   bool = True,
        passphrase            = None,
        disabled_algorithms   = None,
        sock                  = None,
        auto_sudo:       bool = False,
        reconnect:       bool = False
    ):
        """
        @param hostname:     Remote host address.
        @param port:         Port of the remote host sshd server.
        @param username:     Defaults to the current local username.
        @param password:     Used for password authentication; is also used for
                             private key decryption if the parameter
                             `passphrase` is not given.
        @param key_filename: Default file ~/.ssh/{id_rsa,id_dsa,id_ecdsa}.
        @param key_password: If the key has a password.
        @param timeout:      TCP Connect timeout period (in seconds), default
                             permanent.
        @param command_timeout:     Execute command timeout, default permanent.
        @param banner_timeout:      Timeout to wait for SSH banner display (in
                                    seconds), default permanent.
        @param auth_timeout:        Authentication timeout (in seconds), default
                                    permanent.
        @param allow_agent:         Whether to use SSH proxy.
        @param look_for_keys:       Whether to allow key login.
        @param compress:            Whether to enable compression.
        @param gss_auth:            Whether to use GSS-API authentication.
        @param gss_kex:             Whether to Perform GSS-API Key Exchange and
                                    user authentication.
        @param gss_deleg_creds:     Whether to delegate gSS-API client
                                    credentials.
        @param gss_host:            The target name in the kerberos database,
                                    default hostname.
        @param gss_trust_dns:       Whether to trust DNS to securely normalize
                                    the names connected hosts.
        @param passphrase:          Used for decrypting private keys.
        @param disabled_algorithms: An optional dictionary passed to `Transport`
                                    and its namesake keyword argument.
        @param sock:                An open socket or socket-like object (such
                                    as a `.Channel`) to use for communication to
                                    the target host.
        @param auto_sudo:           Automatically add "sudo" to the front of the
                                    command.
        @param reconnect:           If the ssh connection is disconnected when
                                    you call method `self.cmd`, will attempt to
                                    reconnect.
        """
        super().__init__()

        self.connect(
            hostname           =hostname,
            port               =port,
            username           =username,
            password           =password,
            pkey               =paramiko.RSAKey.from_private_key_file(
                                    key_filename, key_password
                                ) if key_filename is not None else None,
            timeout            =timeout,
            allow_agent        =allow_agent,
            look_for_keys      =look_for_keys,
            compress           =compress,
            sock               =sock,
            gss_auth           =gss_auth,
            gss_kex            =gss_kex,
            gss_deleg_creds    =gss_deleg_creds,
            gss_host           =gss_host,
            banner_timeout     =banner_timeout,
            auth_timeout       =auth_timeout,
            gss_trust_dns      =gss_trust_dns,
            passphrase         =passphrase,
            disabled_algorithms=disabled_algorithms
        )
        self.hostname        = hostname
        self.command_timeout = command_timeout
        self.auto_sudo       = auto_sudo
        self.reconnect       = reconnect

        self.params: dict
        # almost all the initialization parameters.

    def __del__(self):
        self.close()

    def cmd(
            self,
            command: str,
            *,
            timeout: int  = None,
            bufsize: int  = None,
            get_pty: bool = None,
            env:     dict = None
    ) -> 'Command':
        """
        @param command: A command string.
        @param timeout: Execute command timeout, default permanent.
        @param bufsize: Buffer size, default permanent.
        @param get_pty: Whether to enable pseudo-terminal, default False.
        @param env:     A dictionary of environment variables. Indication:
                        server may reject environment variables.
        """
        if self.auto_sudo and not command.startswith('sudo '):
            command = f'sudo {command}'

        if command[-1] == '&':
            return self.cmd_async(
                command=command,
                timeout=timeout,
                bufsize=bufsize,
                get_pty=get_pty,
                env=env
            )
        try:
            _, stdout, stderr = self.exec_command(
                command=command,
                timeout=timeout or self.command_timeout,
                bufsize=bufsize,
                get_pty=get_pty,
                environment=env
            )
        except (paramiko.SSHException, ConnectionResetError) as e:
            if not self.reconnect:
                raise e
            try:
                self.connect(self.hostname, **self.params)
            except (paramiko.NoValidConnectionsError, TimeoutError):
                raise e
            else:
                _, stdout, stderr = self.exec_command(
                    command=command,
                    timeout=timeout or self.command_timeout,
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
            env:     dict = None
    ) -> 'Generator':
        """
        @param commands: A commands tuple or list.
        @param timeout:  Execute command timeout, default permanent.
        @param bufsize:  Buffer size, default permanent.
        @param get_pty:  Whether to enable pseudo-terminal, default False.
        @param env:      A dictionary of environment variables. Indication:
                         server may reject environment variables.
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
            env:     dict = None
    ) -> 'threading.Thread':
        """
        @param command: A command string.
        @param timeout: Execute command timeout, default permanent.
        @param bufsize: Buffer size, default permanent.
        @param get_pty: Whether to enable pseudo-terminal, default False.
        @param env:     A dictionary of environment variables. Indication:
                        server may reject environment variables.
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
            raise SSHCommandError

    @property
    def status(self) -> bool:
        return True if command_exitcode == 0 else False

    @property
    def output(self) -> str:
        return process(command_output)

    @property
    def status_output(self) -> 'Tuple[bool, str]':
        return self.status, self.output

    def output_else_raise(self) -> str:
        self.raise_if_error()
        return self.output

    def output_else_define(self, define=None):
        return self.output if self.status else define

    def contain(self, string: str) -> bool:
        return string in self.output

    def contain_string_else_raise(self, string: str):
        if not self.contain(string):
            raise SSHCommandError

    def output_if_contain_string_else_raise(self, string: str) -> str:
        if self.contain(string):
            return self.output
        raise SSHCommandError

    def table2dict(self, *, split: str = None) -> 'Generator':
        """Convert the titled output to dictionary."""

    def line2list(self, *, split: str = None) -> 'Generator':
        """Convert to list by line."""


def gname2gobj(func):
    def inner(*a, gname: 'Union[str, GqylpySSH]' = None, **kw) -> Command:
        if gname is None:
            gobj: GqylpySSH = __first__
        elif gname.__class__ is str:
            gobj: GqylpySSH = getattr(__gpack__, gname)
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
        env:     dict = None,
        gname:  'Union[str, GqylpySSH]' = None
) -> Command:
    """
    @param command: A command string.
    @param timeout: Execute command timeout, default permanent.
    @param bufsize: Buffer size, default permanent.
    @param get_pty: Whether to enable pseudo-terminal, default False.
    @param env:     A dictionary of environment variables. Indication:
                    server may reject environment variables.
    @param gname:   GqylpySSH instance or pointer name of GqylpySSH instance.
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
        env:     dict = None,
        gname:  'Union[str, GqylpySSH]' = None
) -> 'Generator':
    """
    @param commands: A commands tuple or list.
    @param timeout:  Execute command timeout, default permanent.
    @param bufsize:  Buffer size, default permanent.
    @param get_pty:  Whether to enable pseudo-terminal, default False.
    @param env:      A dictionary of environment variables. Indication:
                     server may reject environment variables.
    @param gname:    GqylpySSH instance or pointer name of GqylpySSH instance.
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
        env:     dict = None,
        gname:  'Union[str, GqylpySSH]' = None
) -> 'threading.Thread':
    """
    @param command: A command string.
    @param timeout: Execute command timeout, default permanent.
    @param bufsize: Buffer size, default permanent.
    @param get_pty: Whether to enable pseudo-terminal, default False.
    @param env:     A dictionary of environment variables. Indication:
                    server may reject environment variables.
    @param gname:   GqylpySSH instance or pointer name of GqylpySSH instance.
    """
    return (gname or __first__).cmd_async(
        command=command,
        timeout=timeout,
        bufsize=bufsize,
        get_pty=get_pty,
        env=env
    )


SSHException              = paramiko.ssh_exception.SSHException
AuthenticationException   = paramiko.ssh_exception.AuthenticationException
PasswordRequiredException = paramiko.ssh_exception.PasswordRequiredException
BadAuthenticationType     = paramiko.ssh_exception.BadAuthenticationType
PartialAuthentication     = paramiko.ssh_exception.PartialAuthentication
ChannelException          = paramiko.ssh_exception.ChannelException
BadHostKeyException       = paramiko.ssh_exception.BadHostKeyException
IncompatiblePeer          = paramiko.ssh_exception.IncompatiblePeer
ProxyCommandFailure       = paramiko.ssh_exception.ProxyCommandFailure
NoValidConnectionsError   = paramiko.ssh_exception.NoValidConnectionsError
CouldNotCanonicalize      = paramiko.ssh_exception.CouldNotCanonicalize
ConfigParseError          = paramiko.ssh_exception.ConfigParseError

import sys
import threading
from typing import Union, Tuple, Generator

__first__: GqylpySSH
__gpack__ = sys.modules[__name__]


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    """  QYYYQLLYYYYYYYQLYYQYYQQQYQQYQQQQQQQQQQQQQQQQQQQQQQYYYQQQQQQYL
        YYYYQYLLQYLLYYQYYYYYYYQQYQYQYQQQQQQQQQQQQQQQQQQQQQQQYYYQQQQQQ
        QYYYYLPQYLPLYYYLLYYYYYYYYQQQYQQQQQQQQQQQQQQQQQQQQQQQYYYYQQQQQP
        QYYQLPLQYLLYYQPLLLYYYYYYQYYQYQQQQQQQQQQQQQQYQQQQQQQQYYQYQQQQQQP
       QYYQYLLYYYLLYQYLLYYYYYYYYQYYQYQYYYQQQQQQQQQQYQQQQQQYQQYQYYQQQQQYP
      LQYQYYYYQYYYYYQYYYYYYYYYYYYYYYQQYYYYYYYYYQQQQYQQQQQQYQQYQYYQQQQQQ P
      QYQQYYYYQYYYQQQYYYYYYYYQYQYYYYQQYYYQYQYYQQQQYQQQQQQQYQQYQYYQQQQQQ P
      QYQQYYYYQYYYQQQYYYYYYYYQYQYYYYYQYYYYQYYYQQQQYQQQQQQQYQQYQQYQQQQYYP
      QYQYYYYYQYYYQQQ PYLLLYP PLYYYYYYQYYYYYYQQQQYYQQQQQQYQQYQQQYQQQQYQ
      PQQYYYYYQYYQQYQQQQQQQQQQYP        PPLYQYQYQYQLQQQQQYQQYQQQYYQQQYY
       QQYYYYYQQYQLYQQPQQQQQL QYL           PPYYLYYLQYQQYYQYQQQQYYQPQYL
       YQYYYYQQQYQ  LYLQQQQQQYQQ           YQQQQQGQQQQQQYQYYQQQQYQPQYQ P
      L QYYYYQQLYQ   Y YPYQQQQQ           LQQQQQL YQQQQYQQYQYQQYYQQYQP P
        YYQYYQQ  Q    LQQQQQQY            YQYQQQQQQYYQYLQYQQYQQYYQYQL P
     Y  LYQLQQPL Y     P  P                QLLQQQQQ Q  PQQQQYQQYYQQL P
    P   PYQYQQQQPQ                         PQQQQQQY    QQYQYYQQYYQPP
    L    QQQYQ YYYY              PQ           L  P    LPQYQYYQQLQ P
    Y   PPQQYYL LYQL                                 PQLQYQQYQYQ  L
    Y     QQYQPP PYQY        PQ                      Q  QQYQYQYL  L
    Y     QQYYQ L  QYQP         PLLLLLYL           LQQ LQYYQQQP P L
     L   PPLQYYQ Y  LQQQ                         LQYQ  QYYYQQ     P
      L    Q  QYQ  Y  QQPYL                   PQYYYYPPQYYQQQP    L
       L    L  PQQL   LYQ  PQP             QL PYYYPLQLYQ  QY P   Y
         P   P    PQQP  QY  QLLQQP   LYYLQ   PQYPQQQP P  QY P   L
                       PYQYYY           PQ  PQ      L   Q P    L
              PQYLYYYPQ PLPL             L QY YQYYQYLYQQQ    P
            PYLLLLLYYYQ P  L    P         PYL  PQYYLLLLLLLQ
           LYPLLLLLLYYYY   Y  YQY     LLLPPY   LYYYLLLLLLLLY
           YLLLYLLLLLLYYQ  Q              PQ  YYYLLLLLLLLLLYP
          YLLLLLLLLLLLLLLYQQ              PYYQYYLLLLLLLLYYYLQ
          QLLLLLLLLLLLLLLLLLYYQYP        YQYYLLLLLLLLLLLLLLLQ
          YLLLLLLLLLLLLLLLLLLLYYYLLYYYLLLLLLLLLLLLLLLLLLLLLLYP
         PLLLLLLLLLLLLLLLLLLLLLLLYLLLLLLLLLLLLLLLLLLLLLLLYLYLL
         LLLLLLLLLLYYLLLLLLYLLLLLLLLLLLLLLLL GQYLPY LLLYLYLLLY
         QLLLLYYLYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQYYYYLLQ
         QLLLLLYYQYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQLYYLLLQ
        LYLLYLLLQYYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLYLLLLLQYYYYYLYQ
        YLLLYYLLYQYLLLLLLLLLLLLLLLLLLLLLLLLLLLLYLLLLLYYYYQLLLLY
        QLLLYYYYYQLLLLLLLLLLLLLLYLLLLLLLLLLLLLLLLLLLLYYYLQLLPLLQ
        YLYLLQYYYQLLLLLLLLLLLLLLLLLLLLLLLLLLLLYYLLLLLYYQYYLLLLLQ
       LYLLLLLYYYQLLYLLLLLLLLLLLLYLYLLYYLLLLYLLLLLLLYYYQQLLLLLLLY
       YLLLLLLYYYQLLYLLLLLLLYLYLLLLLLLLLLLLLLLLLLLLYYYYQQLYLLLLLQ
       QLLLYLLLQYQLQLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLYYYQYYLLLLLLLY
       QLLLLLLLLQQYQLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQYYQYYLLLLLLLQ
       QLLLLLLLLLQQYLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLYYYYLLLLLLLLLYL
       QLLLLYLYYLYQLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLQYYYLLLLLLLLLQ
       YLLLLLLLYYLQLLLLLLLLLLLLLLLLLLLLLLLLLYLLLLLLLLYQYYLLLLLLLLLQ
       QLLLLLYLYYYYLLLLLPLLLLLLLYLYLLLLLLLLLLLLLLLLLLLQYYLLLLLLLLYP
       YYLYYLLYYYQLLLLLLLLYLLLLLLLLLLLLLLLLLLLLLLYLYLLYQYYLLLLLLYL
        QLLLLLLYQYLLLLLLLLLLLLLLLLLLLLLYYLYLLLLLLLLLLLYQQQQQQQLYL  """
    __import__(f'{__name__}.g {__name__[7:]}')
    gcode = globals()[f'g {__name__[7:]}']

    for gname in globals():
        if gname[0] != '_' and hasattr(gcode, gname):
            gfunc = getattr(gcode, gname)
            gfunc.__module__ = __package__
            setattr(__gpack__, gname, gfunc)

    setattr(__gpack__, '__init__', gcode.__init__)
