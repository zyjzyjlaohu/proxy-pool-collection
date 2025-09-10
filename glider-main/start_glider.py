import subprocess
import os

# 切换到glider-main目录
os.chdir(r"i:\代理池\glider-main")

# 运行glider.exe，使用我们创建的配置文件
subprocess.run(["glider.exe", "-config", "my_config.conf"])