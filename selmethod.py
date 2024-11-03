from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver_path = '/usr/bin/chromedriver'  # ChromeDriver path
login_url = 'https://vignanits.ac.in/Attendance/Validate.php' # Validate

options = webdriver.ChromeOptions()
options.add_argument("--headless") # for background process
options.add_argument("--window-size=1920,1080")

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(login_url)

    username_input = driver.find_element(By.NAME, 'uname')
    password_input = driver.find_element(By.NAME, 'pass')
    username_input.send_keys('840')  # uname
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
    from_date.send_keys('30-07-2024') # From Date

    to_date = driver.find_element(By.NAME, 'tdt')
    to_date.send_keys('03-11-2024')   # To Date

    to_date.submit()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table//tr[td]"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tables = soup.find_all('table')

    if tables:
        attendance_percentage = []
        for row in tables[0].find_all('tr')[1:]:
            columns = row.find_all('td')
            if columns:
                last_field = columns[-1].get_text(strip=True)
                attendance_percentage.append(last_field)
        for value in attendance_percentage:
            print(value)
    else:
        print("No tables found with data.")

finally:
    driver.quit()
