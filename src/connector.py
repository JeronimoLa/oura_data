from enum import Enum
import sqlite3


sqlite_data_types = {
    "NULL": "Represents missing information or unknown values.",
    "INTEGER": "Signed whole numbers stored in 1, 2, 3, 4, 6, or 8 bytes, depending on magnitude.",
    "REAL": "Floating-point numbers stored as 8-byte IEEE floats.",
    "TEXT": "Character data stored using UTF-8, UTF-16BE, or UTF-16LE encoding. Maximum length is unlimited.",
    "BLOB": "Binary Large Object used to store any kind of data exactly as input. Maximum size is theoretically unlimited."
}


class Type(Enum):
    dict = "TEXT"
    str = "INTEGER"
    int

conn = sqlite3.connect('oura.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()