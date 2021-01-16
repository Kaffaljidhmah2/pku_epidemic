import requests
import json
import datetime
import sys
import io

# 改变标准输出的默认编码 不知道为啥windows上乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
###############################
# UserAgent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"

## Part I 必需填写

sid = ""  # 学号
pwd = ""  # 密码
heath_status = "健康"  # 疫情诊断

###############################

## Part II 下面的内容依照个人情况填写。

### 省市区的编号格式 与 身份证前六位的编码格式是对应的，

### 可以百度“xx省xx市xx区 身份证号码前六位” 来获得。
### 如北京市海淀区 身份证号码前六位 为 110108
### 则省编号 = "11"， 市编号 = "01" 区编号 = "08".


mydata = {
    "xh": sid,  # 学号 （无需手动填写）
    "sfhx": "y",  # 是否回校 (y/n)

    # 回校需填写：
    "hxsj": "20200528 150000",  # 回校时间，格式为“20200409 170200” 2020年4月9日17点02分00秒
    "cfdssm": "",  # 出发地省编号
    "cfddjsm": "",  # 出发地市编号
    "cfdxjsm": "",  # 出发地区编号
    "sflsss": "y",  # 是否留宿宿舍 (y/n)
    "sfcx": "n",  # 是否出校 (y/n) （当日是否离开过学校）

    # 不在校需填写：
    "dqszdxxdz": "",  # 当前所在地详细地址
    "dqszdsm": "",  # 当前所在地省编号
    "dqszddjsm": "",  # 当前所在地市编号
    "dqszdxjsm": "",  # 当前所在地区编号

    "sfmjqzbl": "n",  # 是否与确诊病例密接，尚未解除观察
    "sfmjmjz": "n",  # 是否与确诊病例密接者密接，尚未解除观察
    "sfzgfxdq": "n",  # 目前是否居住在中高风险地区

    "jrtw": "36.5",  # 今日体温（如"36.8")
    "sfczzz": "n",  # 是否存在以下症状（发热、咳嗽、腹泻）
    "jqxdgj": "",  # 行动轨迹
    "qtqksm": "无",  # 其他情况说明
    "tbrq": datetime.datetime.now().strftime("%Y%m%d"),  # 填报日期，自动生成
    "yqzd": heath_status,  # 疫情诊断

    # 下面的不知道有什么用 从js里面加了一些字段
    "dqszdgbm": "",
    "dwdzxx": "",
    "dwjd": "",
    "dwwd": "",
    "sfdrfj": "",
    "chdfj": "",
    "simstoken": "",
    "jkm": "绿码",  # 健康码
    "hsjcjg": "",
    "jjgcsj": "",
}

########################################


sess = requests.Session()
sess.headers["User-Agent"] = UA

portal_url = "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do"
login_data = {'appid': "portal2017", 'userName': sid, 'password': pwd,
              'redirUrl': 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'}
r = sess.post(portal_url, login_data, )
token = json.loads(r.text)['token']

ssoLogin_url = "https://portal.pku.edu.cn/portal2017/ssoLogin.do?token=" + token
res = sess.get(ssoLogin_url)

ep_url = "https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=epidemic"
r = sess.get(ep_url)

link0 = "https://portal.pku.edu.cn/portal2017/account/insertUserLog.do?portletId=epidemic&portletName=%E7%87%95%E5%9B%AD%E4%BA%91%E6%88%98%E2%80%9C%E7%96%AB%E2%80%9D"
r = sess.get(link0)

Tb_url = "https://ssop.pku.edu.cn/stuAffair/edu/pku/stu/sa/jpf/yqfk/stu/saveMrtb.do"
r = sess.post(Tb_url, data=mydata)
print(r.text)
# TODO 考虑给自己邮箱发消息告知填报情况


