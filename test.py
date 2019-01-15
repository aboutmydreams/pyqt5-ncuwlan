import sys, requests, base64, time
from random import choice
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit, QMessageBox



da = {
    1:'login_ok', 
    'E2553': 'Password is error', 
    'E2531': 'User not found', 
    'E2616': 'Arrearage users qianfei',
    'E2532': 'The two authentication interval cannot be less than 10 seconds',
    }

url_list = ['https://www.cnblogs.com/','https://www.coolapk.com/','https://www.w3cschool.cn/','https://www.baidu.com','https://zhidao.baidu.com','https://hanyu.baidu.com', 'http://www.kugou.com','https://www.sina.com.cn/','https://weibo.com/','http://www.sohu.com/','http://site.baidu.com/','https://www.guazi.com','https://open.163.com/','https://www.autohome.com.cn','https://www.imooc.com/','https://modao.cc/','https://jusp.tmall.com','http://www.4399.com/','http://www.tuniu.com/','https://mobile.pconline.com.cn/','http://www.rayli.com.cn/','http://www.hao123.com/zxfy','http://cp.iciba.com/']

t1 = time.time()
def ncuwlan(name,psw):
    t1 = time.time()
    url = 'http://222.204.3.221:804/include/auth_action.php'
    a = base64.b64encode(psw.encode(encoding='utf-8')).decode()
    # print(a,type(a))
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
            return 'ok'
        elif 'E2532' in res:
            print('rest some time')
            time.sleep(12)
            return 'ok'
        elif ('E2531' in res) or ('E2553' in res):
            return 'wrong'
        elif 'Arrearage' in res:
            return 'far'
        else:
            print('something wrong')
            print(res[0:5] + str(da))
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
        print('ncuwlan can not be connected becuuse timeout')
        return 'timeout'

def connect(name,psw):
    while True:
        a_url = choice(url_list)
        try:
            now_res = requests.get(a_url,timeout=10)
            # print(now_res.status_code)
            time.sleep(7)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
            t1 = ncuwlan(name,psw)
            t2 = time.time()
            t3 = time.ctime()
            print('{}s connected with{},now time is {}'.format(str(round(t2-t1,2)),t3,a_url))


class login(QWidget):
    def __init__(self):
        super(login,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("login")
        layout = QGridLayout()
        layout.setColumnMinimumWidth(15,10)
        self.setGeometry(870, 400, 160, 150)

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
        self.alert = QMessageBox()
        self.alert.setText('123133213登录成功')
        self.alert.exec_()

        if ncuwlan(name,psw) == 'ok':
            self.alert = QMessageBox()
            self.alert.setText('登录成功')
            self.alert.exec_()
        elif ncuwlan(name,psw) == 'wrong':
            self.alert = QMessageBox()
            self.alert.setText('用户名或密码错了噢')
            self.alert.exec_()
        elif ncuwlan(name,psw) == 'far':
            self.alert = QMessageBox()
            self.alert.setText('超过范围了噢')
            self.alert.exec_()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = login()
    ex.show()
    sys.exit(app.exec_())







