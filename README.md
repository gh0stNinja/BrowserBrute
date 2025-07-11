# AutoBrowserBoom

🔐 一个基于 Python + Selenium 的自动化浏览器弱口令爆破脚本，集成验证码自动识别（依赖本地 OCR API 服务 [AutoCaptcha](https://github.com/gh0stNinja/AutoCaptcha)）。

---

## 📌 功能概述

- 使用 **Selenium** 控制 Chrome 或 Firefox 自动化登录表单
- 从本地文件批量读取用户名和密码字典进行爆破
- 支持自动检测是否存在验证码输入框
- 自动截图验证码、调用本地 `AutoCaptcha` OCR API 进行识别
- 自动提交验证码并继续尝试登录
- 记录登录成功或失败

---

## 🗂️ 项目结构

```
AutoBrowserBoom/
 │
 ├── boom.py           # 主程序
 ├── auth_key.json     # 存放 OCR API 授权 key
 ├── username.txt      # 用户名字典
 ├── password.txt      # 密码字典
 └── README.md         # 使用说明
```

---

## ⚙️ 使用前准备

1. **环境依赖**  
   - Python 3.x  
   - `selenium`  
   - Chrome 或 Firefox 驱动  
   - `requests`  
   - 本地运行 `AutoCaptcha`（验证码识别服务）

   ```bash
   pip install selenium requests

> 📌 Chrome 需安装对应版本的 chromedriver 并放到 PATH。

1. **配置 OCR 授权**
    在项目根目录创建 `auth_key.json` 文件：

   ```
   {
     "key": "你的授权Key"
   }
   ```

2. **准备字典**
    在同级目录放 `username.txt` 和 `password.txt`，一行一个账号或密码。

------

## 🚀 运行脚本

1. 启动 `AutoCaptcha` 验证码服务：

   ```
   python AutoCaptcha.py -p 58888
   ```

2. 修改 `chrome_try_passwords.py` 里：

   - 登录页面 URL (`url`)
   - XPATH 定位表达式（`xpath_input_username`、`xpath_input_password`、`xpath_login_button`、验证码相关等）
   - 字典文件名

3. 执行：

   ```
   python boom.py
   ```

------

## 🧩 常见问题

- ❓ **Q:** 验证码不准识别怎么办？
   **A:** 请先调试 `AutoCaptcha` 的预处理策略，可开启保存临时图片，微调阈值。
- ❓ **Q:** 找不到元素怎么办？
   **A:** 检查页面结构是否动态渲染，必要时加入 `time.sleep()` 或用显式等待。
- ❓ **Q:** 浏览器窗口一闪而过？
   **A:** 请不要关闭脚本的 `browser`，或者注释掉自动关闭部分。

------

## ⚠️ 声明

> 本项目仅供安全研究与学习交流使用，严禁用于非法用途，使用者需自行承担一切后果！

------

## 📚 作者

- Author: gh0stNinja
- Blog: https://gh0stninja.github.io/

![photo_2025711121445](https://raw.githubusercontent.com/gh0stNinja/images/main/photo_2025711121445.gif)