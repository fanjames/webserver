import socket  
import json
import re
import requests
import subprocess


'''
本机：ssh -NfR 8888:127.0.0.1:8080 root@172.19.167.73
信息外网：ssh -NfL 172.19.167.73:8887:127.0.0.1:8888 127.0.0.1
'''


regex = re.compile(r'\[(.*)\]')


#开启ip和端口
ip_port = ('127.0.0.1', 8080)
#生成句柄
web = socket.socket()
#绑定端口
web.bind(ip_port)
#最多连接数
web.listen(5)
#等待信息
print ('nginx waiting...')
#开启死循环



head = '''HTTP/1.1 200 OK
Content-Type: text/html

<html><body>{content}</body></html>
'''

dingtalk = '''
https://oapi.dingtalk.com/robot/send?access_token=ee5a2ab429f526de063433dc3de99c66ab0b4c8822e5ea82c419e1d4f5cd4df2' \
-H 'Content-Type: application/json' \
-d '
  {"msgtype": "text",
    "text": {
        "content": {content}
     }
  }'
'''
# sp = subprocess.Popen()

dingtalk_url = 'https://oapi.dingtalk.com/robot/send'
params = {'access_token': 'ee5a2ab429f526de063433dc3de99c66ab0b4c8822e5ea82c419e1d4f5cd4df2'}

while True:
    #阻塞
    conn, addr = web.accept()
    # conn.send(bytes('200', 'utf-8'))
    #获取客户端请求数据
    data = conn.recv(1024)
    conn.sendall(bytes(head.format(content='Connected.'), 'utf-8'))
    print(data)

    match = regex.findall(str(data))
    if not match:
        continue

    json_obj = json.loads(match[0].replace('\\n', ''))
    msg = json_obj['labels']

    
    # 向对方发送数据
    r = requests.post('http://requestbin.k8s.lqdl.net/1iwsy0t1', data=msg)
    # r = requests.post(dingtalk_url, data=dingtalk.format(content='我就是我, 是不一样的烟火'))

    payload = {'msgtype': 'text', 
               'text': {'content': msg}
               }
    headers = {'Content-Type': 'application/json'}
    r = requests.post(dingtalk_url, params=params, headers=headers, data=json.dumps(payload))    
    conn.sendall(bytes(head.format(content='Message has been sent.'), 'utf-8'))



    #关闭链接    
    conn.close()



