from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import shutil
import time

def scrape_data(origin_zip, destination_zip, length, width, height, weight_pounds, weight_ounces):
    try:
        chromedriver_autoinstaller.install()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0")
        chromedriver_path = shutil.which("chromedriver")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get('https://www.pirateship.com/usps/shipping-calculator')
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "originZip"))).send_keys(origin_zip)
        wait.until(EC.presence_of_element_located((By.NAME, "destination"))).send_keys(destination_zip)
        wait.until(EC.presence_of_element_located((By.NAME, "dimensionX"))).send_keys(length)
        wait.until(EC.presence_of_element_located((By.NAME, "dimensionY"))).send_keys(width)
        wait.until(EC.presence_of_element_located((By.NAME, "dimensionZ"))).send_keys(height)
        wait.until(EC.presence_of_element_located((By.NAME, "weightPounds"))).send_keys(weight_pounds)
        wait.until(EC.presence_of_element_located((By.NAME, "weightOunces"))).send_keys(weight_ounces)

        wait.until(EC.element_to_be_clickable((By.ID, "packageTypeKey-Parcel"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "packageTypeKey-UspsSmallFlatRateBox"))).click()

        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ps-rate-form"]/div[2]/form/div[2]/div/button')))
        button.click()
        time.sleep(10)

        results_g9ctrl = driver.find_elements(By.CLASS_NAME, "css-g9ctrl")
        results_10m1t44 = driver.find_elements(By.CLASS_NAME, "css-10m1t44")

        if not results_g9ctrl or not results_10m1t44:
            return ["Error: No se encontraron los resultados esperados en la página."]

        num_results = min(len(results_g9ctrl), len(results_10m1t44))
        results = []
        for i in range(num_results):
            results.append(f"Resultado {i + 1}: css-g9ctrl: {results_g9ctrl[i].text}, css-10m1t44: {results_10m1t44[i].text}")
        return results
    except Exception as e:
        return [f"Error: {str(e)}"]
    finally:
        driver.quit()
