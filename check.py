#!/usr/bin/env python
# coding:utf-8

def CheckSocket(host, port):
   """
      检查IP Port是否正常
   :param host:
   :param port:
   :return:
   """

   import select
   import socket

   timeout = 10 * 1  # 10s

   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   # 设置连接超时
   sock.settimeout(timeout)

   #发起连接
   result = sock.connect_ex((host, port))

   return result

def ParsingDomainName(host):
   """
   解析域名, 获取IP地址
   :param host:
   :return:
   """

   import socket

   host_ip = socket.gethostbyname(host)

   return host_ip
