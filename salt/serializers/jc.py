"""
    salt.serializers.jc
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements JC serializer.

    JC converts the output of many commands and file-types to structured format.
    https://github.com/kellyjonbrazil/jc
    Requires JC is installed via pip: $ pip3 install jc
    Requires Python >= 3.6
"""
import importlib

# Import Salt libs
from salt.serializers import DeserializationError

# Import jc
try:
    import jc

    available = True
except ImportError:
    available = False


__all__ = ["deserialize", "available"]


class NotImplementedError(DeserializationError):
    pass


def deserialize(stream_or_string, parser=None):
    """
    Deserialize from raw command output into Python data structure.

    :param stream_or_string: command output stream or string to deserialize.
    :param parser: parser used to serialze the command output
    """

    if not available:
        raise DeserializationError('You need to install "jc" prior to running the jc deserializer')

    if not parser:
        raise DeserializationError("You must specify a parser for the jc deserializer. e.g. parser='uptime'")

    try:
        jc_parser = importlib.import_module('jc.parsers.' + parser)
        if not isinstance(stream_or_string, (bytes, str)):
            return jc_parser.parse(stream_or_string, quiet=True)

        if isinstance(stream_or_string, bytes):
            stream_or_string = stream_or_string.decode("utf-8")

        return jc_parser.parse(stream_or_string, quiet=True)

    except Exception as error:  # pylint: disable=broad-except
        raise DeserializationError(error)


def serialize(obj, **options):
    raise NotImplementedError("JC can only deserialize.")
