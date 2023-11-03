#!/usr/bin/env python3
"""
This module contains a function called filter_datum that
filters sensitive data from a message based on specified fields and
a class called RedactingFormatter.
"""
from typing import List
import logging
import re


class RedactingFormatter(logging.Formatter):
    """
    RedactingFormatter is a custom log formatter that redacts sensitive
    data from log messages.

    It inherits from the logging.Formatter class and provides functionality
    to obfuscate specific fields within log messages based on a provided list
    of sensitive fields.

    Attributes:
        REDACTION (str): The string used to replace sensitive data
        in log messages.
        FORMAT (str): The default log message format.
        SEPARATOR (str): The separator used to split the log message
        into segments.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize a RedactingFormatter instance.

        Args:
            fields (List[str]): A list of sensitive fields to obfuscate
            in log messages.
        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by obfuscating the sensitive fields in
        the log message.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message.

        """
        message = record.getMessage()
        if self.fields:
            message = filter_datum(self.fields, self.REDACTION,
                                   message, self.SEPARATOR)
        record.msg = message  # Update the record's message
        return super().format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Filters sensitive data from a message based on specified fields.

    Args:
        fields (List[str]): A list of fields to be filtered.
        redaction (str): The string to replace the filtered data with.
        message (str): The message containing sensitive data.
        separator (str): The separator used to split the message into segments.

    Returns:
        str: The obfuscated message with filtered data.
    """
    for field in fields:
        pattern = r'(?<={0}{1}=)[^{0}]+'.format(re.escape(separator), field)
        message = re.sub(pattern, redaction, message)
    return message
