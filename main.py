import socket

from teraflashpy import LOCALHOST

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((LOCALHOST, 6341))

s.listen(1)

conn, addr = s.accept()
