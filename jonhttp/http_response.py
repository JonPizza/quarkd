class RespParser:
    def __init__(self, response_text):
        if response_text == '':
            return 'timeout'

        if type(response_text) == str:
            self.response_text = response_text
        else:
            self.response_text = response_text.decode()
        self.headers = {}
        
        self.parse()

    def parse(self):
        # i'm assuming good, clean HTTP is coming back (so i can write dirty code)
        status_end = self.response_text.index('\r\n')
        headers_end = self.response_text.index('\r\n\r\n')
        headers = self.response_text[status_end:headers_end]
        
        status_line = self.response_text[:status_end]
        while '  ' in status_line:
            # got a weird response on https://analytics.att.com/ (AkamaiGHost) 
            # status_line == 'HTTP/1.1   0 Init'
            # unsure what this means 
            status_line = status_line.replace('  ', ' ')  
        self.status_code = int(status_line.split(' ')[1])
        
        for h in headers.split('\r\n')[1:]:
            k, v = [h.split(':')[0], ':'.join(h.split(':')[1:])]
            self.headers[k] = v.strip()

        self.body = self.response_text[headers_end + 4:]


    
