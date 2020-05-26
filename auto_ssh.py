import paramiko

class AutoSsh:

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

    def close(self):
        self.__transport.close()

    def upload(self,local_path,target_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path,target_path)

    def cmd(self, command):
        if(not bool(self._ssh)):
            self._ssh = paramiko.SSHClient()
        self._ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr =self._ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print(result.decode("utf-8"))
        return result

def test():
    host = "120.78.86.71"
    username ="query"
    password = "query123"
    asvn = AutoSsh(host,username,password)
    asvn.cmd("ls")
    asvn.cmd("cd logs")
    asvn.cmd("ls -al")
    asvn.close()

if __name__ == "__main__":
    test()