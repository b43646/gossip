# gossip
实现简单的gossip的机制--尚需完善


## 示例执行步骤

在单台服务器上，通过开启多个窗口来模拟集群，分别运行以下命令行

节点1
`[root@hadoop001 demo1]# python3.6 main.py`

节点2
`[root@hadoop001 demo2]# python3.6 main.py`

节点3
`[root@hadoop001 demo3]# python3.6 main.py`


执行客户端发送数据
`[root@hadoop001 ~]# python3.6 testclient.py 60002 1`

检查各个节点接收的数据是否一致。
每个节点应该收到类似以下的消息，其中version值必须一致
`连接地址: ('127.0.0.1', 53052), version: 1`


#### 故障测试

终止demo2的应用,查看当前集群中每个节点是否仍然可以接收到一致的消息。

执行客户端程序

`[root@hadoop001 ~]# python3.6 testclient.py 60001 3`

其中某个节点应接收以下类似的信息
```
[Errno 111] Connection refused
连接地址: ('127.0.0.1', 53056), version: 3
```

TODO:
统一消息格式，完成节点的动态增删以及动态路由机制
