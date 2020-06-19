import paramiko
from paramiko.py3compat import u
import sys,os,socket,select
import time

class Ssh:

    def __init__(self, host, username,pwd,port=22):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None
        self._ssh = None
        self.connect()

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport
        if(not bool(self._ssh)):
            self._ssh = paramiko.SSHClient()
        self._ssh._transport = self.__transport

    def close(self):
        self.__transport.close()

    def upload(self,local_path,target_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path,target_path)

    def cmd(self, command):
        # 执行命令
        stdin, stdout, stderr =self._ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print(result.decode("utf-8"))
        return result

    def auto_sh(self,scripts):
        chan = self.__transport.open_session()
        chan.get_pty()
        chan.invoke_shell()
        chan.settimeout(1)
        for cmd in scripts:
            chan.sendall(cmd + "\n")
            while True:
                try:
                    x = u(chan.recv(1024))  # Python3用这个
                    if len(x) == 0:
                        print('\r\n*** EOF\r\n')
                        break
                    sys.stdout.write(x)   # 写入缓冲区
                    sys.stdout.flush()    # 刷新，将缓冲区内容显示出来
                except socket.timeout:
                    break
        chan.close()
        self.__transport.close()
        self._ssh.close()

class AutoScript:

    def __init__(self,ssh):
        assert(isinstance(ssh,Ssh))
        self._ssh = ssh

    def run(self):
        result =  self._ssh.cmd("ls logs/4pl | grep 0528.log")
        res = result.split("\n")
        for rs in res:
            cmd = "cat logs/4pl/{} | grep -A50 10:51:31".format(rs)
            self._ssh.cmd(cmd)
        self._ssh.close()

def test():
    # host = "120.78.86.71"
    # username ="query"
    # password = "query123"
    # s = Ssh(host,username,password)
    # ass = AutoScript(s)
    # ass.run()
    r = envoy.run("dir")
    print(r.status_code)
    print(r.std_err)
    print(r.std_out)

if __name__ == "__main__":
    test()