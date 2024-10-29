# -*- coding=utf-8 -*-
r"""
possible option is /usr/bin/notify-send
"""
import subprocess
import shlex


MB_INFO = '--info'
MB_WARNING = '--warning'
MB_ERROR = '--error'
MB_QUESTION = '--question'

IDYES = 0
IDNO = 1


# option/todopoint: change text according to language
XMB_OK = 'Ok'
XMB_YES = 'Yes'
XMB_NO = 'No'
XMB_CANCEL = 'Cancel'
XMB_RETRY = 'Retry'


def _msg(title: str, message: str, what):
    result = subprocess.run([
        '/usr/bin/zenity',
        what,
        '--title', title,
        '--text', message
    ])
    return result.returncode


def _xmsg(title: str, message: str, buttons: tuple):
    try:
        return subprocess.check_output([
            '/usr/bin/xmessage',
            '-print',
            '-center',
            '-buttons', ",".join(shlex.quote(btn) for btn in buttons),
            # '-default', "<buttont>",
            '-title', title,
            message
        ])
    except subprocess.CalledProcessError:
        return None


def showinfo(title: str, message: str):
    _msg(title, message, MB_INFO)


def showwarning(title: str, message: str):
    _msg(title, message, MB_WARNING)


def showerror(title: str, message: str):
    _msg(title, message, MB_ERROR)


def askquestion(title: str, message: str):
    result = _msg(title, message, MB_QUESTION)
    if result == IDYES:
        return True
    elif result == IDNO:
        return False
    else:
        raise SystemError('unknown return code: {}'.format(result))


def askokcancel(title: str, message: str):
    result = _xmsg(title, message, (XMB_OK, XMB_CANCEL))
    if result == XMB_OK:
        return True
    elif result == XMB_CANCEL:
        return False
    else:
        raise SystemError('unknown return code: {}'.format(result))


def askyesno(title: str, message: str):
    result = _msg(title, message, MB_QUESTION)
    if result == IDYES:
        return True
    elif result == IDNO:
        return False
    else:
        raise SystemError('unknown return code: {}'.format(result))


def askyesnocancel(title: str, message: str):
    result = _xmsg(title, message, (XMB_YES, XMB_NO, XMB_CANCEL))
    if result == XMB_YES:
        return True
    elif result == XMB_NO:
        return False
    elif result == XMB_CANCEL:
        return None
    else:
        raise SystemError('unknown return code: {}'.format(result))


def askretrycancel(title: str, message: str):
    result = _xmsg(title, message, (XMB_RETRY, XMB_CANCEL))
    if result == XMB_RETRY:
        return True
    elif result == XMB_CANCEL:
        return False
    else:
        raise SystemError('unknown return code: {}'.format(result))
