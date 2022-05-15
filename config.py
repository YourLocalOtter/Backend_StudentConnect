ALGORITHM = "HS256"
import socket
SECRET = "testserver-" + socket.gethostname() + "-" + socket.getfqdn()