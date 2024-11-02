from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver_path = ''  # ChromeDriver path
login_url = '' # Validate

options = webdriver.ChromeOptions()
options.add_argument('--headless') # for background process

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(login_url)

    username_input = driver.find_element(By.NAME, 'uname')
    password_input = driver.find_element(By.NAME, 'pass')
    username_input.send_keys('')  # uname
    password_input.send_keys('vgnt') # pass
    password_input.submit()

    # wait after login
    view_reports_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='Creports.php']"))
    )
    view_reports_link.click()

    # Class-Wise Report page

    branch_select = driver.find_element(By.NAME, 'br')
    branch_select.send_keys('CSE')  # Select Branch
    
    year_select = driver.find_element(By.NAME, 'yr')
    year_select.send_keys('2')      # Select Year

    section_select = driver.find_element(By.NAME, 'sc')
    section_select.send_keys('A')    # Select Section

    from_date = driver.find_element(By.NAME, 'fdt')
    from_date.send_keys('01-08-2024') # From Date

    to_date = driver.find_element(By.NAME, 'tdt')
    to_date.send_keys('30-10-2024')   # To Date

    to_date.submit()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table//tr[td]"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tables = soup.find_all('table')

    if tables:
        print("Found tables on the page with data.")
        for i, table in enumerate(tables, 1):
            print(f"\nTable {i}:")
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all(['td', 'th'])
                data = [col.get_text(strip=True) for col in columns]
                print(data)
    else:
        print("No tables found with data.")

finally:
    driver.quit()
