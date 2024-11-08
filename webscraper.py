from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

df = pd.read_csv(
    'data/RDC_Inventory_Core_Metrics_Zip_History.csv',
    dtype={'postal_code': 'str'},
    usecols=['postal_code']
)
zip_codes = list(filter(lambda x: x is not None, df.postal_code.unique()))

driver = webdriver.Chrome()

for zip_code in zip_codes:
    driver.get("https://crimegrade.org/crime-by-zip-code/")
    zip_field = driver.find_element(By.ID, "zip-code")
    zip_field.send_keys(zip_code)
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    try:
        table_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "gradeComponents"))
        )
        table_html = table_element.get_attribute("outerHTML")
        file_name = f"data/raw_crime_data/{zip_code}.html"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(table_html)
        print(f"Saved table for ZIP code {zip_code} to {file_name}")
    except Exception as e:
        print(f"Error: Table did not load in time or was not found for ZIP code {zip_code}.", e)
    sleep(120)

driver.quit()
