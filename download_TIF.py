from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time
import os

USER_GOOGLE_ACCOUNT_ADDRESS = "--user-data-dir=YOUR_CHROME_USER_DATA_PATH"
SHEET_URL = "https://docs.google.com/spreadsheets/YOUR_SPREADSHEET_ID"
LINK_TXT = "YOUR_PATH\\url.txt"
TEST_TXT = "YOUR_PATH\\testurl.txt"
ERROR_TXT = "YOUR_PATH\\error.txt"
PROCESSED_LINK_TXT = "YOUR_PATH\\processedLink.txt"
LAST_PROCESSED_LINE_TXT = "YOUR_PATH\\lastProcessedLine.txt"
LAST_PROCESSED_LINE = 0

def downloadTIFF(url):
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(USER_GOOGLE_ACCOUNT_ADDRESS)
    chrome_options.add_argument("--ignore-certificate-errors")

    # 创建一个新的 Chrome 浏览器窗口
    driver = webdriver.Chrome( options=chrome_options)

    try:
    # 打开特定的URL
        driver.get(url)
    except Exception as e:
        log_error(f"{url}\n发生错误:无法打开网页\n{str(e)}")
    # 暂停一下，确保页面已经加载
    time.sleep(3)

    #修改浏览器大小至全屏
    driver.maximize_window()

    try:
        #点击进入Explore
        explore_button = driver.find_element(By.XPATH, '//*[@data-e2e-id="navbarMapBtn"]')
        explore_button.click()
    except Exception as e:
        log_error(f"{url}\n发生错误:无法点击Explore按钮\n{str(e)}")
    
    time.sleep(3)

    #检查每个checkbox是否被勾选，如被勾选则取消勾选
    #Overlays
    overlays_button = driver.find_element(By.XPATH, '//*[@data-e2e-id="overlays-card-checkbox"]')
    selected_elements = overlays_button.find_elements(By.XPATH, './/div[@class="standard-checkbox selected"]')
    if len(selected_elements) > 0:
        overlays_button.click()
    time.sleep(1)

    #Plant Health
    plant_health_button = driver.find_element(By.XPATH, '//*[@data-e2e-id="plantHealthMapTypeBtn"]')
    selected_elements = plant_health_button.find_elements(By.XPATH, './/div[@class="standard-checkbox selected"]')
    if len(selected_elements) > 0:
        plant_health_button.click()
    time.sleep(1)

    #Elevation
    elevation_button = driver.find_element(By.XPATH, '//*[@data-e2e-id="elevationMapTypeBtn"]')
    selected_elements = elevation_button.find_elements(By.XPATH, './/div[@class="standard-checkbox selected"]')
    if len(selected_elements) > 0:
        elevation_button.click()
    time.sleep(1)

    #Annotation
    annotation_elements = driver.find_elements(By.CSS_SELECTOR, '[data-e2e-id="annotation-list-card-button"]')
    for element in annotation_elements:
        selected_elements = element.find_elements(By.XPATH, './/div[@class="standard-checkbox selected"]')
        if len(selected_elements) > 0:
            element.click()
    time.sleep(1)

    #Issue
    issue_button = driver.find_element(By.XPATH, '//*[@data-e2e-id="issueListCardCheckbox"]')
    selected_elements = issue_button.find_elements(By.XPATH, './/div[@class="standard-checkbox selected"]')
    if len(selected_elements) > 0:
        issue_button.click()  
    time.sleep(1)

    #点击导出按钮
    export_button = driver.find_element(By.XPATH, "//button[i[contains(@class, 'icon-file-upload')]]")
    export_button.click()
    time.sleep(3)

    #选择TIFF文件作为输出
    TIFF_button = driver.find_element(By.XPATH, "//export-layer-option[contains(., 'GeoTIFF Map')]")
    TIFF_button.click()
    time.sleep(3)

    try:
        #删除原有邮箱地址
        delete_ma_email = driver.find_element(By.CLASS_NAME, "dd-chip-remove")
        delete_ma_email.click()
    except Exception as e:
        log_error(f"{url}\n发生错误:无法删除原有邮箱地址\n{str(e)}")
    
    time.sleep(1)

    try:
        #输入新邮箱地址
        email_input = driver.find_element(By.XPATH, '//*[@data-e2e-id="emailInput"]')
        email_input.send_keys("your_email@example.com")
        email_input.send_keys(Keys.ENTER)
    except Exception as e:
        log_error(f"{url}\n发生错误:无法添加新邮箱地址\n{str(e)}")
    time.sleep(1)
    
    try:
        #检查分辨率是否为Max Available
        current_value = driver.find_element(By.ID, "resolution").text
        if "Max" in current_value:
            print("It's the default resolution!")
        else:
            resolution_select = driver.find_element(By.ID, "resolution")
            resolution_select.click()

            max_resolution = driver.find_element(By.XPATH, '//resolution-text[contains(text(), "Max")]')
            max_resolution.click()
    except Exception as e:
        log_error(f"{url}\n发生错误:无法选择最大分辨率\n{str(e)}")
    time.sleep(1)

    try:
        #输出图像
        final_export = driver.find_element(By.ID, "exportButton")
        final_export.click()
    except Exception as e:
        log_error(f"{url}\n发生错误:无法输出图像\n{str(e)}")
    time.sleep(2)

    # 关闭浏览器
    driver.quit()

#输出error至error.txt
def log_error(error_message):
    with open(ERROR_TXT, 'a', encoding='utf-8') as f: 
        f.write(f"{error_message}\n")

def update_last_processed_line():
    with open(LAST_PROCESSED_LINE_TXT, 'r') as f:
        return int(f.readline().strip())

#Export任意两行内的所有图片
def process_links_from_file(file_path, start_line=2, end_line=None):
    global LAST_PROCESSED_LINE
    LAST_PROCESSED_LINE = update_last_processed_line()
    start_line -= 2
    end_line -= 1
    if LAST_PROCESSED_LINE < start_line:
        raise ValueError("Error: LAST_PROCESSED_LINE is " + str(LAST_PROCESSED_LINE) + " less than start_line!")
    
    if LAST_PROCESSED_LINE > end_line:
        raise ValueError("Error: LAST_PROCESSED_LINE is " + str(LAST_PROCESSED_LINE) + " greater than end_line!")
    
    if LAST_PROCESSED_LINE > start_line:
        start_line = LAST_PROCESSED_LINE
    

    with open(file_path, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number < start_line:
                continue

            if current_line_number > end_line:
                break

            downloadTIFF(line)
            LAST_PROCESSED_LINE = current_line_number + 1
            with open(PROCESSED_LINK_TXT, 'a') as f:
                f.write(f"Line {LAST_PROCESSED_LINE} Finished!\n")
            with open(LAST_PROCESSED_LINE_TXT, 'w+') as f:
                f.write(str(LAST_PROCESSED_LINE))
            
# downloadTIFF("https://www.dronedeploy.com/app2/sites/64d572fff15fa62477a08495/maps/64d57300f15fa62477")
process_links_from_file(LINK_TXT, 155, 160)
