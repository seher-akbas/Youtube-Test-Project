import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--mute-audio")

driver = webdriver.Chrome(options=chrome_options)
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

for _ in range(5):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(0.5)

assert len(results) >= 5
print("En az 5 video yüklendi")

results[0].click()

wait.until(EC.url_contains("watch"))

videoTitle = wait.until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "h1.ytd-watch-metadata")
    )
)

videoPlayer = wait.until(
    EC.presence_of_element_located((By.TAG_NAME, "video"))

)

assert videoTitle.text , "Video başlığı yok"
print(f"video başlığı: {videoTitle.text}")

assert videoPlayer, "Video yok"
print(f"video yüklendi")


skipButton = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'ytp-skip-ad-button')]"))
    )
skipButton.click()

videoDuration = driver.execute_script("return document.getElementsByTagName('video')[0].duration")
assert videoDuration <= 4*60, "Video 4 dakikadan uzun"

minutes = int(videoDuration // 60)
seconds = int(videoDuration % 60)

print(f"{minutes} dakika {seconds} saniye")

driver.save_screenshot("kısa video.png")

driver.quit()