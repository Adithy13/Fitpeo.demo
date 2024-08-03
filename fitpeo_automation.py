from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize Chrome options
options = Options()
options.headless = False  # Set to True if you want to run the browser in headless mode

# Automatically download and set up ChromeDriver
service = Service(ChromeDriverManager().install())

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. Navigate to FitPeo Homepage
    driver.get('https://fitpeo.com')
    driver.maximize_window()
    print('one')

    # 2. Navigate to the Revenue Calculator Page
    revenue_calculator_link = driver.find_element(By.LINK_TEXT, 'Revenue Calculator')
    revenue_calculator_link.click()
    print('two')

    # 3. Scroll Down to the Slider section
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    print('three')

    # 4. Adjust the Slider
    slider = driver.find_element(By.CSS_SELECTOR, 'input[type="range"]')
    driver.execute_script("arguments[0].value = 820", slider)
    slider.send_keys(Keys.RETURN)
    print('four')

    # 5. Update the Text Field
    text_field = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    text_field.clear()
    text_field.send_keys('560')
    text_field.send_keys(Keys.RETURN)
    print('five')

    # 6. Validate Slider Value
    updated_slider_value = driver.execute_script("return arguments[0].value", slider)
    assert updated_slider_value == '560', f"Slider value should be 560 but got {updated_slider_value}"
    print('six')

    # 7. Select CPT Codes
    cpt_codes = ['CPT-99091', 'CPT-99453', 'CPT-99454', 'CPT-99474']
    for code in cpt_codes:
        checkbox = driver.find_element(By.XPATH, f"//label[text()='{code}']/preceding-sibling::input")
        if not checkbox.is_selected():
            checkbox.click()
    print('seveen')

    # 8. Validate Total Recurring Reimbursement
    total_reimbursement = driver.find_element(By.CSS_SELECTOR, 'selector-for-total-reimbursement')  # Adjust selector
    assert total_reimbursement.text == '$110700', f"Expected total reimbursement to be $110700 but got {total_reimbursement.text}"
    print('done')
finally:
    # Clean up
    time.sleep(5)  # Let user see results before closing
    driver.quit()
