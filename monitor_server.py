import socket, json

Info = {}
Info['IP'] = '127.0.0.1'
Info['UUID'] = '11:11:11:11:11'
Info['PORT'] = [1, 2, 3]

jsonStr = json.dumps(Info)
print(len(jsonStr))
s = socket.socket()

s.connect(('127.0.0.1', 5000))
msg = '''POST /esp_node_register HTTP/1.1
Content-Length: ''' + str(69) + '''
Content-Type: application/x-www-form-urlencoded

info='''+jsonStr
s.send(bytes(msg, 'utf-8'))
data = s.recv(1024)
print(data)
