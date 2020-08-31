# -*- coding: utf-8 -*-
"""
JC Renderer for Salt

JC converts the output of many commands and file-types to structured format.
https://github.com/kellyjonbrazil/jc

Requires JC is installed via pip: $ pip3 install jc

Requires Python >= 3.6

.. versionadded:: TBD
"""

import importlib
from salt.exceptions import SaltRenderError
from salt.ext import six

try:
    import jc
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def render(data, saltenv="base", sls="", parser=None, quiet=True, raw=False, **kws):
    """
    Convert returned command output to a dict or list of dicts using the JC library

    Arguments:
        parser      required    (string) the correct parser for the input data (e.g. 'ifconfig')
                                see https://github.com/kellyjonbrazil/jc/tree/master/docs/parsers
                                for latest list of parsers.
        quiet       optional    (bool) True to suppress warning messages (default is True)
        raw         optional    (bool) True to return pre-processed JSON (default is False)

    :rtype: A Python data structure
    """
    if not isinstance(data, six.string_types):
        # Read from file-like object
        data = data.read()

    if not HAS_LIB:
        raise SaltRenderError('You need to install "jc" prior to running the jc renderer')

    if not parser:
        raise SaltRenderError("You must specify a parser for the jc renderer. e.g. parser='uptime'")

    try:
        jc_parser = importlib.import_module('jc.parsers.' + parser)
        result = jc_parser.parse(data, quiet=quiet, raw=raw)
        return result if result.strip() else {}

    except Exception as e:
        raise SaltRenderError('Error in jc renderer:  %s' % e)
