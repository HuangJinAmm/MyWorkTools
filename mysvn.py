import os
import re

STATUS = {
    "no_change":' ',
    "add":'A',
    "conflicted":'C', 
    "Deleted":'D',
    "Ignored":'I', 
    "Modified ":'M',
    "noversion":'?',
    "miss":'!',
}

def sh(*args):
    #构建命令
    if len(args) == 1:
        command = args[0]
    else:
        command = " ".join(args)
    print("-->"+command)
    with os.popen(command) as out:
        #逐行产生输出结果
        for r in out:
            yield r

#SVN对象:
#   每个对象对应一组路径
#   远程路径url:"snv://xxxxx"
#   本地路径locaPath:"/path/to/your/project"
class Svn(object):


    def __init__(self,localPath,url = '',usr='',pw=''):
        self.url = url
        self.localPath = localPath
        self.usr = usr
        self.pw = pw

    #从默认url更新文件
    #默认更新整个项目
    #参数为子目录或文件的相对路径
    def update(self,*args,filter = None):
        cmd = "svn update"
        if filter != None:
            try:
                args = filter(args)
            except Exception as e:
                print(e)
        for o in self._psh(cmd,args):
            print(o)

    def revert(self,*args):
        cmd = "svn revert"
        for o in self._psh(cmd,args):
            print(o)

    def commit(self,*args,msg = "",filter = None):
        cmd = "svn commit -m " + msg
        if filter != None:
            try:
                args = filter(args)
            except Exception as e:
                print(e)
        for o in self._psh(cmd,args):
            print(o)

    def _add(self,*args,filter = None):
        cmd = "svn add"
        if filter != None:
            try:
                args = filter(args)
            except Exception as e:
                print(e)
        for o in self._psh(cmd,args):
            print(o)

    #查看状态
    def status(self,*args,foldfilter=[],filefilter=[],full = False,update_msg=False):
        rdict = {
            "A":list(),
            "C":list(),
            "D":list(),
            "I":list(),
            "M":list(),
            "?":list(),
            "!":list(),
        }
        cmd = "svn status"
        if full: cmd = cmd + " -v"
        if update_msg: cmd = cmd + " -u"
        out = self._psh(cmd,args)
        if len(foldfilter)==0 and len(filefilter) == 0 :
            outfilter = bool
        else:
            d = "|".join(foldfilter)
            f = "|".join(filefilter)
            res = "^[ACDIM?!].+\/({fold}).+\.({file})$".format(fold=d,file=f)
            pat = re.compile(res)
            outfilter = pat.match
        for o in out:
            if outfilter(o):
                so = o.replace('\n','').split(' ')
                rdict.get(so[0]).append(so[7])
                print(o)
        return rdict

    def status_linux(self,*args,foldfilter=[],filefilter=[],full = False,update_msg=False):
        rdict = {
            "A":list(),
            "C":list(),
            "D":list(),
            "I":list(),
            "M":list(),
            "?":list(),
            "!":list(),
        }
        cmd = "svn status"
        if full: cmd = cmd + " -v"
        if update_msg: cmd = cmd + " -u"
        d = "|".join(foldfilter)
        f = "|".join(filefilter)
        if len(foldfilter)==0 and len(filefilter) == 0 :
            grep=""
        else:
            grep = "|grep -P '^[ACDIM?!].+\/({fold}).+\.({file})$'".format(fold = d,file = f)
        out = self._psh(cmd,args,append= grep)
        for o in out:
            so = o.replace('\n','').split(' ')
            rdict.get(so[0]).append(so[7])
            print(o)
        return rdict
    #查看日志
    def log(self,*args):
        cmd = "svn log"
        for o in self._psh(cmd,args):
            print(o)

    def info(self,*args):
        cmd = "svn info"
        for o in self._psh(cmd,args):
            print(o)
    #检出
    def checkout(self):
        for i in sh("svn","co",self.url,self.localPath,"--username "+self.usr,"--password "+self.pw):
            print(i)

    #批量执行sh并打印
    def _psh(self,cmd,args,append=""):
        if len(args) == 0:
            for out in sh(cmd,self.localPath,append):
                yield out
        for a in args:
            p = os.path.join(self.localPath,a)
            print("="*60)
            for out in sh(cmd,p,append):
                yield out

def test():
    root ="/media/hj/_dde_data/javaProject/plat-dev" 
    URL = "svn://121.199.65.29:8888/4pl/rd/code/dev/web/plateform"
    fold = ["sv/src","web/src","web/html","common/src"]
    
    rootsvn = Svn(root)
    # rootsvn.status_linux(filefilter=["java","js"],foldfilter=["sv","web","common"])
    r = rootsvn.status()
    print(r)
    # rootsvn.info()
    # rootsvn.update()
    # rootsvn.checkout()

if __name__ == "__main__":
    test()