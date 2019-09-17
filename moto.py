import re
import json
import requests
str0 = input()
level = str0[0] #匹配等级
str1 = str0[1:] #匹配姓名
names = re.search(r'!(.+?),', str1) #正则匹配姓名
name = names.group()
pos = names.span()
name = name[1:-1] #剔除标识位，获得姓名
str2 = str1[pos[1]:] #切片复制剔除冗余信息
repos = re.search(r'\d{11}', str2) #匹配手机号
telnumber = repos.group()
pos = repos.span()
str3 = str2[0:pos[0]] + str2[pos[1]:] #剔除手机号码，得到仅包含地址信息的str3
url = "https://restapi.amap.com/v3/geocode/geo?key=6a6615350026e24aa1c159785e70a709" #使用高德API
urlweb = url + "&address=" + str3 #urlweb为完整API请求链接
webdata = requests.get(urlweb).text #webdata为网站返回数据包
content = json.loads(webdata) #转换为json格式
positon = content["geocodes"][0]["location"] #geocodes为地理编码信息列表，location为坐标点，两者用于逆地理编码
rurl = "https://restapi.amap.com/v3/geocode/regeo?output=JSON&key=6a6615350026e24aa1c159785e70a709&radius=100&extensions=base"
rurlweb = rurl + "&location=" + positon #逆地理编码API
respond = requests.get(rurlweb).text #返回详细地理信息
respond = json.loads(respond) #格式转化
if level == "1":
    city = content["geocodes"][0]["city"]  #geocodes为地理编码信息列表
    township = respond["regeocode"]["addressComponent"]["township"] #regeocode为逆地理编码，addressComponent为地址元素列表，township为坐标点所在乡镇/街道
    rt = re.search( township, str3) #匹配地址
    district = content["geocodes"][0]["district"] #geocodes为地理编码信息列表，district为地址所在的区
    if city == '':
        city = content["geocodes"][0]["province"] #province为地址所在的省份名,这里是直辖市的情况
    if rt == None:
          township = ''
          rdt = re.search( district, str3)
          if rdt == None:
              district = ''
              rc = re.search( city, str3)
              tpos = rc.span()
          else:
              tpos = rdt.span()
    else:
        tpos = rt.span()
    str4 = str3[tpos[1]:-1] #剔除非地址字符，得到详细地址str4
    item = {
        "姓名": name,
        "手机": telnumber,
        "地址": [
            content["geocodes"][0]["province"],
            city,
            district,
            township,
            str4
        ]
    }
    jsondata = json.dumps(item, ensure_ascii=False)
else: #2和3难度作一起考虑
    i = 0
    str5 = str3
    while i < len(str3) - 1:
        i += 1
        if str3[i] == '镇' or str3[i] == '乡':
            str5 = str3[i + 1:]
            break
        elif str3[i] == '街' and str3[i + 1] == '道':
            str5 = str3[i + 2:]
            break
    str4 = str5
    i = 0
    while i < len(str5) - 1:
        i += 1
        if (str5[i] == '号'):
            doornumber = str5[: i]
            str4 = str5[i + 1:]
    i = 0
    while i < len(str5) - 1:
        i += 1
        if (str5[i] == '县' or str5[i] == '区' or str5[i] == '镇' or str5[i] == '乡'):
            str5 = str5[i + 1:]
        elif (str5[i] == '街' and str5[i] == '道'):
            str5 = str5[i + 2:]
    district = content["geocodes"][0]["district"]
    city = content["geocodes"][0]["city"]
    township = respond["regeocode"]["addressComponent"]["township"]
    rd = re.search(r'\d+号', str5) #匹配门牌号
    #road = respond["regeocode"]["addressComponent"]["streetNumber"]["street"] #addressComponent为地址元素列表，streetNumber和street均为字面意思
    road1 = re.search(r'(.*)路|街道|巷', str5)
    if road1 == None :
        road=''
    else :
        road = road1.group()
    rt = re.search( township, str3)
    if city == '':
        city = content["geocodes"][0]["province"]
    if rt == None:
        township = ''
    if rd == None:
        doornumber = ''
        if rt == None:
            township = ''
            rdt = re.search(district, str3)
            if rdt == None:
                district = ''
                rc = re.search( city, str3)
                dpos = rc.span()
            else:
                dpos = rdt.span()
        else:
            dpos = rt.span()
    else:
        doornumber = rd.group()
        dpos = rd.span()
    str4 = str5[dpos[1]:-1] #剔除非地址字符，得到详细地址str4
    item = {
        "姓名": name,
        "手机": telnumber,
        "地址": [
            content["geocodes"][0]["province"],
            city,
            district,
            township,
            road,
            doornumber,
            str4
        ]
    }
    jsondata=json.dumps(item,ensure_ascii=False)
print(jsondata)