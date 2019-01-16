# -*- coding: utf-8 -*-
import requests
from sys import exit, argv
from time import sleep
from os import popen, remove
from os.path import isfile,dirname
from random import choice
from base64 import b64encode,b64decode
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QGridLayout,  QLineEdit, QMessageBox

# now_path = dirname(__file__)
# up_path = dirname(now_path) + '/'
# fn = up_path.replace('\\','/')
# file_name = fn + 'us.txt'
url_list = ['https://www.cnblogs.com/','https://www.coolapk.com/','https://www.w3cschool.cn/','https://www.baidu.com','https://zhidao.baidu.com','https://hanyu.baidu.com', 'http://www.kugou.com','https://www.sina.com.cn/','https://weibo.com/','http://www.sohu.com/','http://site.baidu.com/','https://www.guazi.com','https://open.163.com/','https://www.autohome.com.cn','https://www.imooc.com/','https://modao.cc/','https://jusp.tmall.com','http://www.4399.com/','http://www.tuniu.com/','https://mobile.pconline.com.cn/','http://www.rayli.com.cn/','http://www.hao123.com/zxfy','http://cp.iciba.com/']

def create_file(name,psw):
    f = open('us.txt','w')
    user_data = "['{}','{}']".format(name,psw,)
    base64_data = b64encode(user_data.encode(encoding='utf-8')).decode()
    f.write(base64_data)
    f.close()
    # p = popen('attrib +h ' + 'us.txt')
    # p.close()

def ncuwlan(name,psw):
    url = 'http://222.204.3.221:804/include/auth_action.php'
    a = b64encode(psw.encode(encoding='utf-8')).decode()
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
            sleep(1)
            return '稍等一会哟'
        elif ('E2531' in res) or ('E2553' in res):
            return '用户名或密码错了噢'
        elif 'Arrearage' in res:
            return '超过范围了噢'
        elif 'E2833' in res:
            return '地址异常'
        else:
            # print('something wrong')
            return str(res)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
        # print('ncuwlan can not be connected becuuse timeout')
        return '无法连接网络'
    except Exception as e:
        return str(e)
# 请求并返回文字说明

def connect(name,psw):
    n = 0
    while True:
        a_url = choice(url_list)
        try:
            now_res = requests.get(a_url,timeout=10)
            # print(now_res.status_code)
            n+=1
            sleep(7)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
            ncuwlan(name,psw)
        except Exception as e:
            f = open('error_log.txt','a+')
            f.write(str(n) + str(e))
            f.close()
            return False


class login(QWidget):
    def __init__(self):
        super(login,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("login")
        layout = QGridLayout()
        layout.setColumnMinimumWidth(15,10)
        self.setGeometry(880, 420, 160, 150)

        nameLabel = QLabel("账户")
        nameLabel.setGeometry(50,50,20,20)
        self.nameLineEdit = QLineEdit("")
        pswLabel = QLabel("密码")
        self.pswLineEdit = QLineEdit("")

        # layout.setSpacing(10)
        layout.addWidget(nameLabel, 1, 0)
        layout.addWidget(self.nameLineEdit,1,1)
        layout.addWidget(pswLabel, 2, 0)
        layout.addWidget(self.pswLineEdit, 2, 1)

        layout.setColumnStretch(1, 10)
        save_Btn = QPushButton('登录')
        save_Btn.clicked.connect(self.addNum)
        layout.addWidget(save_Btn,3,1)
        self.setLayout(layout)

    def addNum(self):
        name = self.nameLineEdit.text()  # 获取文本框内容
        psw = self.pswLineEdit.text()
        #print('name: %s psw: %s ' % (name,psw))
        tell = ncuwlan(name,psw)
        if (tell == '登录成功~') or (tell == '稍等一会哟'):
            create_file(name,psw)
            self.alert = QMessageBox()
            self.alert.setText('连接成功，已在后台运行')
            self.alert.exec_()
            connect(name,psw)
        else:
            # print(tell)
            self.alert = QMessageBox()
            self.alert.setText(tell)
            self.alert.exec_()

    def auto_login(self):
        f = open('us.txt', 'r')
        user_data = str(b64decode(f.read()), "utf-8")
        f.close()
        data = eval(user_data)
        name, psw = data[0], data[1]
        tell = ncuwlan(name,psw)
        self.alert = QMessageBox()
        self.alert.setText(tell)
        self.alert.exec_()
        if (tell == '登录成功~') or (tell == '稍等一会哟'):
            connect(name,psw)
        if tell == '用户名或密码错了噢':
            remove('us.txt')
            self.initUi()

if __name__ == '__main__':
    app = QApplication(argv)
    if isfile('us.txt'):
        ex = login()
        ex.auto_login()
        exit(app.exec_())
    else:
        ex = login()
        ex.show()
        exit(app.exec_())

# 现在为了解决哪一个问题，一个思路是线程，一个思路是新建UI窗体，ui与逻辑一定要分开
