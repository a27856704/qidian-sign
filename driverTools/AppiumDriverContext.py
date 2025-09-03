from appium import webdriver


class AppiumDriverContext:
    def __init__(self, command_executor, options):
        self.command_executor = command_executor
        self.options = options
        self.driver = None

    def __enter__(self):
        self.driver = webdriver.Remote(command_executor=self.command_executor, options=self.options)
        self.driver.implicitly_wait(10)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            try:
                # 强行和 Appium 断开连接，释放资源
                self.driver.quit()
            except Exception as e:
                # 如果在关闭连接时出现异常，记录日志或者输出错误信息
                print(f"Error occurred while quitting the driver: {e}")
                # 捕获异常并记录日志
                print(f"An error occurred while quitting the driver: {e}")
                # 如果需要，尝试再次关闭应用程序
                try:
                    self.driver.quit()
                except Exception as e:
                    # 再次关闭失败，记录日志
                    print(f"Failed to quit the driver again: {e}")
