from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# 设置 ChromeDriver 的路径，这里是我本地的路径，需要改成你自己的
webdriver_service = Service('E:/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=webdriver_service)

# 登录论坛
def login():
    driver.get('https://bbs.byr.cn/#!collection?p=1')
    username = driver.find_element(By.XPATH, '//*[@id="u_login_id"]')
    username.send_keys('这里是你的用户名')
    password = driver.find_element(By.XPATH, '//*[@id="u_login_passwd"]')
    password.send_keys('这里是你的密码')
    login_button = driver.find_element(By.XPATH, '//*[@id="u_login_submit"]')
    login_button.click()

# 删除一页的过期帖子
def delete_expired_posts_on_page():
    while True:
        time.sleep(2)  # 等待页面加载
        expired_posts = driver.find_elements(By.XPATH, "//td[contains(text(), '[指定的文章不存在或链接错误]')]")

        if not expired_posts:
            print("没有更多可删除的过期帖子。")
            break

        print("发现 %d 篇过期帖子，开始删除..." % len(expired_posts))

        for post in expired_posts:
            delete_button = post.find_element(By.XPATH, "./following-sibling::td/a[contains(@class, 'collection-del')]")
            delete_button.click()
            time.sleep(0.5)  # 等待确认删除弹窗出现

            confirm_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[1]/span")
            confirm_button.click()
            time.sleep(1)  # 等待删除操作完成
            break

        driver.refresh()


login()

for page in range(1, 18):  # 遍历第1页到第17页，请自行修改到你的收藏页的最大页数
    print("正在处理第 %d 页..." % page)
    driver.get(f'https://bbs.byr.cn/#!collection?p={page}')
    delete_expired_posts_on_page()

# 关闭浏览器
driver.quit()
