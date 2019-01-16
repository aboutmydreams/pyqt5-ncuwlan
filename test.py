# -*- coding: utf-8 -*-
import sys, requests, base64, time, os
from random import choice
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit, QMessageBox

url_list = ['https://www.cnblogs.com/','https://www.coolapk.com/','https://www.w3cschool.cn/','https://www.baidu.com','https://zhidao.baidu.com','https://hanyu.baidu.com', 'http://www.kugou.com','https://www.sina.com.cn/','https://weibo.com/','http://www.sohu.com/','http://site.baidu.com/','https://www.guazi.com','https://open.163.com/','https://www.autohome.com.cn','https://www.imooc.com/','https://modao.cc/','https://jusp.tmall.com','http://www.4399.com/','http://www.tuniu.com/','https://mobile.pconline.com.cn/','http://www.rayli.com.cn/','http://www.hao123.com/zxfy','http://cp.iciba.com/']

t1 = time.time()

def create_file(name,psw):
    file_name ='us.txt'
    f = open(file_name,'w')
    user_data = '[{},{}]'.format(name,psw,)
    base64_data = base64.b64encode(user_data.encode(encoding='utf-8')).decode()
    f.write(base64_data)
    f.close()
    p = os.popen('attrib +h ' + file_name)
    p.close()

def ncuwlan(name,psw):
    t1 = time.time()
    url = 'http://222.204.3.221:804/include/auth_action.php'
    a = base64.b64encode(psw.encode(encoding='utf-8')).decode()
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
            print("connect!")
            return '登录成功~'
        elif 'E2532' in res:
            print('rest some time')
            time.sleep(12)
            return '稍等一会哟'
        elif ('E2531' in res) or ('E2553' in res):
            return '用户名或密码错了噢'
        elif 'Arrearage' in res:
            return '超过范围了噢'
        else:
            print('something wrong')
            return str(res)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
        print('ncuwlan can not be connected becuuse timeout')
        return '无法连接网络'
    except Exception as e:
        return str(e)

def connect(name,psw):
    while True:
        a_url = choice(url_list)
        try:
            now_res = requests.get(a_url,timeout=10)
            # print(now_res.status_code)
            time.sleep(7)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
            ncuwlan(name,psw)
        except Exception as e:
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
        self.nameLineEdit = QLineEdit(" ")
        pswLabel = QLabel("密码")
        self.pswLineEdit = QLineEdit(" ")

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
        print('name: %s psw: %s ' % (name,psw))


        tell = ncuwlan(name,psw)
        if (tell == '登录成功~') or (tell == '稍等一会哟'):
            create_file(name,psw)
            connect(name,psw)
            self.alert = QMessageBox()
            self.alert.setText(tell)
            self.alert.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = login()
    ex.show()
    sys.exit(app.exec_())







