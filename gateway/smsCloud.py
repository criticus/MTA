__author__="criticus"
__date__ ="$Apr 7, 2011 4:40:15 PM$"

from abstract import GatewayAbstract
from simplejson import loads, dumps

class SmsCloud(GatewayAbstract):
    "class for SmsCloud gateway"

    def set_gateway(self,data):
        self._gateway = {'url'         :"http://184.105.241.31/jsonrpc",
                         'backup_url'  :"http://199.204.22.230/jsonrpc",
                         'api_key'     :data['GatewaysLogin'],
                         'api_version' :'1.0',
                         'api_method'  :'sms.send',
                         'api_priority':'1'}

    def set_message(self,msg):
        self._message = msg

    def prepare_msg(self):
        import uuid
        unique_id = str(uuid.uuid1())
        args = ['',
                    self._message['PhoneNumber'],
                    self._message['Message'],
                    self._gateway['api_priority']]
        return dict(id = unique_id,method=self._gateway['api_method'],params=args)

    def send(self,data):               
        url = self._gateway['url'] 
        url_tail = '?key=' + self._gateway['api_key'] + '&apiVersion=' + self._gateway['api_version']
        resp = self._request(url+url_tail, data)
                
        if resp.status_int != 200:
            url = self._gateway['backup_url']
            resp = self._request(url+url_tail, data)
            if resp.status_int != 200:
                return {'Conn_Error': 'Could not connect to SMSCloud'}
        
        return loads(resp.body)

    def _request(self,url,data):
        from webob import Request
        from wsgiproxy.exactproxy import proxy_exact_request        
        req = Request.blank(url)
        req.method = 'POST'
        req.content_type = 'application/json-rpc'
        req.body = dumps(data)
        return req.get_response(proxy_exact_request)

    def parse_response(self,response):               
        if response.get('Conn_Error') is not None:
            self._success = False
            return response.get('Conn_Error')
        if response.get('error') is not None:
            self._success = False
            return response.get('error')
        self._success = True
        return response['result']['sms_id']