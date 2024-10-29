# -*- coding=utf-8 -*-
r"""

"""

__all__ = [
    "showinfo",
    "showwarning",
    "showerror",
    "askquestion",
    "askokcancel",
    "askyesno",
    "askyesnocancel",
    "askretrycancel"
]


def showinfo(title: str, message: str):
    r"""
    Show an info message
    """
    raise NotImplementedError()


def showwarning(title: str, message: str):
    r"""
    Show a warning message
    """
    raise NotImplementedError()


def showerror(title: str, message: str):
    r"""
    Show an error message
    """
    raise NotImplementedError()


def askquestion(title: str, message: str):
    r"""
    Ask a question
    """
    raise NotImplementedError()


def askokcancel(title: str, message: str):
    r"""
    Ask if operation should proceed; return true if the answer is ok
    """
    raise NotImplementedError()


def askyesno(title: str, message: str):
    r"""
    Ask a question; return true if the answer is yes
    """
    raise NotImplementedError()


def askyesnocancel(title: str, message: str):
    r"""
    Ask a question; return true if the answer is yes, None if cancelled.
    """
    raise NotImplementedError()


def askretrycancel(title: str, message: str):
    r"""
    Ask if operation should be retried; return true if the answer is yes
    """
    raise NotImplementedError()
