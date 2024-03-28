import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


# 建立存储列表
name_list = []
up_list = []
course_desc_list = []
pubdate_list = []
url_list = []
card_url_list = []
course_like_list = []
course_view_list = []
tag_list = []


# 设置搜索条件
set_time = input("请输入爬取的视频个数：")
selenium_time = int(set_time) + 1
keys = input("请输入要搜索的内容：")
print("正在爬取前" + set_time + "条关于" + keys + "的内容" + "\n")


#设置最大翻页数
Pages = 10
Pages1 = Pages
Pages2 = Pages


# 初始化WebDriver for Edge
wd = webdriver.Edge()


# 设置隐式等待时间为3秒
wd.implicitly_wait(2)


# 导航到Bilibili
wd.get('https://www.bilibili.com/')
element = wd.find_element(By.CLASS_NAME, 'nav-search-input')  # 寻找搜索输入框并输入'前端'，然后按Enter键
element.send_keys(keys + "\n")  # '\n'表示按下Enter键进行搜索


# 窗口跳转至新窗口
windows = wd.window_handles
wd.switch_to.window(windows[-1])


# 点击“最多播放”按钮
button = wd.find_element(By.CSS_SELECTOR,
                         "#i_cecream > div > div:nth-child(2) > div.search-header > div:nth-child(4) > div > div.conditions-order.flex_between > div > button:nth-child(2)")
button.click()
time.sleep(3)


# 提取封面图片链接
while Pages1 != 0:
    time.sleep(2)
    pp = 0
    cover_elements = wd.find_elements(By.CSS_SELECTOR, 'div.bili-video-card__image--wrap > picture> img')
    #当获取目标视频个数时break内循环
    for cover_element in cover_elements:
        selenium_time = int(selenium_time) - 1
        if selenium_time == 0 or pp == 30:
            break
        cover_url = cover_element.get_attribute('src')
        # print(cover_url)
        card_url_list.append(cover_url)
        pp = pp + 1
    #break外循环
    if selenium_time == 0:
        break
    #当前页面循环结束时点击下一页
    NextPageButtons = wd.find_elements(By.CSS_SELECTOR,
                                       '.vui_pagenation--btn-side')
    NextPageButton = NextPageButtons[1]
    NextPageButton.click()
    Pages1 = Pages1 - 1


#返回第一页
Page1 = wd.find_element(By.CSS_SELECTOR,
                        "#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div.flex_center.mt_x50.mb_lg > div > div > button:nth-child(2)")
Page1.click()
time.sleep(5)
selenium_time = int(set_time) + 1


# 循环点击视频并爬取简介
while Pages2 != 0:
    time.sleep(1)
    pp = 0
    video_elements = wd.find_elements(By.CSS_SELECTOR, 'div.bili-video-card__wrap.__scale-wrap > a')

    # 限制爬取个数
    for video_element in video_elements:
        selenium_time = int(selenium_time) - 1
        if selenium_time == 0 or pp == 30:
            break


        # 爬取url
        try:
            video_url = video_element.get_attribute('href')
            url_list.append(video_url)
        except NoSuchElementException:
            url_list.append("无url")


        # 在浏览器中使用JavaScript打开一个新窗口，并将video_url作为新窗口的URL
        wd.execute_script("window.open(arguments[0]);", video_url)
        # time.sleep(1)  # 等待页面加载
        wd.switch_to.window(wd.window_handles[-1])  # 切换到新打开的窗口


        # 爬取播放量
        try:
            view_element = wd.find_element(By.CSS_SELECTOR,
                                           '#viewbox_report > div.video-info-meta > div > div > div.view.item')
            view_count = view_element.text
            # print("播放量为：" + view_count)
            course_view_list.append(view_count)
        except NoSuchElementException:
            course_view_list.append("无播放量")


        # 爬取点赞数信息
        try:
            like_element = wd.find_element(By.CLASS_NAME, 'video-like-info')
            like = like_element.text
            # print(like)
            course_like_list.append(like)
        except NoSuchElementException:
            course_like_list.append("无点赞信息")


        # 爬取标题
        try:
            title_element = wd.find_element(By.CLASS_NAME,
                                            'video-title')
            title = title_element.text
            # print(title)
            name_list.append(title)

        except NoSuchElementException:
            name_list.append("无标题")

        # 爬取作者ID
        try:
            author_element = wd.find_element(By.CSS_SELECTOR, '.up-name')
            author_id = author_element.text
            # print(author_id)
            up_list.append(author_id)
        except NoSuchElementException:
            up_list.append("无作者")


        # 爬取上传时间
        try:
            time_element = wd.find_element(By.CLASS_NAME,
                                           'pubdate')
            upload_time = time_element.text
            # print(upload_time)
            pubdate_list.append(upload_time)
        except NoSuchElementException:
            pubdate_list.append("无上传时间")



        # 爬取标签
        try:
            tag_elements = wd.find_elements(By.CSS_SELECTOR, '#v_tag > div > div> div > a')
            tag = ''
            for tag_element in tag_elements:
                tag = tag + ' ' + tag_element.text
        except NoSuchElementException:
            tag = "无标签"
        tag_list.append(tag)


        # 爬取视频简介
        try:

            description_element = wd.find_element(By.CLASS_NAME, 'desc-info-text')
            description = description_element.text
            # print(description)
            course_desc_list.append(description)
        except NoSuchElementException:
            # print("无法找到视频简介")
            course_desc_list.append("无简介")
        pp = pp + 1
        wd.close()  # 关闭当前窗口
        wd.switch_to.window(wd.window_handles[-1])  # 切换回原始窗口

    #当前页面全部视频检索完成时，停滞2秒
    time.sleep(2)
    if selenium_time == 0:
        break
    #点击下一页
    NextPageButtons2 = wd.find_elements(By.CSS_SELECTOR,
                                        '.vui_pagenation--btn-side')
    NextPageButton2 = NextPageButtons2[1]#上一页和下一页的类名一样，选择第二个
    NextPageButton2.click()
    Pages2 = Pages2 - 1


#写入csv文件
import csv
from itertools import zip_longest

# 假设不是所有列表的长度都相同

# 创建一个文件对象，指定文件名和写入模式
with open('video_info.csv', 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # 写入表头
    writer.writerow(
        ['Name', 'Up', 'Course Description', 'Publish Date', 'URL', 'Card URL', 'Course Likes', 'Course Views', 'Tags'])

    # 使用 zip_longest 组合列表并填充缺失值
    for data in zip_longest(name_list, up_list, course_desc_list, pubdate_list, url_list,
                            card_url_list, course_like_list, course_view_list, tag_list, fillvalue=''):
        writer.writerow(data)

print("CSV 文件已生成。")
input("按任意键退出")


# 关闭浏览器
wd.quit()
