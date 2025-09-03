import time

from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import InvalidSessionIdException
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # 适用于Appium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from driverTools.AppiumDriverContext import AppiumDriverContext
from exceptions.LuciferCustomError import LuciferCustomError


# 测试完成后退出
# driver.quit()


class LinkAppium:
    def __init__(self, driver=None):
        self.driver = driver

    def set_driver(self, driver):
        self.driver = driver

    def agree_to_terms(self):
        try:
            self.driver.find_element(AppiumBy.ID, 'com.qidian.QDReader:id/button_text_id').click()
            # print(self.driver.page_source)

            print("点击了'同意并继续'按钮。")
            return True
        except NoSuchElementException as e:
            raise LuciferCustomError("在尝试同意条款时找不到元素：")

    def login(self, username, password):
        try:
            switch_to_login_mode_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.qidian.QDReader:id/tvLogin"))
            )

            switch_to_login_mode_button.click()

            # 使用AppiumBy等待“同意并继续”按钮出现，并且是可点击的
            agree_and_continue_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.qidian.QDReader:id/btnRight"))
            )

            # 点击“同意并继续”按钮
            agree_and_continue_button.click()

            # 假设driver已经被正确初始化并配置

            # 显式等待用户名输入框出现
            username_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.ID, "com.qidian.QDReader:id/mNickNameEditText"))
            )
            # 输入用户名（或手机号/邮箱）
            username_input.send_keys(username)

            # 定位密码输入框并输入密码
            password_input = self.driver.find_element(AppiumBy.ID, "com.qidian.QDReader:id/mPwdEditText")
            password_input.send_keys(password)

            # 等待登录按钮可点击并点击登录按钮
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.qidian.QDReader:id/btnLogin"))
            )
            login_button.click()

            print("登录操作完成。")
            return True
        except NoSuchElementException as e:
            # print(self.driver.page_source)
            raise LuciferCustomError("在尝试登录时找不到元素：")

    def check_in(self):
        try:
            login_button = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.qidian.QDReader:id/btnCheckIn"))
            )
            login_button.click()

            print("签到操作完成。")
            return True
        except NoSuchElementException as e:
            # print(self.driver.page_source)
            raise LuciferCustomError("在尝试签到时找不到元素：")
        except TimeoutException as e:
            print(self.driver.page_source)
            raise LuciferCustomError("签到超时：")
        except InvalidSessionIdException as e:
            print(self.driver.page_source)
            raise LuciferCustomError("会话无效：")

    def handle_update_dialog(self):
        try:
            # 等待更新对话框出现
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.TextView[contains(@text, '检测到新版本')]"))
            )
            # 查找以后再说按钮并点击
            later_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.qidian.QDReader:id/cancel"))

            )
            later_button.click()
            return True

        except TimeoutException as e:
            return False

    def auto_sign(self):
        # 设置capabilities和初始化driver
        options = AppiumOptions()
        options.set_capability('platformName', 'Android')
        # options.set_capability('app', '/apk_pack/1001745.apk')
        options.set_capability('appPackage', 'com.qidian.QDReader')  # 起点小说的包名
        # options.set_capability('appActivity', 'com.qidian.QDReader.ui.activity.MainGroupActivity')  # 起点小说的主Activity
        options.set_capability('appActivity', 'com.qidian.QDReader.ui.activity.SplashActivity')  # 起点小说的主Activity
        options.set_capability('noReset', True)  # 使用此选项以避免每次启动应用时清除其数据
        options.set_capability('automationName', 'UiAutomator1')  # 使用UiAutomator1或UiAutomator2
        # options.set_capability('automationName', 'UiAutomator2')
        # 如果你的设备不是通过USB连接的，则需要指定deviceName
        # options.set_capability('deviceName', '你的设备ID')

        with AppiumDriverContext('http://192.168.1.248:4723/wd/hub', options) as driver:
        # with AppiumDriverContext('http://10.0.0.211:4723/wd/hub', options) as driver:
            # 创建测试对象

            try:
                self.driver = driver
                # 执行测试逻辑
                # self.agree_to_terms()
                # self.login("13586514868", "90Xx1201")
                self.handle_update_dialog()
                self.check_in()

                # 睡两秒
                time.sleep(5)
                self.driver.terminate_app("com.qidian.QDReader")
            except LuciferCustomError as e:
                if driver:
                    self.driver.quit()
                return e.message
            return "签到成功"


if __name__ == '__main__':
    linkAppium = LinkAppium()
    print(linkAppium.auto_sign())
