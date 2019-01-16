# studypyqt5

da = {
    1:'login_ok', 
    'E2553': 'Password is error', 
    'E2531': 'User not found', 
    'E2616': 'Arrearage users qianfei',
    'E2532': 'The two authentication interval cannot be less than 10 seconds',
    }
## 用户体验层
https://cdn.nlark.com/yuque/0/2019/png/164272/1547546562926-4a108026-1c58-4f95-98ae-e6c81e3718dd.png

## 业务实现层思路
### 使用pyqt5编辑窗口，用户第一次验证时储存信息
通过os.path获取当前路径，在相关目录下创建新的目录或直接在当前目录下创建隐藏文件（.json .txt都可以 加密储存）。

用户第二次登录时，判断是否存在该文件（进行验证），如果存在文件则直接执行检查网络和自动连接。

### 检查网络与发送请求
每隔6秒访问一些相应较快的网页，这样的网页最好准备多一些，这样更礼貌。当访问超时（5s）时，重新发送验证请求。

### 注销
清除  remove 之前存储信息的文件。
