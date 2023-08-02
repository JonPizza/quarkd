import time
import socket

from .http_response import RespParser
from .raw_http import send_message, send_ssl_message

DEFAULT_HEADERS = [
    'Accept: */*',
    'Accept-Encoding: identity',
    'Connection: close',
    'User-Agent: Chrome/114.0.5735.199',
]

def parse_url(url):
    proto_end_idx = url.find('//') + 2
    path_start_idx = url[proto_end_idx:].find('/') + proto_end_idx
    proto = url[0:proto_end_idx]
    if path_start_idx + 1 == proto_end_idx:
        path_start_idx = len(url)
    host = url[proto_end_idx:path_start_idx]
    path = url[path_start_idx:]
    if path == '':
        path = '/'
    return proto, host, path


def parse_host(proto, host):
    if ':' in host:
        return host.split(':')[0], int(host.split(':')[1])
    else:
        if proto == 'http://':
            return host, 80
        else:
            return host, 443


def build_request(method, url, headers, body):
    proto, host, path = parse_url(url)
    request = b''
    request += f'{method} {path} HTTP/1.1\r\n'.encode('utf-8')
    request += f'Host: {host}\r\n'.encode('utf-8')
    for h in DEFAULT_HEADERS + headers:
        request += (h + '\r\n').encode('utf-8')
    request += b'\r\n'
    request += body.encode('utf-8')
    return request


def send_http11(method, url, headers, body='', timeout=None):
    proto, host, _ = parse_url(url)
    hostname, port = parse_host(proto, host)
    request = build_request(method, url, headers, body)
    start_time = time.time()
    try:
        if proto == 'http://':
            response = send_message(
                hostname, request, port=port, timeout=timeout)
        else:
            response = send_ssl_message(
                hostname, request, port=port, timeout=timeout)
    except socket.timeout:
        return 'timeout'
    response = RespParser(response.decode('utf-8'))
    response.time = time.time() - start_time
    return response


if __name__ == '__main__':
    res = send_http11('GET', 'https://jonyork.net/', timeout=4)
    print(res.status_code)
    for k, v in res.headers.items():
        print(f'{k}: {v}')
    print('\n')
    print(res.body)
