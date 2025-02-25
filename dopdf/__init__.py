import os
import ntpath


import xl


import pyabo
from pyabo import base_suttaref, page_parsing
from doepub import basestr


TEX_DIR = PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

assert os.path.isdir(TEX_DIR)


_url_table = [
    ("%", "\\letterpercent"),
    ("#", "\\letterhash"),
    ("\\", "\\letterescape"),
]


def el_url(s):
    return _el(s, _url_table)


def _el(s, table=None):
    table = _url_table or table
    ns = ""
    for c in s:
        ns += _el_char(c, table)
    return ns


def _el_char(c, table):
    for (a, b) in table:
        if c == a:
            return b + " "
    return c


def _new_line(line):
    new_line = []
    for x in line:
        if isinstance(x, str):
            new_line.extend(base_suttaref.parse(x))
        else:
            new_line.append(x)

    return new_line


def join_to_tex(line: list, bns: list[str], c):
    new_line = _new_line(line)
    s = ""
    for x in new_line:
        if isinstance(x, str):
            s += c(x)
        elif isinstance(x, pyabo.BaseElement):
            s += x.to_tex(bns=bns, c=c)
        else:
            raise Exception((type(x), x))
    return s


def join_to_xml(line: list, bns, c, doc_path, tag_unicode_range=True):
    elements = []
    for x in _new_line(line):
        if isinstance(x, str):
            elements.extend(basestr.str2es(c(x), tag_unicode_range))
        elif isinstance(x, pyabo.BaseElement):
            elements.extend(x.to_es(bns=bns, c=c, doc_path=doc_path, tag_unicode_range=tag_unicode_range))
        elif isinstance(x, xl.Element):
            elements.append(x)
        else:
            raise Exception(x)
    return elements


def join_to_text(line: list, c=None):
    c = c or page_parsing.no_translate
    s = ""
    for x in line:
        if isinstance(x, str):
            s += x
        elif isinstance(x, pyabo.BaseElement):
            s += x.get_text()
        else:
            raise Exception(type(x))
    return c(s)


def ntrelpath(path1, path2):
    try:
        path = ntpath.relpath(path1, ntpath.dirname(path2))
    except ValueError:
        path = path1
    return path
