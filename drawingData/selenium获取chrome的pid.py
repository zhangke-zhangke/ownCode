from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
driver = webdriver.Chrome(chrome_options=options)
my_dict = driver.capabilities
print(my_dict)
print(driver.service.process.pid)




# from selenium import webdriver
# from contextlib import suppress
# import psutil
#
# driver = webdriver.Chrome()
# driver.get('https://www.google.com/')
# for process in psutil.process_iter():
#     if process.name() == 'chrome.exe' and '--test-type=webdriver' in process.cmdline():
#         with suppress(psutil.NoSuchProcess):
#             print(process.pid)



