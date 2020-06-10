import os
import sys
import re

#文件路径分隔符
if sys.platform=='win32':
    FSep = r'\\'
else:
    FSep = r'\/'

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
        self.rdict = {
            "A":list(),
            "C":list(),
            "D":list(),
            "I":list(),
            "M":list(),
            "?":list(),
            "!":list(),
        }

    #从默认url更新文件
    #默认更新整个项目
    #参数为子目录或文件的相对路径
    def update(self,*args):
        cmd = "svn update"
        for o in self._psh(cmd,args):
            print(o)

    def revert(self,*args):
        cmd = "svn revert"
        for o in self._psh(cmd,args):
            print(o)

    def commit(self,msg = ""):
        args = self.rdict.get("M")
        if len(args)>0:
            cmd = "svn commit -m " + msg
            for o in self._psh(cmd,args):
                print(o)

    def add(self):
        cmd = "svn add"
        args = self.rdict.get("?")
        for out in self._psh(cmd,args):
            print(out)

    #查看状态
    def status(self,*args,foldfilter=[],filefilter=[],full = False,update_msg=False):
        print("*"*50+"查询状态"+"*"*50)
        cmd = "svn status"
        if full: cmd = cmd + " -v"
        if update_msg: cmd = cmd + " -u"
        out = self._psh(cmd,args)
        if len(foldfilter)==0 and len(filefilter) == 0 :
            outfilter = bool
        else:
            d = "|".join(foldfilter)
            f = "|".join(filefilter)
            res = r"^[ACDIM?!].+?{f}({fold}).*?\.({file})$".format(f=FSep,fold=d,file=f)
            pat = re.compile(res)
            outfilter = pat.match
        for o in out:
            print(o)
            o= o.replace('\n','')
            if outfilter(o):
                splitO = o.split(' ')
                self.rdict.get(splitO[0]).append(splitO[7])

    def status_linux(self,*args,foldfilter=[],filefilter=[],full = False,update_msg=False):
        cmd = "svn status"
        if full: cmd = cmd + " -v"
        if update_msg: cmd = cmd + " -u"
        d = "|".join(foldfilter)
        f = "|".join(filefilter)
        if len(foldfilter)==0 and len(filefilter) == 0 :
            grep=""
        else:
            grep = r"|grep -P '^[ACDIM?!].+\/({fold}).+\.({file})$'".format(fold = d,file = f)
        out = self._psh(cmd,args,append= grep)
        for o in out:
            so = o.replace('\n','').split(' ')
            self.rdict.get(so[0]).append(so[7])
            print(o)
    #查看日志
    def log(self,*args):
        cmd = "svn log"
        for o in self._psh(cmd,args):
            print(o)

    def info(self,*args):
        print("*"*100)
        cmd = "svn info"
        for o in self._psh(cmd,args):
            print(o)
    #检出
    def checkout(self):
        print("*"*50+"检出"+"*"*50)
        if not self.usr:
            self.pw = input("username")
        if not self.pw:
            self.pw = input("password")
        if bool(self.url) and bool(self.localPath):
            for i in sh("svn","co",self.url,self.localPath,"--username "+self.usr,"--password "+self.pw):
                print(i)
        else:
            print("no url or localpath")

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

class Maven:

    def __init__(self):
        self.path = r"D:\work-project\upload-jar"
        self.up_url = r"http://192.168.0.250:8081/repository/maven-releases/"
        self.dId = "maven-releases"
        self._cmd = r"mvn deploy:deploy-file "
        self.id_rule = "[\w-]+(?=-\d)"
        self.version_rule = "(?<=-)[\d\.]+"

    def parse(self,path,dr,file):
        file_name,file_ext = os.path.splitext(file)
        id_result = re.findall(self.id_rule,file_name)
        version_result = re.findall(self.version_rule,file_name)
        cmd_map = dict()
        cmd_map["gid"] = dr
        cmd_map["id"] = id_result[0]
        cmd_map["version"] = version_result[0]
        cmd_map["ext"] = file_ext[1::]
        cmd_map["file_path"] = os.path.join(path,file)
        cmd_map["url"] = self.up_url
        cmd_map["did"] = self.dId
        self._cmd = self._cmd + "-DgroupId={gid} -DartifactId={id} -Dversion={version} -Dpackaging={ext} -Dfile={file_path} -Durl={url} -DrepositoryId={did}".format_map(cmd_map)

    def upload(self):
        # sh(self._cmd)
        print(self._cmd)

    def scan(self):
        for root,dir_names,files in os.walk(self.path):
            for dr in dir_names:
                sub_path = os.path.join(root,dr)
                for file in os.listdir(sub_path):
                    self.parse(sub_path,dr,file)
                    self.upload()


def test():
    mvn = Maven()
    mvn.scan()
    # ########
    # root_dev = r"D:\work-project\plat\dev"
    # root_rm = r"D:\work-project\ld\dev"

    # ########
    # devSvn = Svn(root_dev)
    # rmSvn = Svn(root_rm)

    # tskList = [devSvn,rmSvn]
    # ########
    # for tsk in tskList:
    #     tsk.info()
    #     # tsk.update()
    #     tsk.status()
    #     # tsk.status(filefilter=["java","js","html","xml"],foldfilter=["src","html"])

if __name__ == "__main__":
    test()
