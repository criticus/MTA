__author__="criticus"
__date__ ="$Apr 7, 2011 4:40:15 PM$"

from abstract import GatewayAbstract

class Motricity(GatewayAbstract):
    "class for Motricity gateway"

    def set_gateway(self,data):
        self._gateway = {'url'       :"http://gt.od.motricity.com/messagingAPI/3_0/sendsms",
                         'login'     :data['GatewaysLogin'],
                         'short_code':data['GatewaysCode'],
                         'reporting' :True}

    def set_message(self,msg):
        self._message = msg

    def prepare_msg(self):
        import urllib
        data = {'a':self._gateway['login'],
                's':self._gateway['short_code'],
                'd':self._message['PhoneNumber'],
                'm':self._message['Message'],
                'c':int(self._message['OperatorsID'])}
        return urllib.urlencode(data)

    def parse_response(self,response):
        response = str(response)
        if response.find('Error') == -1:
            self._success = True
        else:
            self._success = False
        return response
            