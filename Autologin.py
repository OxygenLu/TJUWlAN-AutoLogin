"""
tju-校园网自动登录 v1.0
"""
import os
import time
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- config ---
USERNAME = '' #填账号
PASSWORD = '' #填密码
LOGIN_URL = 'http://202.113.9.18/srun_portal_pc?ac_id=16&theme=tju'

def show_welcome():
    print(
'''
--------------------------------------------------------
                                                        
   ##     ##                        ###                 
   ##                                ##                 
 ######  ###  ##  ##         ##  ##  ##   ##### #####   
   ##     ##  ##  ##  #####  ##  ##  ##      ## ##  ##  
   ##     ##  ##  ##         ######  ##  ###### ##  ##  
    ###   ##   ####          ##  ## ####  ##### ##  ##  
       ####                   
                                                        
                    Welcome to TJU    

           OxygenLu 制作-TJU校园网自动登录 v1.0
--------------------------------------------------------
'''
    )

def setup_driver():
    options = Options()
    options.add_argument('--headless')  # 后台运行
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # 增加用户代理，防止被识别为爬虫
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)...")
    
    # 使用 webdriver_manager 自动管理驱动
    from selenium.webdriver.chrome.service import Service
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def check_net():
    try:
        target = "www.baidu.com"
        param = "-n" if os.name == 'nt' else "-c"
        res = subprocess.run(["ping", param, "1", target], capture_output=True, timeout=5)
        return res.returncode == 0
    except:
        return False

def login(driver):
    try:
        driver.get(LOGIN_URL)

        time.sleep(2)
        

        user_input = driver.find_element(By.NAME, "username")
        pass_input = driver.find_element(By.NAME, "password")
        
        # 输入账号密码
        user_input.clear()
        pass_input.clear()
        user_input.send_keys(USERNAME)
        pass_input.send_keys(PASSWORD)
        

        pass_input.send_keys(Keys.RETURN)
        time.sleep(3)
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] 登录过程出错: {e}")
        return False

if __name__ == '__main__':

    show_welcome()
    if check_net():
        print(f"[{datetime.now()}] 网络已链接，欢迎使用。")
    else:
        print(f"[{datetime.now()}] 检测到未联网，正在启动浏览器登录...")
        
        driver = setup_driver()
        try:
            success = login(driver)
            if success and check_net():
                print(f"\n[{datetime.now()}] >>> 登录成功！网络已恢复。")
            else:
                print(f"\n[{datetime.now()}] >>> 登录尝试结束，请检查账号密码或网络环境。")
        finally:
            driver.quit()