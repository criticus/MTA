__author__="criticus"
__date__ ="$Apr 7, 2011 4:40:15 PM$"

from abstract import GatewayAbstract

class MxTelecom(GatewayAbstract):
    "class for MxTelecom gateway"

    def set_gateway(self,data):
        self._gateway = {'url'       :"http://sms.mxtelecom.com/SMSSend",
                         'login'     :data['GatewaysLogin'],
                         'passw'     :data['GatewaysPass'],
                         'short_code':data['GatewaysCode'],
                         'reporting' :True}

    def set_message(self,msg):
        self._message = msg

    def prepare_msg(self):
        import urllib
        data = {'user'   :self._gateway['login'],
                'pass'   :self._gateway['passw'],
                'smsfrom':self._gateway['short_code'],
                'smsto'  :"1"+self._message['PhoneNumber'],
                'smsmsg' :self._message['Message'],
                'report' :self._gateway['reporting']}
        return urllib.urlencode(data)

    def parse_response(self,response):
        if response.isdigit():
            self._success = True
        else:
            self._success = False
        return response
            