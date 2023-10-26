from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send an email
def send_email(content):
    # Set up the SMTP server
    smtp_server = 'smtp.example.com'  # Your SMTP server
    smtp_port = 587  # Your SMTP port
    sender_email = 'your_email@example.com'  # Your email
    receiver_email = 'receiver_email@example.com'  # Receiver's email
    password = 'your_password'  # Your password

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
    driver=webdriver.Chrome()

    # Navigate to the website
    driver.get('https://www.latamairlines.com/br/pt/destinos')

    # Click the "Mais Ofertas" button six times
    for _ in range(6):
        try:
            mais_ofertas_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Mostrar mais ofertas')]"))
            )
            mais_ofertas_button.click()
            time.sleep(3)  # Adjust this time if necessary
        except:
            print("Button not found.")

    # Scrape the prices
    prices = driver.find_elements_by_xpath("//p[@class='sc-eqUAAy bQfEYp latam-typography latam-typography--heading-05 sc-fqkvVR gQycbC']")
    for price in prices:
        print(price.text)

    # Close the browser
    driver.quit()
