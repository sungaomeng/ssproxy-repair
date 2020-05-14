#!/usr/bin/env python
#coding=utf-8

import os, time, sys
import slb, check, dns

##### 以下变量请根据自己的情况补充 ####
#AK信息
access_key_id = '';
access_key_secret = '';

#区域ID, 我这里是新加坡
region_id= 'ap-southeast-1'

#监听端口
port = 8388

#带宽峰值
bandwidth = '50'

#后端服务器ID
backend_servers_id = "i-t4n190***y3d0"

#探测地址
host = 'ss.test.com'

###################################

#解析域名, 获取IP地址
host_ip = check.ParsingDomainName(host)

#检查IP Port是否正常
result = check.CheckSocket(host_ip, port)

if 0 == result:
    print ("Domain:%s HostIp:%s Port:%s is open, exit." % (host, host_ip, port))
    sys.exit(0)
else:
    print ("Domain:%s HostIp:%s Port:%s is not open, return code：%s" % (host, host_ip, port, result))
    print("Prepare to create a new load balancing, Please wait ... ")

    #创建负载均衡
    new_load_balancer_info = slb.CreateLoadBalancer(access_key_id, access_key_secret, region_id)
    new_load_balancer_id = new_load_balancer_info['LoadBalancerId']
    new_load_balancer_ip = new_load_balancer_info['Address']
    # print (new_load_balancer_id, new_load_balancer_ip)

    #向负载均衡添加后端服务器
    slb.AddBackendServers(access_key_id, access_key_secret, region_id, new_load_balancer_id, backend_servers_id)

    #创建监听端口
    slb.CreateLoadBalancerTCPListenerRequest(access_key_id, access_key_secret, region_id, new_load_balancer_id, port, bandwidth)

    #启动监听端口
    slb.StartLoadBalancerListenerRequest(access_key_id, access_key_secret, region_id, new_load_balancer_id, port)


# 10s 后检查新建立的SLB端口是否通
print("Wait 10 seconds to check the new load balancing again ...")
time.sleep( 10 )

result = check.CheckSocket(new_load_balancer_ip, port)
if 0 == result:
    print("New LoadBalancer:%s Port:%s is open" % (new_load_balancer_ip, port))

    ### 准备删除旧SLB
    # 查询旧负载均衡的ID
    old_load_balancer_id = slb.DescribeLoadBalancers(access_key_id, access_key_secret, region_id, backend_servers_id, host_ip)

    # 根据ID删除旧负载均衡
    slb.DeleteLoadBalancer(access_key_id, access_key_secret, region_id, old_load_balancer_id)

    # 去DNS里更新A记录
    dns.UpdateDNS(access_key_id, access_key_secret, host, host_ip, new_load_balancer_ip)

    # 更新本地Hosts, 防止DNS更新不及时导致一直检测旧IP
    dns.UpdateHosts(new_load_balancer_ip, host)

else:
    print("New LoadBalancer:%s Port:%s is not open，return code：%s" % (new_load_balancer_ip, port, result))


    # Domain:ss.roobo.net HostIp:161.**.**.186 Port:8388 is not open, return code：35
    # Prepare to create a new load balancing, Please wait ...
    # New LoadBalancer:lb-t4nupa5f9w2ynfzsqkjo1 create successful.
    # New LoadBalancer:lb-t4nupa5f9w2ynfzsqkjo1 add backendserver:i-t4n190***y3d0 successful.
    # New LoadBalancer:lb-t4nupa5f9w2ynfzsqkjo1 create listener port:8388 successful.
    # New LoadBalancer:lb-t4nupa5f9w2ynfzsqkjo1 start listener port:8388 successful.
    # Wait 10 seconds to check the new load balancing again ...
    # New LoadBalancer:161.**.**.196 Port:8388 is open
    # Old LoadBalancer:lb-t4n9hdg5***houyedj delete successful.
    # DNS update record successful domain:ss.test.com, old ip:161.**.**.186, new ip:161.**.**.196