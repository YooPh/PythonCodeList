#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import poplib

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
def get_header(msg):
    for header in ['Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
            elif header in ['From','To']:
                hdr, addr = parseaddr(value)
                name = decode_str(addr)
                value=name
        print( value)
# 头部信息已取出


# 获取邮件的字符编码，首先在message中寻找编码，如果没有，就在header的Content-Type中寻找
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos+8:].strip()
    return charset


if __name__ == '__main__':
    # 输入邮件地址, 口令和POP3服务器地址:
    from_email = "massway01@msw-auto.com"
    from_email_pwd = "Cam21130607"
    pop_server = "pop.qiye.aliyun.com"

    server = poplib.POP3(pop_server)
    server.set_debuglevel(1)
    # 设置实例的调试级别。这控制打印的调试输出量。默认值0不产生调试输出。值1产生适量的调试输出，通常每个请求都有一行。值2或更高会产生最大调试输出量，记录在控制连接上发送和接收的每行。
    # print(server.getwelcome().decode("utf-8"))
    # 欢迎信息
    # 登录
    server.user(from_email)
    server.pass_(from_email_pwd)
    resp, mails, octets = server.list() # 返回邮件数量和每个邮件的大小

    for i in range(1,10):

        resp, lines, octets = server.retr(i)    # 返回由参数标识的邮件的全部文本
        msg_content = b"\r\n".join(lines).decode("utf-8","ignore") # byte字符串
        msg = Parser().parsestr(msg_content)    # 解析为普通字符串

        get_header(msg)

    server.quit()