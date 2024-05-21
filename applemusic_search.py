import os.path
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

path = r'' #chromedriver位置
url = 'https://music.apple.com/cn/search?term='
regular_expression = u'[\u4e00-\u9fa5]+' #匹配中文
profile_dir = r'' #chrome配置文件位置
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
playlist = '' #播放列表
playlist_element = '//button[starts-with(@title,"'+playlist+'")]'

service = Service(executable_path=path) #启动时使用已有配置文件
web = webdriver.Chrome(service=service, options=chrome_options)

web.get(url)
time.sleep(8)


music_search_list = web.find_elements('xpath', '//*[@class="grid svelte-1n98s4f grid--flow-row grid--custom-columns grid--top-results"]/li/div') #查找歌曲列表
print(music_search_list)
for i in music_search_list:
    info_secondary = i.find_element('xpath', './/*[starts-with(@class,"top-search-lockup__secondary")]').text #类型和艺人
    info_primary = i.find_element('xpath', './/*[starts-with(@class,"top-search-lockup__primary__title")]').text #名称
    type = re.search(regular_expression, info_secondary)
    print(type)
    if type.group(0) == '歌曲':
        print(info_primary, info_secondary)
        button_menu = i.find_element('xpath', './/button[starts-with(@class,"contextual-menu__trigger")]')
        button_menu.click()
        time.sleep(0.1)
        button_add1 = i.find_element('xpath', '//button[starts-with(@title,"添加到歌单")]')
        button_add1.click()
        button_add2 = i.find_element('xpath', playlist_element)
        button_add2.click()
        time.sleep(0.1)
time.sleep(5)
web.close()
