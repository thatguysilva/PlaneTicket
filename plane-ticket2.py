from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

# Function to send an email
def send_email(content):
    # Set up the SMTP server
    smtp_server = 'smtp-mail.outlook.com'  # Your SMTP server - outlook is recommended
    smtp_port = 587  # Your SMTP port
    sender_email = ''  # Your email
    receiver_email = ''  # Receiver's email
    password = 'iwantcheaptickets-123'  # Your password

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Flight Price Alert'

    # Add body to email
    message.attach(MIMEText(content, 'plain'))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

# Main function
if __name__ == '__main__':
    # Set up the Chrome driver (you might need to download the corresponding driver for your Chrome version)
    driver = webdriver.Chrome()

    # Navigate to the website
    driver.get('https://www.latamairlines.com/br/pt/destinos')

    # Accept cookies
    time.sleep(5)  # Adjust this time if necessary
    try:
        cookies_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Aceite todos os cookies')]"))
        )
        cookies_button.click()
        time.sleep(3)  # Adjust this time if necessary
    except Exception as e:
        print(f"Cookies button not found. Error: {e}")

    # Click the "Mais Ofertas" button six times
    time.sleep(5)  # Adjust this time if necessary
    for _ in range(6):
        try:
            mais_ofertas_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Mostrar mais ofertas')]"))
            )
            mais_ofertas_button.click()
            time.sleep(3)  # Adjust this time if necessary
        except Exception as e:
            print(f"Button not found. Error: {e}")

    # Scrape the prices, corresponding city names, and dates
    time.sleep(5)  # Adjust this time if necessary
    prices = driver.find_elements(By.XPATH, "//p[@class='sc-eqUAAy bQfEYp latam-typography latam-typography--heading-05 sc-fqkvVR gQycbC']")
    cities = driver.find_elements(By.XPATH, "//span[@class='sc-eqUAAy hmdnMD latam-typography latam-typography--heading-05 sc-fqkvVR gQycbC']")
    dates = driver.find_elements(By.XPATH, "//span[@class='sc-eqUAAy cWmgsD latam-typography latam-typography--paragraph-medium sc-fqkvVR gQycbC']")

    # Filter and save information for prices below BRL 500
    valid_prices = []
    for i in range(len(prices)):
        price_text = prices[i].text
        price_value = float(price_text.split()[1].replace('.', '').replace(',', '.'))
        city_name = cities[i].text
        date_text = re.search(r'Viaje em <strong>(\d{2}/\d{2}/\d{2})</strong>', dates[i].get_attribute('innerHTML')).group(1)
        if price_value < 500:
            valid_prices.append(f"{city_name}: {price_text}, Date: {date_text}")

    # Send the results to an email
    content = "\n".join(valid_prices)
    send_email(content)

    # Close the browser
    driver.quit()
