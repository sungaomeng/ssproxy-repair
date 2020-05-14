## Python检测负载均衡并自动更新
##### 项目地址 [GitHub](https://github.com/sungaomeng/ssproxy-repair)


### 脚本说明

这个脚本是用来自动修复基于阿里云搭建的Ss服务


- 在阿里云新加坡地区购买了一台低配ECS,搭建了Ss服务端

- 由于阿里云经常封杀端口或者公网IP，所以我前面用一个公网负载均衡作为入口 (这样封杀的时候就是封杀的负载均衡了)

- 脚本检测到负载均衡的端口或者IP被封后, 会自动创建一个新的负载均衡并建立监听端口, 然后更新DNS及Hosts记录并删除旧负载均衡

- 一套流程下来, 虽然有一定的延时, 但基本能自动化操作修复, 不用人为干预了。
### 前提条件
- 全部基于阿里云
- 阿里云ECS、负载均衡、云解析DNS
### 脚本流程
``` bash
├── README.md
├── requirements.txt
├── check.py # 检查相关函数, 检查域名的端口是否正常,通过域名解析IP
├── dns.py   # 阿里云云解析DNS相关函数, 查询/修改DNS记录, 更新本地Hosts
├── main.py  # 主程序入口,集合其他脚本函数
└── slb.py   # 阿里云负载均衡相关函数, 创建/删除负载均衡,创建/启动监听端口,添加后端服务器

0 directories, 6 files
```

1. main.py中定义阿里云相关变量 及 "host" 变量 (负载均衡公网IP对应的域名 或者直接写IP，如果写IP请注释DNS相关函数调用，建议域名)
2. 检查域名对应端口是否正常，正常则退出，否则新建负载均衡、添加后端服务器、建立监听、启动监听
3. 等待10s后再次检查新负载均衡的IP对应端口是否正常，正常则删除旧负载均衡并更新DNS后退出，否则打印log后退出

### 依赖

- Python 3 (我的环境是3.5.2)
- Crontab
- 以及一些python依赖见requirements.txt

### 使用

``` bash
$ git clone https://github.com/sungaomeng/ssproxy-repair.git
$ pip install -r ssproxy-repair/requirements.txt

# 校时
$ echo "* * * * * /usr/sbin/ntpdate ntp.aliyun.com" >> /var/spool/$User
# 每半小时执行一次检查
$ echo "*/30 * * * * /usr/bin/python /root/ssproxy-repair/main.py >> /tmp/ssproxy-repair.log 2>&1" >> /var/spool/$User
```

### 日志

目前并没有输出到log, 仅是打印到前台

```
Domain:ss.roobo.net HostIp:161.**.**.186 Port:8388 is not open, return code：35
Prepare to create a new load balancing, Please wait ...
New LoadBalancer:lb-t4nupa5f9w2ynfzsqkjo1 create successful.
New LoadBalancer:lb-t4nupa5f9w2ynfzsqkjo1 add backendserver:i-t4n190***y3d0 successful.
New LoadBalancer:lb-t4nupa5f9w2ynfzsqkjo1 create listener port:8388 successful.
New LoadBalancer:lb-t4nupa5f9w2ynfzsqkjo1 start listener port:8388 successful.
Wait 10 seconds to check the new load balancing again ...
New LoadBalancer:161.**.**.196 Port:8388 is open
Old LoadBalancer:lb-t4n9hdg5***houyedj delete successful.
DNS update record successful domain:ss.test.com, old ip:161.**.**.186, new ip:161.**.**.196
Hosts update record successful domain:ss.test.com, new ip:161.**.**.196
```
