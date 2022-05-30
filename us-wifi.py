# -*- coding: utf-8 -*-
import requests
from sys import exit, argv
from time import sleep
from os import popen, remove
from os.path import isfile,dirname
from random import choice
from base64 import b64encode,b64decode
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QGridLayout,  QLineEdit, QMessageBox

# 随机访问的网站，避免大量访问单个网站造成ip被屏蔽
url_list = ['https://www.cnblogs.com/','https://www.coolapk.com/','https://www.w3cschool.cn/','https://www.baidu.com','https://zhidao.baidu.com','https://hanyu.baidu.com', 'http://www.kugou.com','https://www.sina.com.cn/','https://weibo.com/','http://www.sohu.com/','http://site.baidu.com/','https://www.guazi.com','https://open.163.com/','https://www.autohome.com.cn','https://www.imooc.com/','https://modao.cc/','https://jusp.tmall.com','http://www.4399.com/','http://www.tuniu.com/','https://mobile.pconline.com.cn/','http://www.rayli.com.cn/','http://www.hao123.com/zxfy','http://cp.iciba.com/']

# 创建文件用于加密与保存用户数据
def create_file(name,pwd):
    with open('us.txt','w') as f:
        user_data = f"['{name}','{pwd}']"
        base64_data = b64encode(user_data.encode(encoding='utf-8')).decode()
        f.write(base64_data)
    # 以下两行是将文件隐藏，但是在打包后似乎出现了一些权限问题
    # p = popen('attrib +h ' + 'us.txt')
    # p.close()


# 发生联网请求并返回文字说明
def post_data(name,pwd):
    url = 'http://222.204.3.221:804/include/auth_action.php'
    a = b64encode(pwd.encode(encoding='utf-8')).decode()
    data = {
        'action': 'login',
        'username': name,
        'password': '{B}' + a,
        'ac_id': '1',
        'user_ip': '',
        'nas_ip': '',
        'user_mac': '',
        'save_me': 1,
        'ajax': 1,
    }
    try:
        res = requests.post(url,data=data,timeout=5).text
        if 'login_ok' in res:
            # print("connect!")
            return '登录成功~'
        elif 'E2532' in res:
            # print('rest some time')
            return '登录成功 等一小会就好'
        elif ('E2531' in res) or ('E2553' in res):
            return '用户名或密码错了噢'
        elif 'Arrearage' in res:
            return '超过范围了噢'
        elif 'E2833' in res:
            return '地址异常'
        else:
            return str(res)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
        return '无法连接网络'
    except Exception as e:
        return str(e)

# 循环请求 检测是否断网，如果断网（timeout）则从新连，出现未知错误记录error_log.txt,格式为连接次数，请求网址，报错说明
def connect(name,pwd):
    n = 0
    while True:
        a_url = choice(url_list)
        try:
            now_res = requests.get(a_url,timeout=10)
            n+=1
            sleep(7)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
            post_data(name,pwd)
        except Exception as e:
            with open('error_log.txt','a+') as f:
                f.write(str(n) +a_url + str(e))
            return False


class login(QWidget):
    def __init__(self):
        super(login,self).__init__()
        self.initUi()

    #  窗体的UI 一个title 两个文字 两个输入框 一个登录按钮
    def initUi(self):
        self.setWindowTitle("login")
        layout = QGridLayout()
        layout.setColumnMinimumWidth(15,10)
        self.setGeometry(880, 420, 160, 150)  # 窗体位置和大小 前两个是相对于显示桌面的坐标，后两个是窗体的大小

        nameLabel = QLabel("账号")
        nameLabel.setGeometry(30,30,20,20)
        self.nameLineEdit = QLineEdit("")
        pwdLabel = QLabel("密码")
        self.pwdLineEdit = QLineEdit("")

        # layout.setSpacing(10)
        layout.addWidget(nameLabel, 1, 0)
        layout.addWidget(self.nameLineEdit,1,1)
        layout.addWidget(pwdLabel, 2, 0)
        layout.addWidget(self.pwdLineEdit, 2, 1)

        layout.setColumnStretch(1, 10)
        login_btn = QPushButton('登录')
        login_btn.clicked.connect(self.addNum)
        layout.addWidget(login_btn,3,1)
        self.setLayout(layout)

    def addNum(self):
        name = self.nameLineEdit.text()  # 获取文本框内容
        pwd = self.pwdLineEdit.text()
        # print('name: %s pwd: %s ' % (name,pwd))
        tell = post_data(name,pwd)
        if tell in ['登录成功~', '登录成功 等一小会就好']:
            create_file(name,pwd)
            self.alert = QMessageBox()
            self.alert.setText('连接成功，已在后台运行')
            self.alert.exec_()
            connect(name,pwd)
        else:
            # print(tell)
            self.alert = QMessageBox()
            self.alert.setText(tell)
            self.alert.exec_()

    # 自动登入，获取第一次登录成功时保存的用户信息
    def auto_login(self):
        with open('us.txt', 'r') as f:
            user_data = str(b64decode(f.read()), "utf-8")
        data = eval(user_data)
        name, pwd = data[0], data[1]
        tell = post_data(name,pwd)
        self.alert = QMessageBox()
        self.alert.setText(tell)
        self.alert.exec_()
        if tell in ['登录成功~', '登录成功 等一小会就好']:
            connect(name,pwd)
        if tell == '用户名或密码错了噢':
            remove('us.txt')
            self.initUi()


# isfile('us.txt')判断用户是否登录
if __name__ == '__main__':
    app = QApplication(argv)
    if isfile('us.txt'):
        ex = login()
        ex.auto_login()
    else:
        ex = login()
        ex.show()

    exit(app.exec_())

# 现在为了解决第一次登录崩溃的问题，一个思路是线程，一个思路是新建UI窗体，ui与逻辑一定要分开
