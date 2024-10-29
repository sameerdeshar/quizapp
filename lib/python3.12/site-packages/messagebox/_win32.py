# -*- coding=utf-8 -*-
r"""
https://docs.microsoft.com/de-de/windows/win32/api/winuser/nf-winuser-messagebox?redirectedfrom=MSDN

maybe-todopoint:
    add option to specify default-button
"""
import ctypes


# => for buttons
MB_ABORTRETRYIGNORE = 0x00000002
MB_CANCELTRYCONTINUE = 0x00000006
MB_HELP = 0x00004000
MB_OK = 0x00000000
MB_OKCANCEL = 0x00000001
MB_RETRYCANCEL = 0x00000005
MB_YESNO = 0x00000004
MB_YESNOCANCEL = 0x00000003

# => for icons
# MB_ICONEXCLAMATION = 0x00000030
MB_ICONWARNING = 0x00000030
MB_ICONINFORMATION = 0x00000040
# MB_ICONASTERISK = 0x00000040
MB_ICONQUESTION = 0x00000020
MB_ICONSTOP = 0x00000010
MB_ICONERROR = 0x00000010
# MB_ICONHAND = 0x00000010

# => for default buttons
MB_DEFBUTTON1 = 0x00000000
MB_DEFBUTTON2 = 0x00000100
MB_DEFBUTTON3 = 0x00000200
MB_DEFBUTTON4 = 0x00000300

# => return-codes
IDABORT = 3
IDCANCEL = 2
IDCONTINUE = 11
IDIGNORE = 5
IDNO = 7
IDOK = 1
IDRETRY = 4
IDTRYAGAIN = 10
IDYES = 6


def _msg(title: str, message: str, style: int):
    # MessageBoxW(hwnd, text, caption, utype)
    return ctypes.windll.user32.MessageBoxW(None, message, title, style)


def showinfo(title: str, message: str):
    _msg(title, message, MB_ICONINFORMATION | MB_OK)


def showwarning(title: str, message: str):
    _msg(title, message, MB_ICONWARNING | MB_OK)


def showerror(title: str, message: str):
    _msg(title, message, MB_ICONERROR | MB_OK)


def askquestion(title: str, message: str):
    result = _msg(title, message, MB_ICONINFORMATION | MB_YESNO)
    if result == IDYES:
        return True
    elif result == IDNO:
        return False
    else:
        raise SystemError('unknown return code: {}'.format(result))


def askokcancel(title: str, message: str):
    result = _msg(title, message, MB_ICONQUESTION | MB_OKCANCEL)
    if result == IDOK:
        return True
    elif result == IDCANCEL:
        return False
    else:
        raise SystemError('unknown return code: {}'.format(result))


def askyesno(title: str, message: str):
    result = _msg(title, message, MB_ICONQUESTION | MB_YESNO)
    if result == IDYES:
        return True
    elif result == IDNO:
        return False
    else:
        raise SystemError('unknown return code: {}'.format(result))


def askyesnocancel(title: str, message: str):
    result = _msg(title, message, MB_ICONQUESTION | MB_YESNOCANCEL)
    if result == IDYES:
        return True
    elif result == IDNO:
        return False
    elif result == IDCANCEL:
        return None
    else:
        raise SystemError('unknown return code: {}'.format(result))


def askretrycancel(title: str, message: str):
    result = _msg(title, message, MB_ICONQUESTION | MB_RETRYCANCEL)
    if result == IDRETRY:
        return True
    elif result == IDCANCEL:
        return None
    else:
        raise SystemError('unknown return code: {}'.format(result))
