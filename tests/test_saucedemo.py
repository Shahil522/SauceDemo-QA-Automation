from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_driver():
    return webdriver.Firefox()

def test_valid_login():
    driver = create_driver()
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    assert "inventory" in driver.current_url
    driver.quit()

def test_add_product_and_checkout():
    driver = create_driver()
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CSS_SELECTOR, '[data-test="shopping-cart-link"]').click()
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "first-name").send_keys("Shahil")
    driver.find_element(By.ID, "last-name").send_keys("Mansuri")
    driver.find_element(By.ID, "postal-code").send_keys("834001")
    driver.find_element(By.ID, "continue").click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "finish"))
    ).click()
    WebDriverWait(driver, 20).until(
        EC.url_contains("checkout-complete.html")
    )
    assert "Thank you for your order!" in driver.page_source
    driver.quit()

def test_locked_out_user():
    driver = create_driver()
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    error_message = driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
    assert "Sorry, this user has been locked out." in error_message.text
    driver.quit()