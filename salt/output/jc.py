# -*- coding: utf-8 -*-
"""
JC Outputter for Salt
JC converts the output of many commands and file-types to structured format.
https://github.com/kellyjonbrazil/jc
Requires JC is installed via pip: $ pip3 install jc
Requires Python >= 3.6

Usage:
    This outputter requires a parser to be defined via the JC_PARSER env variable:
    $ JC_PARSER=uptime salt '*' cmd.run 'uptime' --out=jc
.. versionadded:: TBD
"""
import os
import importlib
import json
from salt.exceptions import SaltRenderError

try:
    import jc
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

__virtualname__ = "jc"


def __virtual__():
    return __virtualname__


def output(data, parser=None):
    """
    Convert returned command output to JSON using the JC library
    :rtype: str (JSON)
    """

    parser = os.getenv('JC_PARSER')

    if not HAS_LIB:
        raise SaltRenderError('You need to install "jc" prior to running the jc outputter')

    if not parser:
        raise SaltRenderError("You must specify a parser for the jc outputter by exporting the JC_PARSER env variable."
                              "e.g. export JC_PARSER='uptime'")

    try:
        jc_parser = importlib.import_module('jc.parsers.' + parser)
        result = jc_parser.parse(data['minion'], quiet=True)
        return json.dumps(result)

    except Exception as e:
        raise SaltRenderError('Error in jc outputter:  %s' % e)
