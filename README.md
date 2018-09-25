## 功能
* 自动完成、磁盘分区、扩展 LVM逻辑卷、扩展 root(根)分区。
* 参考文章: http://zongming.net/read-1154

## 注意事项
* 数据无价，执行前请 **务必备份数据**，避免数据丢失造成损失。

## 应用场景
* 适合虚拟化技术中的模板镜像(镜像体积较小)，例如: XenServer / Vmware / KVM 等虚拟化场景。

## 环境
* Python 3

## 条件
* 操作系统: 支持 CentOS 7.x & Ubuntu Server 16.x 。
* 文件系统: 支持 XFS(CentOS 7.2) & EXT4(Ubuntu Server 16.x) 。
* 磁盘，必须已经存在分区表(类型msdos)，并且有大于1GB的可用分区。
* root分区，必须是基于 LVM逻辑卷创建的。

## 使用方法
* 下载代码，保存到指定的路径，例如:
```bash
/root/
```
* 使用 root 权限执行程序:
```bash
cd /root/AutoExtPartition/
python3 demo.py
```

## 验证
* CentOS 系统

![程序执行之前](https://github.com/eastNan/AutoExtPartition/blob/master/doc/pic/auto-fs1.png)
![程序执行之后](https://github.com/eastNan/AutoExtPartition/blob/master/doc/pic/auto-fs2.png)

* Ubuntu 系统

![程序执行之前](https://github.com/eastNan/AutoExtPartition/blob/master/doc/pic/auto-fs3.png)
![程序执行之后](https://github.com/eastNan/AutoExtPartition/blob/master/doc/pic/auto-fs4.png)
