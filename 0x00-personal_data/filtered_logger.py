#!/usr/bin/env python3
"""
This module contains a function called filter_datum that
filters sensitive data from a message based on specified fields and
a class called RedactingFormatter.
"""
import mysql.connector
import logging
import os
import re
from typing import List
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """
    Create and configure a logger with a StreamHandler and
    RedactingFormatter.

    Returns:
            logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)

    # Create a StreamHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Add the StreamHandler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the personal data MySQL database.

    Returns:
            mysql.connector.connection.MySQLConnection: The database
            connection object.
    """
    db_connection = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connection


def main():
    """
    Retrieve all rows from the users table and display each row
    under a filtered format.
    """
    # Establish a database connection
    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)

    # Query the users table
    query = "SELECT * FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Configure the logger
    logger = get_logger()

    # Iterate over each row and log the filtered data
    for row in rows:
        filtered_row = '; '.join([f"{key}={value}" if key not in PII_FIELDS
                                  else f"{key}={RedactingFormatter.REDACTION}"
                                  for key, value in row.items()])

        filtered_row += ';'

        # Log the filtered row as an INFO-level message
        logger.info(filtered_row)

    # Close the cursor and database connection
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    main()
