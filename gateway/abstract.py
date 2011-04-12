__author__="criticus"
__date__ ="$Apr 7, 2011 4:40:15 PM$"

class GatewayAbstract:
    "abstract class for aggregators gateways"
    _gateway = ''
    _message = ''
    _success = False
    
    def __init__(self, msg):
        self.set_gateway(msg)
        self.set_message(msg)

    def process(self):
        data = self.prepare_msg()
        if data is not None:
            response = self.send(data)
            response = self.parse_response(response)
            return self.update_msg(self._message,response)
        else:
            self._message['Error'] = 'empty message'
            return self._message

    def prepare_msg(self,msg): pass
    
    def parse_response(self,response): pass

    def set_gateway(self,data): pass

    def set_message(self,msg): pass

    def send(self,data):
        import urllib2
        try:
            headers = self._gateway['headers']
        except NameError:
            headers = {}
        request = urllib2.Request(self._gateway['url'],data,headers)
        try:
            return urllib2.urlopen(request).read()
        except Exception:
            return str(Exception)

    def update_msg(self,msg,response):
        if self._success:
            msg['MT_ID'] = response
            msg['Sent'] = 1
        else:
            msg['Error'] = response
            msg['Sent'] = 2
        return msg


