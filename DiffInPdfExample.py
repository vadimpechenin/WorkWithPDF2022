"""
https://translated.turbopages.org/proxy_u/en-ru.ru.fe9fe0ca-632f3bcb-3afb6190-74722d776562/https/www.geeksforgeeks.org/check-if-two-pdf-documents-are-identical-with-python/
difflib: это модуль, который содержит функцию, позволяющую сравнивать набор данных.
SequenceMatcher : используется для сравнения пары входных последовательностей.
"""

import hashlib
from difflib import SequenceMatcher


def hash_file(fileName1, fileName2):
    # Use hashlib to store the hash of a file
    h1 = hashlib.sha1()
    h2 = hashlib.sha1()

    with open(fileName1, "rb") as file:

        # Use file.read() to read the size of file
        # and read the file in small chunks
        # because we cannot read the large files.
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h1.update(chunk)

    with open(fileName2, "rb") as file:

        # Use file.read() to read the size of file a
        # and read the file in small chunks
        # because we cannot read the large files.
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h2.update(chunk)

        # hexdigest() is of 160 bits
        return h1.hexdigest(), h2.hexdigest()


msg1, msg2 = hash_file("pdf\\pd1.pdf ", "pdf\\pd2.pdf")

if (msg1 != msg2):
    print("These files are not identical")
else:
    print("These files are identical")