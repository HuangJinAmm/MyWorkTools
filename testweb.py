import base64
import random
import os
from requests import Request,Response,Session
import yaml
from faker import Faker
import hashlib
import re
import logging
import functools

faker=Faker("zh_CN")
md5 = hashlib.md5()

def get_yaml_property(yaml,property:str,default=None):
    if not isinstance(property,str):
        raise ValueError("wrong property")
    properties = property.strip().split('.')
    cmd = "yaml"
    for pty in properties:
        cmd += ".get('{}')".format(pty)
    try:
        retvar = eval(cmd)
    except Exception as identifier:
        retvar = default
    return retvar

def parseYaml(config_path): 
    if bool(config_path) and os.path.exists(config_path):
        with open("web.yml") as f:
            con = yaml.safe_load(f)
        u = get_yaml_property(con,"web.test",default={})
        ut = TestUser(u.get("url"),u.get("cookie"),u.get("rule"))
        for t in u.get("task"):
            newtask = Task(t.get("path"),t.get("data"),method = t.get("method"))
            ut.tasks.append(newtask)
        ut.doJob()

def getFromCookie(cookie,name):
    pattern = r"(?<={}=)\w+(?=;)".format(name)
    g = re.findall(pattern,cookie) 
    return g[0]

class TestUser:

    def __init__(self,url,cookies,rule=None):
        self._url = url
        self._headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        }
        self._session = Session()
        self._headers["Cookie"] = cookies
        self._headers["Origin"] = url
        self._headers["Host"] = url[6::]
        self._headers["User-Agent"] = faker.user_agent()
        self.tasks = []
        self.rule = rule

    def post(self,url,data=None,files=None):
        r = Request("post",url,header=self._headers,data=data)
        rsp = self._session.send(r)
        return rsp

    def get(self,url,param):
        r = Request("GET",url,params=param)
        rsp = self._session.send(r)
        return rsp

    def doJob(self):
        token = getFromCookie(self._headers["Cookie"],"token")
        for t in self.tasks:
            if bool(self.rule):
                exec("{}({},{})".format(self.rule,'t','token'))
            # yield self.post(dourl,data=data)
            print("===="+self._url+t.path)
            print(t._data)


class Task:

    def __init__(self,path,faker_datas,method = "get"):
        self.path = path
        self.method = method
        self._data = self.applyFakerData(faker_datas)

    def applyFakerData(self,faker_datas):
        retMap={}
        for f,fv in faker_datas.items():
            print(fv)
            if fv.startswith("faker"):
                try:
                    exec_faker = eval("{}()".format(fv))
                    retMap[f]=exec_faker
                except Exception as identifier:
                    retMap[f] = ""
        return retMap

def wo56(t,token):
    urlstr = t.path
    for k,v in t._data.items():
        urlstr = urlstr + "&{}={}".format(k,v)
    signStr = urlstr + token
    md5.update(signStr.encode("utf-8"))
    t._data["sign"] = md5.hexdigest()

class ResponseStatic:

    def __init__(self):
        pass

if __name__ == "__main__":
    parseYaml("web.yml")