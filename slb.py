#!/usr/bin/env python
#coding=utf-8

def CreateLoadBalancer(access_key_id, access_key_secret,region_id):
    """
    创建负载均衡
    :param access_key_id:
    :param access_key_secret:
    :return:
    """

    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkslb.request.v20140515.CreateLoadBalancerRequest import CreateLoadBalancerRequest

    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = CreateLoadBalancerRequest()
    request.set_accept_format('json')

    request.set_AddressType("internet")
    request.set_InternetChargeType("paybytraffic")
    request.set_LoadBalancerName("ssproxy")
    request.set_PayType("PayOnDemand")
    request.set_AddressIPVersion("ipv4")

    response = client.do_action_with_exception(request)
    # response = b'{"LoadBalancerName":"ssproxy","RequestId":"528DF913-D101-4806-A46B-0FC8D35C81A6","ResourceGroupId":"rg-acfm3dhve34laua","Address":"161.117.32.186","VpcId":"","NetworkType":"classic","VSwitchId":"","AddressIPVersion":"ipv4","LoadBalancerId":"lb-t4n9hdg5paj2sihouyedj"}'

    response_str = str(response, encoding='utf-8')
    response_dict = eval(response_str)

    print ("New LoadBalancer:%s create successful." % response_dict['LoadBalancerId'])

    return (response_dict)


def AddBackendServers(access_key_id, access_key_secret, region_id, load_balancer_id, backend_servers_id):
    """
    向负载均衡添加后端服务器
    :param access_key_id:
    :param access_key_secret:
    :param region_id:
    :param load_balancer_id:
    :param backend_servers_id:
    :return:
    """

    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkslb.request.v20140515.AddBackendServersRequest import AddBackendServersRequest

    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = AddBackendServersRequest()
    request.set_accept_format('json')

    request.set_LoadBalancerId(load_balancer_id)
    # request.set_BackendServers(backend_servers)
    request.set_BackendServers("[{\"ServerId\": \"%s\", \"Weight\": \"100\", \"Type\": \"ecs\", \"Description\": \"proxy\"}]" % backend_servers_id)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    # print(str(response, encoding='utf-8'))
    print ("New LoadBalancer:%s add backendserver:%s successful." % (load_balancer_id, backend_servers_id))


def CreateLoadBalancerTCPListenerRequest(access_key_id, access_key_secret, region_id, load_balancer_id, port, bandwidth):
    """
    创建监听端口
    :param access_key_id:
    :param access_key_secret:
    :param region_id:
    :param load_balancer_id:
    :param port:
    :param bandwidth:
    :return:
    """

    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkslb.request.v20140515.CreateLoadBalancerTCPListenerRequest import CreateLoadBalancerTCPListenerRequest

    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = CreateLoadBalancerTCPListenerRequest()
    request.set_accept_format('json')

    request.set_ListenerPort(port)
    request.set_Bandwidth(bandwidth)
    request.set_LoadBalancerId(load_balancer_id)
    request.set_BackendServerPort(port)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    # print(str(response, encoding='utf-8'))
    print ("New LoadBalancer:%s create listener port:%s successful." % (load_balancer_id, port))

def StartLoadBalancerListenerRequest(access_key_id, access_key_secret, region_id, load_balancer_id, port):
    """
    启动监听端口
    :param access_key_id:
    :param access_key_secret:
    :param region_id:
    :param load_balancer_id:
    :param port:
    :return:
    """

    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkslb.request.v20140515.StartLoadBalancerListenerRequest import StartLoadBalancerListenerRequest

    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = StartLoadBalancerListenerRequest()
    request.set_accept_format('json')

    request.set_ListenerPort(port)
    request.set_LoadBalancerId(load_balancer_id)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    # print(str(response, encoding='utf-8'))
    print ("New LoadBalancer:%s start listener port:%s successful." % (load_balancer_id, port))



def DescribeLoadBalancers(access_key_id, access_key_secret, region_id, backend_servers_id, host_ip):
    """
    查询旧负载均衡的ID
    :param access_key_id:
    :param access_key_secret:
    :param region_id:
    :param backend_servers_id:
    :param host_ip:
    :return:
    """

    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest

    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = DescribeLoadBalancersRequest()
    request.set_accept_format('json')

    request.set_ServerId(backend_servers_id)
    request.set_Address(host_ip)

    response = client.do_action_with_exception(request)

    response_str = str(response, encoding='utf-8')
    response_dict = eval(response_str)

    return (response_dict['LoadBalancers']['LoadBalancer'][0]['LoadBalancerId'])
    # python2:  print(response)
    # print(str(response, encoding='utf-8'))


def DeleteLoadBalancer(access_key_id, access_key_secret, region_id, load_balancer_id):
    """
    根据ID删除旧负载均衡
    :param access_key_id:
    :param access_key_secret:
    :param region_id:
    :param load_balancer_id:
    :return:
    """

    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkslb.request.v20140515.DeleteLoadBalancerRequest import DeleteLoadBalancerRequest

    client = AcsClient(access_key_id, access_key_secret, region_id)

    request = DeleteLoadBalancerRequest()
    request.set_accept_format('json')

    request.set_LoadBalancerId(load_balancer_id)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    # print(str(response, encoding='utf-8'))
    print("Old LoadBalancer:%s delete successful." % load_balancer_id)