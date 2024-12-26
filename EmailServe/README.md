# EmailServe in HPC

这个东西的功能是使用学校的邮箱系统发送邮件

## 编译
首先在main.py中填写好你自己的信息

```python
sender = 'xxxxxxxx@hust.edu.cn' # 学校邮箱
passwd = 'xxxxxxxxxx'  # 学校邮箱密码
receiver = 'xxxxx@outlook.com'  # 随便一个你其他的常用邮箱用来接收邮件
```

```bash
cd EmailServe
pip install pyinstaller
./build.sh
```


## 添加到系统PATH

```bash
export PATH=$HOME/work/EmailServe/dist:$PATH
```


## 使用

```
email -c "hello world"
```

