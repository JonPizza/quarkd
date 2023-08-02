from jonhttp.http import build_request, send_http11


def verify_payload(method, url, exploit, payload, *, verbose=False):
    verifier = payload.get('verifier')
    if not verifier:
        return True  # no verifier = passes by default
    timeout = verifier.get('timeout', payload.get(
        'timeout', exploit.get('timeout', 10)))  # get best timeout
    responses = []
    for request in verifier['requests']:
        headers = exploit.get('headers', []) + request.get('headers', [])
        if verbose:
            print(' --- Request --- ')
            print(build_request(method, url, headers, request.get('body', '')).decode())
            print(' --- Response --- ')
        responses.append(send_http11(method, url, headers, body=request.get('body', ''), timeout=timeout))
        if verbose:
            if responses[-1] != 'timeout':
                print(responses[-1].response_text[:100] + '...' if len(responses[-1].response_text) > 103 else responses[-1].response_text)
            else:
                print('Timed out.')
    return verifier['check'](*responses)
