import requests,time
from base64 import b64encode
import os 
import sys

def ping_baidu():
    # print(backinfo)
    return os.system('ping -c 1 -w 1 www.baidu.com')

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
            return 'connect'
        elif 'E2532' in res:
            # print('rest some time')
            time.sleep(15)
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


res = ping_baidu()
print('-'*100)
print(res)
print('-'*100)

n = 1
while 1:
    if ping_baidu() != 0:
        # 断网情况返回 512，联网情况返回 0 
        log = post_data('123456','123456')
        time.sleep(5)
        n+=1
        print('-'*20,n,'-'*20)
        if log != 'connect':
            flog = open('log.txt','w')
            flog.write(str(log))
