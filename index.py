import selenium.webdriver as webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep


BTCHISTORY = "https://coinmarketcap.com/currencies/bitcoin/historical-data/"

chrome_path = "C:\Development\chromedriver_win32\chromedriver.exe"
service = Service(chrome_path)
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options. add_argument("--incognito")


driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(15)
driver.get(BTCHISTORY)

driver.find_element(By.CLASS_NAME, "cmc-cookie-policy-banner__close").click()
sleep(1)

dates = []
open_prices = []
highs = []
lows = []
close_prices = []
volumes = []
m_caps = []


for n in range(6000):
    try:
        date_ = driver.find_element(By.CSS_SELECTOR, f".kkTWGn .hLKazY tbody tr:nth-child({n + 1}) td:first-child")
        dates.append(date_.text)
    except NoSuchElementException:
        break
    # if date_.text == "Mar 22, 2021":
    #     break
    # dates.append(date_.text)
    open_ = driver.find_element(By.CSS_SELECTOR, f".kkTWGn .hLKazY tbody tr:nth-child({n + 1}) td:nth-child(2)")
    open_prices.append(open_.text)
    high = driver.find_element(By.CSS_SELECTOR, f".kkTWGn .hLKazY tbody tr:nth-child({n + 1}) td:nth-child(3)")
    highs.append(high.text)
    low = driver.find_element(By.CSS_SELECTOR, f".kkTWGn .hLKazY tbody tr:nth-child({n + 1}) td:nth-child(4)")
    lows.append(low.text)
    close_ = driver.find_element(By.CSS_SELECTOR, f".kkTWGn .hLKazY tbody tr:nth-child({n + 1}) td:nth-child(5)")
    close_prices.append(close_.text)
    volume = driver.find_element(By.CSS_SELECTOR, f".kkTWGn .hLKazY tbody tr:nth-child({n + 1}) td:nth-child(6)")
    volumes.append(volume.text)
    m_cap = driver.find_element(By.CSS_SELECTOR, f".kkTWGn .hLKazY tbody tr:nth-child({n + 1}) td:last-child")
    m_caps.append(m_cap.text)

    if (n + 1) % 30 == 0:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        try:
            driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[3]/div/div/div[1]/p[1]/button').click()
        except NoSuchElementException:
            break
    print(f"Row {n} completed")

for q in range(len(dates)):
    if q == 0:
        with open("BTCPRICEHISTORY2.txt", mode="a") as file:
            file.write(f"DATE|OPEN|HIGH|LOW|CLOSE|VOLUME|MARKET CAP\n")
    try:
        with open("BTCPRICEHISTORY2.txt", mode="a") as file:
            file.write(f"{dates[q]}|{open_prices[q]}|{highs[q]}|{lows[q]}|{close_prices[q]}|{volumes[q]}|{m_caps[q]}\n")
    except UnicodeEncodeError:
        pass
    except IndexError:
        pass

print(dates)
print(len(dates))
print(open_prices)
print(len(open_prices))
print(highs)
print(len(highs))
print(lows)
print(len(lows))
print(close_prices)
print(len(close_prices))

driver.quit()
