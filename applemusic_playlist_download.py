import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import subprocess

path = r'' #chromedriver位置
url = 'https://music.apple.com/library/' #歌单地址
regular_expression = u'[\u4e00-\u9fa5]+' #匹配中文
profile_dir = r'' #chrome配置文件位置
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
directory = ''

service = Service(executable_path=path) #启动时使用已有配置文件
web = webdriver.Chrome(service=service, options=chrome_options)

web.get(url)
time.sleep(1)
input()

playlist = web.find_elements('xpath', '//*[@id="scrollable-page"]/main/div/div[2]/div/div/div[starts-with(@class,"songs-list-row")]')
for i in playlist:
    music = i.find_element('xpath', './/*[starts-with(@href,"https://music.apple.com/cn/album")]')
    music_url = music.get_attribute('href')
    print(music_url)
    process = ''
    print(process)
    #运行脚本
    result = subprocess.run(process, shell=True, capture_output=True, text=True, cwd=directory)
    #处理输出
    if result.returncode == 0:
        lines = result.stdout.splitlines()
        for line in lines:
            print(line)
    else:
        print(f"命令执行失败：{result.stderr}")

time.sleep(5)
web.close()
