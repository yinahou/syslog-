import re
import json

x=0

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

def Type_Manage(syslog):
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

def Type_SYSTEM_STATUS(syslog):
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

with open('syslog_dict.json',mode='r',encoding='utf-8')as f:
    dicts=json.load(f)
    for i in dicts:
        if x==0:
            SYSLOG_Type=i
            x+=1
        elif x==1:
            Manage_remarks=i
            x+=1
        elif x==2:
            System_remarks =i
            x+=1
        elif x==3:
            LEVELS =i
            x+=1
        elif x==4:
            WorkTypes =i



