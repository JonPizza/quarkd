import threading
from queue import Queue
import sys
import requests
import random
import argparse

from jonhttp.http import send_http11
from payloads.payloads import PAYLOADS
from payloads.verifier import verify_payload
from colors import *

args = []  # global var to keep track of all args...
thread_food = Queue()

def verify_url_works(url):
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:  # don't allow redirs for now. so sue me :/
            return True
    except:
        return False


def log_success(method, url, exploit, exploid_id, thread_id):
    print(f'[T-{thread_id}] {CYAN}[+] possible exploit: \'{exploit["name"]}\' {exploid_id} {method} {url}{RESET}')
    open(f'{args.output_file}.log', 'a').write(
        f'[T-{thread_id}] \'{exploit["name"]}\' {exploid_id} {method} {url}\n')

def log_success_fr(method, url, exploit, exploid_id, thread_id):
    print(f'[T-{thread_id}] {GREEN}[!] exploit: \'{exploit["name"]}\' {exploid_id} {method} {url}{RESET}')
    open(args.output_file, 'a').write(
        f'\'{exploit["name"]}\' {exploid_id} {method} {url}\n')

def log(method, url, exploit, exploid_id, thread_id):
    print(
        f'[T-{thread_id}] \'{exploit["name"]}\' {exploid_id} {method} {url}')


def get_send_http_method(exploit):
    if exploit.get('http_version') == '1.1':
        return send_http11
    else:  # default to HTTP/1.1
        return send_http11


def test_one_url(exploit, url, thread_id):
    headers = exploit['headers'] + [args.headers.replace('\\r\\n', '\r\n').replace('\\n', '\n')]
    send_http = get_send_http_method(exploit)
    methods = exploit['methods']
    for method in methods:
        for i, payload in enumerate(exploit['payloads']):
            responses = []
            for request in payload['requests']:
                response = send_http(
                    method, url, headers + request.get('headers', []), body=request.get('body', ''), timeout=20)
                if response != 'timeout' and (str(response.status_code) in args.skip_codes.split(',')):
                    break
                responses.append(response)
            if not args.silent and payload['check'](*responses):
                log_success(method, url, exploit, i, thread_id)
                if verify_payload(method, url, exploit, payload) and verify_payload(method, url, exploit, payload): # run verify_payload twice cuz i can. sue me.
                    log_success_fr(method, url, exploit, i, thread_id)
            elif not args.silent and args.verbose:
                log(method, url, exploit, i, thread_id)


def scan(thread_id):
    while True:
        url = thread_food.get()
        for exploit in PAYLOADS:
            if args.dont_verify or verify_url_works(url):
                print(f'[T-{thread_id}] Testing {url}')
                try:
                    test_one_url(exploit, url, thread_id)
                except Exception as e:
                    if args.verbose: # otherwise fail silent
                        raise e
        thread_food.task_done()


def load_args():
    global args
    parser = argparse.ArgumentParser(
        prog='Nuclepy',
        description='Automatically check for all sorts of vulnerabilityies mannn!',
        epilog='Rock on brotha.')
    parser.add_argument('url_file')
    parser.add_argument('output_file')
    parser.add_argument('-t', '--threads', dest='threads', default=10, type=int)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument('-k', '--dont-verify', dest='dont_verify', action='store_true')
    parser.add_argument('-s', '--silent', dest='silent', action='store_true')
    parser.add_argument('-hd', '--headers', dest='headers', default='', help='Invalid headers are okay. Input as a striiing')
    parser.add_argument('-sc', '--skip-codes', dest='skip_codes', default='403,405', help='deez codes ain\'t vulnerable (prolly). Comma sep list. (default: 403,405,418) (i dont fw teapots)')
    args = parser.parse_args()


def main():
    load_args()

    urls = open(args.url_file).read().split('\n')
    random.shuffle(urls)  # randomize order to avoid rate limiting

    for url in urls:
        thread_food.put(url)

    for i in range(args.threads):
        threading.Thread(target=scan, args=(i,), daemon=True).start()

    thread_food.join()
    if not args.silent:
        print('that\'s all folks!')


if __name__ == '__main__':
    main()
