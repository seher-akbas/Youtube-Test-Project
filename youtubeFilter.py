import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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

results = wait.until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='contents']//ytd-video-renderer"))
)


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

for _ in range(25):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(0.5)

duration_elements = driver.find_elements(
    By.CSS_SELECTOR,
    "ytd-thumbnail-overlay-time-status-renderer .yt-badge-shape__text"
)

moveMause = ActionChains(driver)
short_videos = []

for duration_element in duration_elements:
    text = duration_element.text.strip()
    moveMause.move_to_element(duration_element)

    if text == "SHORTS":
        continue

    try:
        minutes, seconds = text.split(":")
        intMinutes = int(minutes)

        assert intMinutes <= 4 , f"filtre doğru çalışmıyor: {text}"

        short_videos.append(text)

    except:
        print(f"Süre formatı beklenmeyen: {text}")


assert len(short_videos) >= 5, (
    f"Yetersiz video sayısı: {len(short_videos)}"
)

print("Filtre doğru çalışıyor")

driver.quit()

