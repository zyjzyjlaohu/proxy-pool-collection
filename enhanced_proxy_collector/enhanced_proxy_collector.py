import base64
from concurrent.futures import ThreadPoolExecutor
import socket
import warnings
import time
import json
import os
import requests

warnings.filterwarnings("ignore")

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 配置参数
CONFIG = {
    "fofa_email": "15263284687@163.com",
    "fofa_key": "c77484c6157fbeb48652288c6f4fa5a6",
    "max_workers": 100,
    "connect_timeout": 3,
    "test_timeout": 6,
    "search_queries": [
        # 原始SOCKS5无认证代理语法
        "protocol==\"socks5\" && \"Version:5 Method:No Authentication(0x00)\" && country=\"CN\"",
        # 用户提供的新语法1
        "title=\"代理池网页管理界面\"",
        # 用户提供的新语法2
        "body=\"get all proxy from proxy pool\"",
        # 其他可能的代理相关语法
        'url=".*all/"',
        "protocol==\"socks5\" && country=\"CN\""
    ],
    "test_urls": [
        "https://www.baidu.com/",
        "https://www.qq.com/",
        "https://www.163.com/"
    ]
}

# 文件名配置 - 使用脚本所在目录作为输出目录
FILES = {
    "fofa_results": os.path.join(script_dir, "enhanced_fofa_results.txt"),
    "open_ports": os.path.join(script_dir, "enhanced_open_ports.txt"),
    "valid_proxies": os.path.join(script_dir, "enhanced_valid_proxies.txt"),
    "user_dict": os.path.join(script_dir, "user.txt"),
    "pass_dict": os.path.join(script_dir, "pass.txt")
}

# 读取用户名和密码字典
def load_credentials():
    usernames = []
    passwords = []
    
    try:
        with open(FILES["user_dict"], 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"用户名字典文件 {FILES['user_dict']} 不存在，使用默认值")
        usernames = ["test", "guest", "admin", "user"]
    
    try:
        with open(FILES["pass_dict"], 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"密码字典文件 {FILES['pass_dict']} 不存在，使用默认值")
        passwords = ["123456", "admin123", "password"]
    
    return usernames, passwords

# 对搜索查询进行base64编码
def encode_query(query):
    return base64.b64encode(query.encode('utf-8')).decode('utf-8')

# 从Fofa API爬取数据
def fetch_fofa_data():
    if not CONFIG["fofa_key"]:
        print("Fofa API Key 未设置，无法爬取数据")
        return
    
    # 清空之前的结果文件
    open(FILES["fofa_results"], 'w').close()
    
    all_proxies = set()  # 使用集合去重
    
    for query in CONFIG["search_queries"]:
        print(f"正在使用语法 '{query}' 爬取 Fofa 数据")
        encoded_query = encode_query(query)
        
        # 构建Fofa API URL - 修正格式
        url = f"https://fofa.info/api/v1/search/all?email={CONFIG['fofa_email']}&key={CONFIG['fofa_key']}&qbase64={encoded_query}&size=5000"
        
        try:
            print(f"正在请求URL: {url}")
            response = requests.get(url, timeout=30)
            
            # 检查响应状态
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                continue
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"无法解析响应为JSON: {response.text}")
                continue
            
            # 检查API错误
            if data.get('error'):
                print(f"Fofa API 错误: {data['error']}")
                print(f"错误消息: {data.get('errmsg', '无详细错误信息')}")
                continue
            
            if data.get('size', 0) == 0:
                print("未找到符合条件的结果")
                continue
            
            if 'results' not in data or not data['results']:
                print("结果列表为空")
                continue
            
            # 提取代理信息
            for result in data['results']:
                # 不同语法返回的结果结构可能不同，尝试多种方式提取IP和端口
                if isinstance(result, list) and len(result) > 0:
                    proxy_candidate = result[0]
                else:
                    proxy_candidate = str(result)
                
                # 尝试从结果中提取IP:PORT格式的代理
                if ':' in proxy_candidate and '.' in proxy_candidate:
                    parts = proxy_candidate.split(':')
                    if len(parts) >= 2:
                        # 提取IP和端口部分
                        ip_part = ':'.join(parts[:-1])  # 处理可能包含冒号的IPV6
                        port_part = parts[-1]
                        
                        # 尝试清理IP部分，移除可能的协议前缀
                        if '://' in ip_part:
                            ip_part = ip_part.split('://')[-1]
                        
                        # 简单验证IP和端口格式
                        if '.' in ip_part and port_part.isdigit():
                            proxy = f"{ip_part}:{port_part}"
                            all_proxies.add(proxy)
        except Exception as e:
            print(f"爬取数据时出错: {str(e)}")
            # 暂停一段时间后继续
            time.sleep(2)
            continue
    
    # 将去重后的结果写入文件
    with open(FILES["fofa_results"], 'w', encoding='utf-8') as f:
        for proxy in all_proxies:
            f.write(proxy + '\n')
    
    print(f"Fofa数据爬取完毕，共获取 {len(all_proxies)} 个去重后的代理，结果已保存到 {FILES['fofa_results']}")

