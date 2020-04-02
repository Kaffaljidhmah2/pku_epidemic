import requests
import json
import urllib
import datetime

###############################

## Part I 必需填写

sid = "" # 学号
pwd = "" # 密码
heath_status = "健康" # 疫情诊断


###############################

## Part II 下面的内容依照个人情况填写。

### 省市区的编号格式 与 身份证前六位的编码格式是对应的，

### 可以百度“xx省xx市xx区 身份证号码前六位” 来获得。
### 如北京市海淀区 身份证号码前六位 为 110108
### 则省编号 = "11"， 市编号 = "01" 区编号 = "08".

addr = "" # 当前所在地地址（不在校则需填写）


mydata = {
    "xh": sid, # 学号 （无需手动填写）
    "sfhx": "n", # 是否回校 (y/n)

    # 回校需填写：
    "hxsj": "", # 回校时间，格式为“20200409 170200” 2020年4月9日17点02分00秒
    "cfdssm": "", # 出发地省编号
    "cfddjsm": "", # 出发地市编号
    "cfdxjsm": "" ,# 出发地区编号
    "sflsss": "" ,# 是否留宿宿舍 (y/n)
    "sfcx": "" , # 是否出校 (y/n)

    # 不在校需填写：
    "dqszdxxdz": urllib.parse.quote(addr), # 当前所在地详细地址，在前面写
    "dqszdsm": "", # 当前所在地省编号
    "dqszddjsm": "", # 当前所在地市编号
    "dqszdxjsm": "", # 当前所在地区编号


    "sfqwhb14": "n", # 14日内是否途径湖北或前往湖北 (y/n)
    "sfjchb14": "n", # 14日内是否接触过来自湖北地区的人员 (y/n)
    "sfqwjw14": "n", # 14日内是否有境外旅居史 (y/n)
    "sfjcjw14": "n", # 14日内是否接触过境外人员 (y/n)


    "jrtw": "37", # 今日体温（如"36.8")
    "sfczzz": "n", # 是否存在病症
    "jqxdgj": "", # 行动轨迹
    "qtqksm": "", # 其他情况说明
    "tbrq": datetime.datetime.now().strftime("%Y%m%d"), # 填报日期，自动生成
    "yqzd": urllib.parse.quote(heath_status), #疫情诊断
    
    # 下面的不知道有什么用

    "dwdzxx":"" , 
    "dwjd":"",
    "dwwd":"",
    "sfdrfj":"",
    "chdfj":"",
    "simstoken":"",
}

########################################


sess = requests.Session()

portal_url = "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do"
login_data = {'appid':"portal2017",'userName':sid, 'password':pwd, 'redirUrl':'https://portal.pku.edu.cn/portal2017/ssoLogin.do'}
r=sess.post(portal_url,login_data)
token = json.loads(r.text)['token']

ssoLogin_url = "https://portal.pku.edu.cn/portal2017/ssoLogin.do?token="+token
res = sess.get(ssoLogin_url)

ep_url = "https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=epidemic"
r=sess.get(ep_url)

link0="https://portal.pku.edu.cn/portal2017/account/insertUserLog.do?portletId=epidemic&portletName=%E7%87%95%E5%9B%AD%E4%BA%91%E6%88%98%E2%80%9C%E7%96%AB%E2%80%9D"
r=sess.get(link0)

Tb_url = "https://ssop.pku.edu.cn/stuAffair/edu/pku/stu/sa/jpf/yqfk/stu/saveMrtb.do"
r = sess.post(Tb_url,data=mydata)
print(r.text)