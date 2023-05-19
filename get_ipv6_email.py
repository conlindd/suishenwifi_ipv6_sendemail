import os
import json
import socket
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
import time
import smtplib


def get_ip():

    hostname = socket.gethostname()


    addr_infos = socket.getaddrinfo(hostname, None, socket.AF_INET6)
    ips = set([addr_info[-1][0] for addr_info in addr_infos])
    print(ips)
    # 获取一个ipv6地址列表
    urlText = [ip for ip in ips if ip.startswith("24")] #获取24开头的ipv6地址
    # 给ipv6列表添加http:[]
    global_ips=['http://[' + item + ']' for item in urlText]
    # global_ips = ips
    whether_to_send, send_ip = get_temp_ip(global_ips)
    send_ip = json.dumps(send_ip)
    return whether_to_send, send_ip
    
    
def get_temp_ip(current_ip):
    # temp_ip_json_path = "/var/tmp/ip.json"
    temp_ip_json_path = "ip.json"
    if not os.path.exists(temp_ip_json_path):
        print("没有存储个过ip,发送并存储它.".format(temp_ip_json_path))
        with open(temp_ip_json_path, 'w') as jo:
            json.dump(current_ip, jo)
            return True, current_ip

    else:
        with open(temp_ip_json_path, 'r') as jo:
            origin_ip = json.load(jo)
        if origin_ip == current_ip:
            # print("Current ip {} do not change, no need to send".format(current_ip))
            print("当前ip地址没有改变,不需要发送邮件".format(current_ip))
            return False, current_ip
        else:
            # print("The ip updated from {} to {}, update it.".format(origin_ip, current_ip))
            print("当前ip地址发送改变,发送邮件通知.".format(origin_ip, current_ip))
            os.remove(temp_ip_json_path)
            with open(temp_ip_json_path, 'w') as jo:
                json.dump(current_ip, jo)
                return True, current_ip


    
def send_an_email(email_content): # email_content是一个字符串
    mail_host = "smtp.163.com" # 这个去邮箱找
    mail_user = '1xxxxx0@163.com' #发送的邮件地址
    mail_auth_code = 'YxxxxxxBH' #授权码，不是邮箱的登陆密码
    mail_sender = mail_user # 用mail_user 作为发送人
    mail_receivers = ['1xxxxxx0@qq.com'] #收件人list
    message = MIMEMultipart()
    message['From'] = Header(mail_sender)  # 寄件人
    message['Subject'] = Header("随身wifi的ipv6地址") #主题名字
    message.attach(MIMEText(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'\n', 'plain', 'utf-8')) # 时间
    message.attach(MIMEText('该随身wifi的ipv6地址如下:\n', 'plain', 'utf-8')) # 头信息
    
    # 具体的IPv6地址
    message.attach(MIMEText(email_content, 'plain', 'utf-8'))
    message.attach(MIMEText('\n使用方法:\nhttp://[你的ipv6地址号]:端口号 \n然后输入到浏览器地址栏进行访问', 'plain', 'utf-8')) # 帮助信息
    # print("message is {}".format(message.as_string())) # debug用
    smtpObj = smtplib.SMTP(mail_host)
    # smtpObj.set_debuglevel(1) # 同样是debug用的
    smtpObj.login(mail_user, mail_auth_code) # 登陆
    smtpObj.sendmail(mail_sender, mail_receivers, message.as_string()) # 真正发送邮件就是这里
    
    # main方法
if __name__ == "__main__":
    whether_to_send, global_ips = get_ip()
    if whether_to_send:
        send_an_email(global_ips)
    else:
        print("等待,不发送")