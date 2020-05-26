# SYSlog日志转换OPC-UA协议脚本
本脚本的作用是将SYSlog日志转为opc-ua协议


代码:https://github.com/yinahou/syslog-opc_ua

#### 目前功能：
##### 1、opc服务端
* 读取SYSlog日志
* 转换SYSlog日志为opc_ua协议
* 上传内容到opc服务器
##### 1、opc客户端
* 读取opc_ua
* 对应密码本将opc_ua内容转换回SYSlog日志

#### 进行中的内容
* 界面设计

### 密码本
```Python
SYSLOG_Type={'System':'1','Manage':'2','SYSTEM_STATUS':'3'}
Manage_remarks={'应用系统基本设置操作':'1','设备加载应用策略操作':'2','用户操作超时自动退出':'3'}
System_remarks={'启动业务处理主程序':'1','启动系统状态采集程序':'2','活动链接':'3','当前工作模式为':'4','开始设置业务规则':'5','设备开始正常工作':'6'}
LEVELS={'启动':'1','系统状态':'2','工作模式':'3','设置规则':'4','工作状态':'5'}
WorkTypes={'代理模式':'1'}
```
* 密码本文件：https://github.com/yinahou/syslog-opc_ua/blob/master/syslog_dict.json

### 测试用例
* tcp测试：https://github.com/yinahou/syslog-opc_ua/blob/master/SYSlog.txt
* 日志处理：https://github.com/yinahou/syslog-opc_ua/blob/master/log_test.xml
* 地址配置文件：https://github.com/yinahou/syslog-opc_ua/blob/master/host.txt

### 使用的包
```Python
import socket
import re
from opcua import Server
import json
```

## 代码详解
### 1、SYSlog处理
https://github.com/yinahou/syslog-opc_ua/blob/master/syslog_handle.py

按不同SYSlog类型定义不同函数处理数据

SYSlog总共有三大类型，定义为`Type_System`,`Type_Manage`,`Type_SYSTEM_STATUS`

针对每种类型定义一个函数，用正则表达式解析SYSlog内容

>#### 1、`Type_System`有4种特殊情况，分类处理
```Python
def Type_System(syslog):
    devip = " ".join(re.findall(r'DEVIP=(.*?) ', syslog, re.S))
    type = " ".join(re.findall(r'Type=(.*?) ', syslog, re.S))
    type=SYSLOG_Type[type]
    time = " ".join(re.findall(r'TIME=(.*?) LEVEL', syslog, re.S))
    level = " ".join(re.findall(r'LEVEL=(.*?) ', syslog, re.S))
    level=LEVELS[level]
    result = " ".join(re.findall(r'RESULT=(.*?) ', syslog, re.S))
    if result=="成功":
        result='1'
    else:
        result='0'
    remark = " ".join(re.findall(r'REMARK=(.*?) ', syslog, re.S))
    opcsyslog=devip+" "+type+" "+time+" "+level+ " "+result

    # 特殊类型描述处理
    if remark[0:4] == "活动链接":
        linknum = " ".join(re.findall(r'活动链接\[(.*?)\]', remark, re.S))
        cpu = " ".join(re.findall(r'CPU利用率\[(.*?)%\]', remark, re.S))
        disk = " ".join(re.findall(r'存储利用率\[(.*?)%\]', remark, re.S))
        mem = " ".join(re.findall(r'内存利用率\[(.*?)%\]', remark, re.S))
        net = " ".join(re.findall(r'隔离通道\[(.*?)\]', remark, re.S))
        if net == "正常":
            net = '1'
        else:
            net = '0'
        netflow = " ".join(re.findall(r'实时吞吐量\[(.*?)bps\]', remark, re.S))
        remark='3'
        opcsyslog=opcsyslog+" "+remark+" "+linknum+" "+cpu+" "+disk+" "+mem+" "+net+" "+netflow
    elif remark[0:7] == "当前工作模式为":
        worktype = " ".join(re.findall(r'当前工作模式为\[(.*?)\]', remark, re.S))
        worktype=WorkTypes[worktype]
        remark='4'
        opcsyslog= opcsyslog+" "+remark+" "+worktype
    elif remark[0:9] == "启动业务处理主程序":
        sys = " ".join(re.findall(r'启动业务处理主程序\[(.*?)\]', remark, re.S))
        version = " ".join(re.findall(r'\(ver:(.*?)\)', remark, re.S))
        remark='1'
        opcsyslog = opcsyslog + " " +remark+" "+sys+" "+version
    else:
        remark=System_remarks[remark]
        opcsyslog=opcsyslog+" "+remark
    isout = " ".join(re.findall(r'ISOUT=(.*)', syslog))
    opcsyslog = opcsyslog+" "+isout
    return opcsyslog
```

>#### 2、`Type_Manage`
```Python
devip = " ".join(re.findall(r'DEVIP=(.*?) ', syslog, re.S))
    type = " ".join(re.findall(r'Type=(.*?) ', syslog, re.S))
    type = SYSLOG_Type[type]
    time = " ".join(re.findall(r'TIME=(.*?) USER', syslog, re.S))
    user=" ".join(re.findall(r'USER=(.*?) ', syslog, re.S))
    event=" ".join(re.findall(r'EVENT=(.*?) ', syslog, re.S))
    result = " ".join(re.findall(r'RESULT=(.*?) ', syslog, re.S))
    if result == "成功":
        result = '1'
    else:
        result = '0'
    remark = " ".join(re.findall(r'REMARK=(.*)', syslog))
    remark=Manage_remarks[remark]
    opcsyslog = devip+" "+type+" "+time+" "+user+" "+event+" "+result+" "+remark
    return opcsyslog
```

