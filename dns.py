#!/usr/bin/env python
#coding=utf-8

def DescribeDomainRecords(access_key_id, access_key_secret, domain_name, subdomain_name, old_host_ip):
    """
    查询域名A记录的相关信息#
    :param access_key_id:
    :param access_key_secret:
    :param host:
    :param host_ip:
    :return:
    """

    import json
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest

    client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')

    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain_name)
    request.set_RRKeyWord(subdomain_name)
    request.set_ValueKeyWord(old_host_ip)

    response = client.do_action_with_exception(request)

    response_str = str(response, encoding='utf-8')
    response_json = json.loads(response_str)
    subdomain_record_id = response_json['DomainRecords']['Record'][0]['RecordId']

    return subdomain_record_id
    # # python2:  print(response)
    # print(str(response, encoding='utf-8'))


def UpdateDomainRecord(access_key_id, access_key_secret, subdomain_record_id, subdomain_name, new_load_balancer_ip):
    """
    更新域名记录值
    :param access_key_id:
    :param access_key_secret:
    :param subdomain_record_id:
    :param subdomain_name:
    :param new_load_balancer_ip:
    :return:
    """

    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ClientException
    from aliyunsdkcore.acs_exception.exceptions import ServerException
    from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

    client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')

    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    request.set_RecordId(subdomain_record_id)
    request.set_RR(subdomain_name)
    request.set_Type("A")
    request.set_Value(new_load_balancer_ip)

    response = client.do_action_with_exception(request)

    # python2:  print(response)
    # print(str(response, encoding='utf-8'))

def UpdateDNS(access_key_id, access_key_secret, host, old_host_ip, new_load_balancer_ip):
    """
    更新DNS
    :param access_key_id:
    :param access_key_secret:
    :param host:
    :param host_ip:
    :return:
    """

    import tldextract
    ext = tldextract.extract(host)
    subdomain_name = ext.subdomain
    domain_name = ext.domain + '.' + ext.suffix

    #查询
    subdomain_record_id = DescribeDomainRecords(access_key_id, access_key_secret, domain_name, subdomain_name, old_host_ip)
    # print (subdomain_record_id)
    UpdateDomainRecord(access_key_id, access_key_secret, subdomain_record_id, subdomain_name, new_load_balancer_ip)
    print("DNS update record successful domain:%s, old ip:%s, new ip:%s " % (host, old_host_ip, new_load_balancer_ip))