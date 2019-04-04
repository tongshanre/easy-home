# encoding:utf-8
import json
import socket
'''
ESP8266 消息处理引擎：协议（UDP）,消息格式（JSON）
{
   type:CTL/DATA/HEART  # 控制消息、数据消息、心跳
   code:          #消息分类
        CTL:      1, AP热点控制
                  2,
        DATA:     1, IO端口控制, port:1
                  2,
        HEART:    无用
   data:          # 消息类型
   response:      # 消息响应 200正常，其他错误
   error:          # 错误信息
}
'''


class MSG:
    @staticmethod
    def get_msg():
        msg = {'type': '', 'code': -1, 'data': '', 'response': 0, 'error': ''}
        return msg

    @staticmethod
    def get_data_msg():
        msg = MSG.get_msg()
        msg['type'] = 'DATA'
        return msg

    @staticmethod
    def get_ctr_msg():
        msg = MSG.get_msg()
        msg['type'] = 'CTR'
        return msg

    @staticmethod
    def get_heart_msg():
        msg = MSG.get_msg()
        msg['type'] = 'HEART'
        return msg

    @staticmethod
    def get_error_msg(error):
        msg = MSG.get_msg()
        msg['response'] = 400
        msg['error'] = error
        return msg

    @staticmethod
    def json_to_str(msg):
        return json.dumps(msg)

    @staticmethod
    def str_to_json(json_str):
        return json.loads(json_str)

'''
    连接服务端工具类
'''
class GPIO_Client:

    @staticmethod
    def sendData(address, gpio, value):
        msg = MSG.get_data_msg()
        msg['type'] = 'DATA'
        msg['code'] = 1
        msg['data'] = str(gpio) + '-' + str(value)
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cs.connect(address)
            cs.send(bytes(json.dumps(msg), 'utf-8'))
            cs.settimeout(200)
            buffer = cs.recv(1024)
            rMsg = MSG.str_to_json(str(buffer, 'utf-8'))
            if(200 == rMsg['response']):
                return True
            else:
                return False
        except OSError:
            return False
        finally:
            cs.close()

    @staticmethod
    def sendHeart(address):
        msg = MSG.get_heart_msg()
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cs.connect(address)
            cs.send(bytes(json.dumps(msg), 'utf-8'))
            cs.settimeout(200)
            buffer = cs.recv(1024)
            rMsg = MSG.str_to_json(str(buffer, 'utf-8'))
            if (200 == rMsg['response']):
                return True
            else:
                return False
        except OSError:
            return False
        finally:
            cs.close()
