import socket
import syslog_handle
import re
from opcua import Server



def postData(ip,port,opcserver):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_port = (ip, port)
    print(ip_port)
    sk.bind(ip_port)
    sk.listen(3)
    server = Server()
    opc_server = opcserver
    opc_server = "opc.tcp://" + opc_server + "/freeopcua/server/"
    server.set_endpoint(opc_server)  # 设定服务器URI
    print("OPC服务段地址：" + opc_server)
    uri = 'http://examples.freeopcua.github.io'
    idx = server.register_namespace(uri)  # 注册地址空间
    server.import_xml("log_test.xml")  # 导入自定义的节点类型
    server.start()
    myobj = server.nodes.objects.add_object(idx, "sys")  # 直接实例化对象以及添加变量
    myvar = myobj.add_variable(idx, "Single log", 'null')
    conn, address = sk.accept()
    print(address)

    def upData(str):
        myvar.set_value(str)

    while True:
        data = conn.recv(1024)
        if data == b'quit':
            break
        syslog = syslog_handle.Syslog_Handle(data.decode())
        print(syslog)
        upData(syslog)
    sk.close()

def opc_hadle():
    with open('host.txt', mode='r+', encoding='utf-8')as f:
        for line in f:
            print(line)
            ip = " ".join(re.findall(r'tcpadd=(.*?) ', line, re.S))
            port = int(" ".join(re.findall(r'tcpport=(.*?) ', line, re.S)))
            opcserver = " ".join(re.findall(r'opcserver=(.*)', line, re.S))
    postData(ip, port, opcserver)

