#!/usr/bin/python3


import socket
import yaml
import pickle
# import random


class GossipService(object):
    def __init__(self):
        self.version = {"version": 0}
        self.hosts_table = []
        self.next_host = ""

    def random_server(self, localhost):
        with open('config.yaml', 'r') as f:
            config = yaml.load(f)
            # localhost == True，该函数产生随机产生peer节点信息
            if localhost:
                return config["current_host"], config["current_port"]
            else:
                length = len(config["peers"])
                for i in range(length):
                    # if i == 0:
                    #     num = random.randint(0, length - 1) % 2
                    # else:
                    #     num = i
                    num = i
                    if config["peers"][num]["host"] not in self.hosts_table:
                        self.hosts_table.append(config["peers"][num]["host"])
                        return config["peers"][num]["host"], config["peers"][num]["port"]
                self.hosts_table = [config["peers"][0]["host"]]
                self.next_host = config["peers"][0]["name"]
                return config["peers"][0]["host"], config["peers"][0]["port"]

    def start_send(self, host, port):
        # 创建 socket 对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        # 发送数据
        msg = pickle.dumps(self.version)
        s.send(msg)
        s.close()

    def start_receiver(self, host, port):
        receiver = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        receiver.bind((host, port))
        receiver.listen(1024)
        while True:
            cli, addr = receiver.accept()
            buf = cli.recv(1024)
            version = pickle.loads(buf)
            if int(self.version["version"]) < int(version["version"]):
                self.version = version
                host, port = self.random_server(False)
                try:
                    self.start_send(host=host, port=port)
                    print("连接地址: %s, version: %s" % (str(addr), self.version["version"]))
                except Exception as inst:
                    print(inst)
                    self.update_config()
                    host, port = self.random_server(False)
                    self.start_send(host=host, port=port)
                    print("连接地址: %s, version: %s" % (str(addr), self.version["version"]))

    def update_config(self):
        with open('config.yaml', 'r') as f:
            config = yaml.load(f)
            for i in config["peers"]:
                if self.next_host == i["name"]:
                    config["peers"].remove(i)
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)

    def start(self):
        host, port = self.random_server(True)
        self.start_receiver(host=host, port=port)


if __name__ == "__main__":
    gs = GossipService()
    gs.start()
