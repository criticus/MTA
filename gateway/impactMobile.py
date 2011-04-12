__author__="criticus"
__date__ ="$Apr 7, 2011 4:40:15 PM$"

from abstract import GatewayAbstract

class ImpactMobile(GatewayAbstract):
    "class for Impact Mobile gateway"
    
    def set_gateway(self,data):
        headers = {"Content-type":"text/xml; charset=UTF-8",
                   "X-XIAM-Provider-ID":data['GatewaysLogin']
                  }
        self._gateway = {'url'       :"http://websvcs1.jumptxt.com/smsxml/collector",
                         'short_code':data['GatewaysCode'],
                         'headers'   :headers
                         }

    def set_message(self,msg):
        self._message = msg

    def prepare_msg(self):
        import uuid
        unique_id = str(uuid.uuid1())
        import cgi
        message = cgi.escape(self._message['Message'])

        xml = "<?xml version='1.0' encoding='UTF-8'?>"
        xml += "<!DOCTYPE xiamSMS SYSTEM 'xiamSMSMessage.dtd'>"
        xml += "<xiamSMS>"
        xml += "<submitRequest id='" + unique_id + "'>"
        xml += "<from>+%s</from>" % (self._gateway['short_code'])
        xml += "<to>+1%s</to>" % (self._message['PhoneNumber'])
        xml += "<content type='text'>" + message + "</content>"
        xml += "<sendOnGroup value='" + self._message['OperatorsID'] +"'/>"
        xml += "<requestDeliveryReport value='yes'/>"
        xml += "</submitRequest>"
        xml += "</xiamSMS>"
       
        return xml

    def parse_response(self,response):
        from xml.dom.minidom import parseString
        import xml.dom.minidom
        try:
            doc = parseString(response)
        except:
            self._success = False
            return str(Exception)

        response  = doc.documentElement

        try:
            response_status = response.getAttribute('status').lower()
            result_status = response.firstChild.firstChild.getAttribute('status').lower()
        except:
            self._success = False
            return 'Invalid XML in Response'
        
        if response_status == 'fail':
            self._success = False
            return response.getAttribute('statusText')
        elif response_status == 'ok' and result_status != 'ok':
            self._success = False
            return  response.firstChild.firstChild.getAttribute('statusText')
        elif response_status == 'ok' and result_status == 'ok':
            self._success = True
            return response.firstChild.getAttribute('id')
        else:
            self._success = False
            return 'Invalid XML in Response'