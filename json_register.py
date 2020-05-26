import json
SYSLOG_Type={'System':'1','Manage':'2','SYSTEM_STATUS':'3'}
Manage_remarks={'应用系统基本设置操作':'1','设备加载应用策略操作':'2','用户操作超时自动退出':'3'}
System_remarks={'启动业务处理主程序':'1','启动系统状态采集程序':'2','活动链接':'3','当前工作模式为':'4','开始设置业务规则':'5','设备开始正常工作':'6'}
LEVELS={'启动':'1','系统状态':'2','工作模式':'3','设置规则':'4','工作状态':'5'}
WorkTypes={'代理模式':'1'}
dict_list=[]
dict_list.append(SYSLOG_Type)
dict_list.append(Manage_remarks)
dict_list.append(System_remarks)
dict_list.append(LEVELS)
dict_list.append(WorkTypes)
x=0
with open('syslog_dict.json',mode='w',encoding='utf-8')as f:
    json.dump(dict_list,f)

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