# 测试端口是否开放
def test_port(proxy):
    proxy = proxy.strip()
    if not proxy or ':' not in proxy:
        return
    
    try:
        ip, port = proxy.split(':', 1)  # 只分割第一个冒号，处理IPV6
        if not port.isdigit():
            return
        
        port = int(port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(CONFIG["connect_timeout"])
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            with open(FILES["open_ports"], 'a', encoding='utf-8') as f:
                f.write(f"{ip}:{port}\n")
        
        sock.close()
    except Exception:
        pass

# 批量测试端口开放情况
def check_ports():
    # 清空之前的结果文件
    open(FILES["open_ports"], 'w').close()
    
    try:
        with open(FILES["fofa_results"], 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{FILES['fofa_results']} 文件不存在，请先运行数据爬取")
        return
    
    print(f"正在测试 {len(proxies)} 个代理的端口开放情况")
    
    with ThreadPoolExecutor(max_workers=CONFIG["max_workers"]) as executor:
        executor.map(test_port, proxies)
    
    # 统计开放的端口数量
    try:
        with open(FILES["open_ports"], 'r', encoding='utf-8') as f:
            open_count = len(f.readlines())
    except FileNotFoundError:
        open_count = 0
    
    print(f"端口检测完毕，共发现 {open_count} 个开放的端口，结果已保存到 {FILES['open_ports']}")

# 测试代理的有效性
def test_proxy(proxy):
    proxy = proxy.strip()
    if not proxy or ':' not in proxy:
        return
    
    usernames, passwords = load_credentials()
    success = False
    
    # 尝试不同的测试URL
    for test_url in CONFIG["test_urls"]:
        # 1. 尝试无密码代理
        try:
            response = requests.get(
                test_url,
                proxies={'http': f"socks5://{proxy}", 'https': f"socks5://{proxy}"},
                timeout=CONFIG["test_timeout"],
                verify=False
            )
            
            if response.status_code == 200:
                print(f'[有效代理] 无密码: {proxy} (测试URL: {test_url})')
                with open(FILES["valid_proxies"], 'a', encoding='utf-8') as f:
                    f.write(f"socks5://{proxy}\n")
                success = True
                break
        except Exception:
            pass
        
        # 如果已经找到有效代理，跳过后续测试
        if success:
            break
    
    # 如果无密码代理测试失败，尝试使用用户名和密码
    if not success:
        for username in usernames:
            for password in passwords:
                try:
                    proxy_url = f"socks5://{username}:{password}@{proxy}"
                    response = requests.get(
                        CONFIG["test_urls"][0],  # 使用第一个URL进行认证测试
                        proxies={'http': proxy_url, 'https': proxy_url},
                        timeout=CONFIG["test_timeout"] / 2,  # 认证测试使用较短的超时时间
                        verify=False
                    )
                    
                    if response.status_code == 200:
                        print(f'[有效代理] 带认证: {proxy} | 用户名: {username} | 密码: {password}')
                        with open(FILES["valid_proxies"], 'a', encoding='utf-8') as f:
                            f.write(f"{proxy_url}\n")
                        success = True
                        break
                except Exception:
                    pass
                
            if success:
                break
    
    if not success:
        print(f'[无效代理] {proxy}')

# 批量测试代理有效性
def check_proxies():
    # 清空之前的结果文件
    open(FILES["valid_proxies"], 'w').close()
    
    try:
        with open(FILES["open_ports"], 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{FILES['open_ports']} 文件不存在，请先运行端口检测")
        return
    
    print(f"正在测试 {len(proxies)} 个代理的有效性")
    
    # 使用较少的线程以避免连接过多
    with ThreadPoolExecutor(max_workers=min(50, CONFIG["max_workers"])) as executor:
        executor.map(test_proxy, proxies)
    
    # 统计有效代理数量
    try:
        with open(FILES["valid_proxies"], 'r', encoding='utf-8') as f:
            valid_count = len(f.readlines())
    except FileNotFoundError:
        valid_count = 0
    
    print(f"代理检测完毕，共发现 {valid_count} 个有效代理，结果已保存到 {FILES['valid_proxies']}")

# 主函数
def main():
    print("=== 增强版代理收集工具启动 ===")
    
    # 1. 从Fofa爬取数据
    fetch_fofa_data()
    
    # 2. 测试端口开放情况
    check_ports()
    
    # 3. 测试代理有效性
    check_proxies()
    
    print("=== 增强版代理收集工具完成 ===")
    
    # 4. 显示统计信息
    try:
        with open(FILES["fofa_results"], 'r') as f:
            total_count = len(f.readlines())
        with open(FILES["open_ports"], 'r') as f:
            open_count = len(f.readlines())
        with open(FILES["valid_proxies"], 'r') as f:
            valid_count = len(f.readlines())
            
        print(f"\n统计信息:")
        print(f"- 总爬取代理数: {total_count}")
        print(f"- 端口开放数: {open_count}")
        print(f"- 有效代理数: {valid_count}")
        print(f"- 有效率: {valid_count/total_count*100:.2f}%" if total_count > 0 else "- 有效率: 0%")
    except:
        pass

if __name__ == '__main__':
    main()
