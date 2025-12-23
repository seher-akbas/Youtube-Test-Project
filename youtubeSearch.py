import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.get("https://www.youtube.com/")
driver.maximize_window()
wait = WebDriverWait(driver, 20)

searchBox = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ara']"))
)

searchBox.send_keys("software testing")

searchButton = wait.until(
    EC.presence_of_element_located((By.XPATH, "//button[@title='Ara']"))
)
searchButton.click()


for _ in range(6):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(0.5)

results = driver.find_elements(
    By.XPATH, "//*[@id='contents']//ytd-video-renderer"
)

assert len(results) >= 10
print("En az 10 video yüklendi")


for _ in range(5):
    driver.execute_script("window.scrollBy(0, -1000);")
    time.sleep(0.5)

filterButton = driver.find_element(By.XPATH, "//button[@aria-label='Arama filtreleri']")
filterButton.click()

videoFButton = driver.find_element(By.XPATH, "//*[@id='label']/yt-formatted-string[text() ='Video']")
videoFButton.click()

filterButton.click()

durationFilter =driver.find_element(By.XPATH, "//*[@id='label']/yt-formatted-string[text() ='4 dakikadan kısa']")
durationFilter.click()

for _ in range(10):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(0.5)

assert len(results) >= 5
print("En az 5 video yüklendi")
driver.quit()