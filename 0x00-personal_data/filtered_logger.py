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
    """
    for field in fields:
        pattern = r'(?<={0}{1}=)[^{0}]+'.format(re.escape(separator), field)
        message = re.sub(pattern, redaction, message)
    return message
