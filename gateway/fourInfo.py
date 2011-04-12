__author__="criticus"
__date__ ="$Apr 7, 2011 4:40:15 PM$"

from abstract import GatewayAbstract

class FourInfo(GatewayAbstract):
    "class for FourInfo gateway"

    def set_gateway(self,data):
        self._gateway = {'url'       :"http://gateway.4info.net/msg",
                         'login'     :data['GatewaysLogin'],
                         'passw'     :data['GatewaysPass'],
                         'short_code':data['GatewaysCode']
                         }

    def set_message(self,msg):
        self._message = msg

    def prepare_msg(self):
        message = self._convert_to_ascii(self._message['Message'])
        xml = "<?xml version='1.0'?>"
        xml += "<request clientId='%s' clientKey='%s' type='MESSAGE'>" % (self._gateway['login'],self._gateway['passw'])
        xml += "<message>"
        xml += "<sender>"
        xml += "<type>6</type>"
  	xml += "<id>%s</id>" % (self._gateway['short_code'])
  	xml += "</sender>"
        xml += "<recipient>"
        xml += "<type>5</type>"
        xml += "<id>%s</id>" % (self._message['PhoneNumber'])
        xml += "</recipient>"
        xml += "<text>" + message + "</text>" 
        xml += "</message>"
        xml += "</request>"
       
        return xml

    def parse_response(self,response):
        from xml.dom.minidom import parseString
        import xml.dom.minidom
        try:
            doc = parseString(response)
        except:
            self._success = False
            return 'Empty Response'

        response  = doc.documentElement

        #get Status Id
        status = response.getElementsByTagName("status")
        id_node = status[0].getElementsByTagName('id')[0]
        id = id_node.childNodes[0].data

        if id == '1':
            self._success = True
        else:
            self._success = False

        #get Request Id
        request_node = response.getElementsByTagName('requestId')
        request_id = request_node[0].childNodes[0].data

        return request_id

    def _multiple_replace(self, dic, text):
        import re
        pattern = "|".join(map(re.escape, dic.keys()))
        return re.sub(pattern, lambda m: dic[m.group()], text)

    def _convert_to_ascii(self,text):
        dic = { '&':'&#38;',
                '@':'&#64;',
                '%':'&#37;',
                '$':'&#36;',
                '{':'&#123;',
                '}':'&#125;',
                '*':'&#42;',
                '\n':'&#10;',
                '\r':'&#13;',
                '\t':'&#9;'
              }
        return self._multiple_replace(dic, text)


            