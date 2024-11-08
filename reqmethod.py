import requests
from bs4 import BeautifulSoup
import time

# Define URLs
login_url = 'https://vignanits.ac.in/Attendance/Validate.php' # Validate
protected_url = 'https://vignanits.ac.in/Attendance/EAttend.php' # EAttend
studentwise_report_url = "https://vignanits.ac.in/Attendance/Sreports.php" # CReports

# Login credentials
payload = {
    'uname': '840',
    'pass': 'vgnt'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': login_url
}

with requests.Session() as session:
    login_response = session.post(login_url, headers=headers, data=payload)

    if login_response.status_code == 200 and "Enter Attendance" in login_response.text:
        print("Logged in")
    else:
        print("Login failed.")
        exit(1)

    form_data = {
        'roll':'23891A0549',
        'fdt': '30-07-24',  # From Date
        'tdt': '08-11-24',  # To Date
        'Submit': 'Submit'
    }

    max_attempts = 10
    attempt = 0
    response = None

    while attempt < max_attempts:
        try:
            response = session.post(studentwise_report_url, headers=headers, data=form_data, timeout=20)
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            if tables and any(row.find('td') for table in tables for row in table.find_all('tr')):
                print("Student-Wise Report page Accessed")
                break
            else:
                print(f"Attempt {attempt + 1}: Waiting for page to load...")
                time.sleep(2)
                attempt += 1

        except requests.exceptions.Timeout:
            print("Request timed out. The server took too long to respond.")
            break
        except requests.exceptions.RequestException as e:
            print("An error occurred while accessing the page:", e)
            break

    if response and response.status_code == 200 and tables:
        print("Student-Wise Report - ")
        for i, table in enumerate(tables, 1):
            rows = table.find_all('tr')
            data_rows = [row for row in rows if row.find('td')]
            if data_rows:
                print(f"\nTable {i}:")
                for row in data_rows:
                    columns = row.find_all(['td', 'th'])
                    data = [col.get_text(strip=True) for col in columns]
                    print(data)
    else:
        print("Timeout on Student-Wise Report")
