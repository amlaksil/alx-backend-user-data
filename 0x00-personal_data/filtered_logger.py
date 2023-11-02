#!/usr/bin/env python3

"""
This module contains a function called filter_datum that
filters sensitive data from a message based on specified fields.
"""
from typing import List
import re


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

    Example:
        >>> flds = ['Password', 'User']
        >>> redaction = '[REDACTED]'
        >>> msg = 'User=silamlak@example.com;Password=secret123'
        >>> separator = ';'
        >>> filtered_message = filter_datum(fields, redaction, msg, separator)
        >>> print(filtered_message)
        User:[REDACTED];Password:[REDACTED]
    """
    str_to_be_replaced = []
    for item in fields:
        if item in message:
            msg_list = message.split(separator)
            for msg_segment in msg_list:
                if item in msg_segment:
                    delimiter = msg_segment[len(item)]
                    val = msg_segment.split(delimiter)[1]
                    str_to_be_replaced.append(val)
                    break
    obfuscated_msg = message
    for element in str_to_be_replaced:
        obfuscated_msg = re.sub(rf'{element}', f'{redaction}', obfuscated_msg)
    return obfuscated_msg
