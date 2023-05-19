### 随身wifi  Debian系统获取ipv6地址并发送邮件通知



#### 0.安装python相关的内容

```
root@4G-wifi:~# apt-get install python3 python3-requests python3-gi python3-dbus
```



#### 1.复制本仓库的get_ipv6_email.py文件保存到指定目录/usr/local

```
root@4G-wifi:~# 
root@4G-wifi:~# cd /usr/local
root@4G-wifi:/usr/local# mkdir gipv6
root@4G-wifi:/usr/local# vim get_ipv6_email.py

然后将本项目get_ipv6_email.py文件的内容复制进去

```



#### 2.然后把你的邮箱信息填写进去

```
    mail_host = "smtp.163.com" # 这个去邮箱找
    mail_user = '1xxxxxxx0@163.com' #发送的邮件地址
    mail_auth_code = 'YxxxxxxxxH' #授权码，不是邮箱的登陆密码
    mail_sender = mail_user # 用mail_user 作为发送人
    mail_receivers = ['1xxxxxx70@qq.com'] #收件人list
```



#### 3.给get_ipv6_email.py文件赋权

```
sudo chmod +x get_ipv6_email.py

```



#### 4.设置开机脚本自启动

```
sudo vim /etc/rc.local


把下边这句填入 exit 0上面

/usr/bin/python3 /usr/local/get_ipv6_email.py > /usr/local/get_ipv6_email.log
```



#### 5.最后重启Linux,脚本就能自动运行并打印日志了。



#### 6.可以看到接收的邮箱里有一个邮件,上边会显示你的ipv6地址

```
2023-05-19 07:36:41
该随身wifi的ipv6地址如下:
["http://[2xx:xxx::11eb]"]
```



#### 7.在你的debian上创建网站,然后在浏览器中访问你的ipv6地址:端口号就能访问通了

```
注意访问地址的格式是:
 http:[你的ipv6地址]:端口号
 
例如:
http://[2xx:xxx::11eb]:1526
```



参考:

https://zhuanlan.zhihu.com/p/338190964

https://www.linuxprobe.com/linux-python-auto.html