>#### 3、`Type_SYSTEM_STATUS`
```Python
devip = " ".join(re.findall(r'DEVIP=(.*?) ', syslog, re.S))
    type = " ".join(re.findall(r'Type=(.*?) ', syslog, re.S))
    type = SYSLOG_Type[type]
    time = " ".join(re.findall(r'TIME=(.*?) LINKNUM', syslog, re.S))
    linknum=" ".join(re.findall(r'LINKNUM=(.*?) ', syslog, re.S))
    cpu=" ".join(re.findall(r'CPU=(.*?) ', syslog, re.S))
    disk=" ".join(re.findall(r'DISK=(.*?) ', syslog, re.S))
    mem=" ".join(re.findall(r'MEM=(.*?) ', syslog, re.S))
    net=" ".join(re.findall(r'NET=(.*?) ', syslog, re.S))
    netflow=" ".join(re.findall(r'NETFLOW=(.*?) ', syslog, re.S))
    devstatus=" ".join(re.findall(r'DEVSTATUS=(.*?) ', syslog, re.S))
    isout = " ".join(re.findall(r'ISOUT=(.*)', syslog))
    opcsyslog= devip+" "+type+" "+time+" "+linknum+" "+cpu+" "+disk+" "+mem+" "+net+" "+netflow+" "+devstatus+" "+isout
    return opcsyslog
```

>#### 4、最后设函数`Syslog_Handle`统合三种类型的SYSlog
```Python
def Syslog_Handle(syslog):
    opcsyslog=""
    type = " ".join(re.findall(r'Type=(.*?) ', syslog, re.S))
    if type=="System":
        opcsyslog = Type_System(syslog)
    elif type == "Manage":
        opcsyslog = Type_Manage(syslog)
    elif type =="SYSTEM_STATUS":
        opcsyslog = Type_SYSTEM_STATUS(syslog)
    return opcsyslog
```

### 2、向OPC_UA服务器发送数据
https://github.com/yinahou/syslog-opc_ua/blob/master/opc_server.py

数据已经由SYSlog处理为OPC-UA格式，只需传输到服务器

>#### 1、从host.txt文件中读取IP，端口以及服务器信息。
```Python
def opc_hadle():
    with open('host.txt', mode='r+', encoding='utf-8')as f:     # 从host配置文件读取配置信息
        for line in f:
            print(line)
            ip = " ".join(re.findall(r'tcpadd=(.*?) ', line, re.S))
            port = int(" ".join(re.findall(r'tcpport=(.*?) ', line, re.S)))
            opcserver = " ".join(re.findall(r'opcserver=(.*)', line, re.S))
    postData(ip, port, opcserver)
```

>#### 2、定义postdata函数用于向服务器发送数据
>>##### (1)、创建套接字，绑定套接字到本地IP与端口
```Python
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
>>##### (2)、套接字绑定的IP与端口
```Python
    ip_port = (ip, port)
    print(ip_port)
    sk.bind(ip_port)
```
>>##### (3)、开始TCP监听
```Python
sk.listen(3)
```
>>##### (4)、设定服务器URI,注册地址空间,直接实例化对象以及添加变量
```Python
    server.set_endpoint(opc_server)  # 设定服务器URI
    uri = 'http://examples.freeopcua.github.io'
    idx = server.register_namespace(uri)  # 注册地址空间
    server.import_xml("log_test.xml")  # 导入自定义的节点类型
    server.start()
    myobj = server.nodes.objects.add_object(idx, "sys")  # 直接实例化对象以及添加变量
    myvar = myobj.add_variable(idx, "Single log", 'null')
    conn, address = sk.accept()
```
>>##### (5)、定义upData函数用于循环内调用，传送数据
```Python
    def upData(str):
        myvar.set_value(str)
```
>>##### (6)、建立循环使用syslog_handle.py中的Syslog_Handle函数处理数据并用upData函数发送
```Python
    while True:
        data = conn.recv(1024)
        if data == b'quit':
            break
        syslog = syslog_handle.Syslog_Handle(data.decode())
        print(syslog)
        upData(syslog)
    sk.close()
```

### 3、OPC客户端（测试用）
https://github.com/yinahou/syslog-opc_ua/blob/master/opc_server.py

调用
```Python
import json
```
密码本：
```Python
SYSLOG_Type={'System':'1','Manage':'2','SYSTEM_STATUS':'3'}
Manage_remarks={'应用系统基本设置操作':'1','设备加载应用策略操作':'2','用户操作超时自动退出':'3'}
System_remarks={'启动业务处理主程序':'1','启动系统状态采集程序':'2','活动链接':'3','当前工作模式为':'4','开始设置业务规则':'5','设备开始正常工作':'6'}
LEVELS={'启动':'1','系统状态':'2','工作模式':'3','设置规则':'4','工作状态':'5'}
WorkTypes={'代理模式':'1'}
```

数据写入：
```Python
dict_list=[]
dict_list.append(SYSLOG_Type)
dict_list.append(Manage_remarks)
dict_list.append(System_remarks)
dict_list.append(LEVELS)
dict_list.append(WorkTypes)
x=0
with open('syslog_dict.json',mode='w',encoding='utf-8')as f:
    json.dump(dict_list,f)
    
```

数据读取：
```Python
with open('syslog_dict.json',mode='r',encoding='utf-8')as f:
    dicts=json.load(f)
    for i in dicts:
        if x==0:
            print("SYSLOG_Type")
            print(i)
            x+=1
        elif x==1:
            print("Manage_remarks")
            print(i)
            x+=1
        elif x==2:
            print("System_remarks")
            print(i)
            x+=1
        elif x==3:
            print("LEVELS")
            print(i)
            x+=1
        elif x==4:
            print("WorkTypes")
            print(i)
```
