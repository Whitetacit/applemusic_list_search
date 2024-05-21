import os.path
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import difflib

list_path = '' #歌单位置

path = r'' #chromedriver位置
regular_expression = u'[\u4e00-\u9fa5]+' #匹配中文
profile_dir = r'' #chrome配置文件位置
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
playlist = '' #播放列表
playlist_element = '//button[starts-with(@title,"'+playlist+'")]'

service = Service(executable_path=path) #启动时使用已有配置文件
web = webdriver.Chrome(service=service, options=chrome_options)

def add_playlist(xml_path):
    button_menu = xml_path.find_element('xpath', './/button[starts-with(@class,"contextual-menu__trigger")]')
    button_menu.click()
    time.sleep(0.5)
    button_add1 = xml_path.find_element('xpath', '//button[starts-with(@title,"添加到歌单")]')
    button_add1.click()
    button_add2 = xml_path.find_element('xpath', playlist_element)
    button_add2.click()

def search_music(name,artists):
    url = 'https://music.apple.com/cn/search?term='+name
    web.get(url)
    time.sleep(6)
    music_search_list = web.find_elements('xpath', '//*[@class="grid svelte-1n98s4f grid--flow-row grid--custom-columns grid--top-results"]/li/div') #查找歌曲列表
    print(music_search_list)
    music_count = 0
    music_dictionary = {}
    is_found = False
    for i in music_search_list:
        music_count += 1
        info_secondary = i.find_element('xpath', './/*[starts-with(@class,"top-search-lockup__secondary")]').text #类型和艺人
        info_primary = i.find_element('xpath', './/*[starts-with(@class,"top-search-lockup__primary__title")]').text #名称
        #print(info_secondary)
        type = re.search(regular_expression, info_secondary)
        music_dictionary[music_count] = i
        print(type)
        if type.group(0) == '歌曲':
            info_artists = info_secondary.split('·', 1)[1]
            info_artist = re.split('[' + re.escape(',;&') + ']', info_artists)[0]
            print(info_artist)
            print('当前:', info_primary, info_secondary)
            if difflib.get_close_matches(info_artist, artists, n=1, cutoff=0.8) is not None: #匹配内容
                print('匹配成功:', info_primary, info_secondary)
                add_playlist(i)
                is_found = True
                break
    if not is_found:
        print('匹配失败')
        search_music_count = int(input('手动输入数字（从1开始，0代表无匹配）'))+1
        while True:
            if search_music_count == 0:
                break
            try:
                find_music_xpath = music_dictionary[search_music_count]
                break
            except:
                print('非法输入')
        if search_music_count != 0:
            add_playlist(find_music_xpath)

    time.sleep(1)

def open_txt(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            info = line.split('-', 1)
            music_name = info[0]
            music_artists = info[1]
            music_artist = re.split('['+re.escape(',/;&')+']', music_artists)
            print(music_artist)
            search_music(music_name, music_artist)

open_txt(list_path)
web.close()
