import socket
import ssl


context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')


def send_ssl_message(hostname, req, *, port=443, timeout=None):
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            if timeout != None:
                ssock.settimeout(timeout)
            ssock.sendall(req)
            response = b''
            chunk = ssock.recv(4096)
            while chunk != b'':
                response += chunk
                chunk = ssock.recv(4096)
            return response

def send_message(hostname, req, *, port=80, timeout=None):
    with socket.create_connection((hostname, port)) as sock:
        if timeout != None:
            sock.settimeout(timeout)
        sock.sendall(req)
        response = b''
        chunk = sock.recv(4096)
        while chunk != b'':
            response += chunk
            chunk = sock.recv(4096)
        return response

if __name__ == '__main__':
    print(send_ssl_message('jonyork.net',
          b'GET / HTTP/1.1\r\nHost: google.com\r\nAccept: */*\r\nAccept-Encoding: identity\r\nConnection: close\r\n\r\n').decode())
