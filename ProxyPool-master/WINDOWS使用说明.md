# Windows系统使用说明

本文档介绍如何在Windows系统中运行ProxyPool代理池。

## 环境准备

在Windows系统中运行ProxyPool，需要安装以下环境：

1. Python 3.6+（推荐Python 3.8或更高版本）
2. Redis（可以使用Windows版Redis或远程Redis服务）
3. Git（可选，用于克隆代码）

## 安装步骤

### 1. 安装Python

从[Python官网](https://www.python.org/downloads/windows/)下载最新的Python安装包并安装。

安装时请勾选"Add Python to PATH"选项，以便在命令行中直接使用Python和pip命令。

### 2. 安装Redis

**方法一：安装Windows版Redis**

从[MicrosoftArchive/redis](https://github.com/MicrosoftArchive/redis/releases)下载Windows版Redis安装包并安装。

**方法二：使用远程Redis服务**

您也可以使用远程Redis服务，无需在本地安装Redis。在代码中的`setting.py`文件中配置远程Redis服务器信息。

### 3. 获取代码

通过Git克隆代码：

```cmd
git clone https://github.com/Python3WebSpider/ProxyPool.git
cd ProxyPool
```

或者直接从GitHub下载ZIP压缩包并解压。

### 4. 安装依赖

在命令提示符中执行以下命令安装依赖：

```cmd
pip install -r requirements.txt
```

如果安装速度较慢，可以使用国内镜像源：

```cmd
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 5. 配置Redis连接

打开`proxypool/setting.py`文件，根据您的Redis环境修改以下配置：

```python
# 如果使用本地Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''  # 如果没有设置密码，保持为空

# 如果使用远程Redis
# REDIS_HOST = 'your_redis_host'
# REDIS_PORT = your_redis_port
# REDIS_PASSWORD = 'your_redis_password'
```

### 6. 运行代理池

在命令提示符中执行以下命令启动代理池：

```cmd
python run.py
```

或者直接双击运行批处理文件：

```
start_proxypool.bat
```

## 快速启动脚本

本项目提供了几个快速启动脚本，您可以根据需要选择使用：

- `simple_start.bat`：简化版启动脚本
- `start_proxypool.bat`：标准启动脚本
- `start_with_env.bat`：带环境变量的启动脚本
- `start_proxy_with_fix.bat`：修复版启动脚本

## 测试代理池

代理池启动后，可以通过以下方式测试是否正常工作：

1. 打开浏览器，访问 [http://localhost:5555/random](http://localhost:5555/random)，如果返回一个代理地址，则表示代理池正常运行。

2. 您也可以使用`examples/usage.py`和`examples/usage2.py`中的示例代码来使用代理池。

## 常见问题

### 1. Redis连接失败

如果出现Redis连接失败的错误，请检查：

- Redis服务是否已启动
- Redis配置是否正确
- 防火墙是否阻止了连接

### 2. 无法获取代理

如果无法获取代理，可能是：

- 代理池中暂时没有可用代理，请等待一段时间
- 代理获取器没有正常工作
- 代理测试器没有正常工作

### 3. 其他问题

如果遇到其他问题，可以查看`logs`目录下的日志文件获取详细错误信息。

## 注意事项

1. Windows系统中运行多进程程序可能会有一些特殊问题，请确保您的Python版本兼容。
2. 如果在Windows系统中遇到多进程相关的错误，可以尝试使用`simple_start.bat`或修改代码使用多线程代替多进程。
3. 定期更新代理池代码以获取最新功能和修复。

祝您使用愉快！