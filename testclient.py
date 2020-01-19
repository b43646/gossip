#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import sys
import pickle

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
# host = socket.gethostname()

# 设置端口号
# port = 60002

# 连接服务，指定主机和端口
s.connect(("127.0.0.1", sys.argv[1]))

# 接收小于 1024 字节的数据

msg = {"version": sys.argv[2]}
s.send(pickle.dumps(msg))

s.close()
