import paramiko

class AutoSsh:

    def __init__(self,hostname,username,password):
        self._ssh = self.connect(hostname,username,password)

    def connect(self,hostname,username,password):
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=hostname, port=22, username=username , password= password)
        return ssh

    def exec_command(self,cmd):
        # 执行命令
        stdin, stdout, stderr = self._ssh.exec_command('ls')
        # 获取命令结果
        return stdout.read()

    def close(self):
        # 关闭连接
        self._ssh.close()