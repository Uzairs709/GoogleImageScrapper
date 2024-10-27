import base64
import gc
import os
import re
import uuid
import time
from http.client import responses

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup the Chrome WebDriver
driver = webdriver.Chrome()

def scrap_web(search_url):
    driver.get(url=search_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.F0uyec'))
    )

    # Scroll to load more images
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    page_html = driver.page_source
    page_soup = bs4.BeautifulSoup(page_html, "html.parser")

    containers = page_soup.findAll("div", {'class': "F0uyec"})  # Thumbnail container div class
    containers_length = len(containers)
    print(f"Found {containers_length} containers")
    return containers_length

def get_img_links(containers_length):
    for i in range(1, containers_length + 1):
        x_path = f'(//div[@class="F0uyec"])[{i}]//img'  # Thumbnail image XPath

        try:
            # Find the thumbnail image and click to open the side panel
            thumbnail = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, x_path))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", thumbnail)

            # Close pop-ups or overlays if any before clicking the thumbnail
            close_popups()

            thumbnail.click()

            # Wait for the high-resolution image to load in the side panel
            high_res_xpath = '//img[contains(@class, "sFlh5c FyHeAf iPVvYb") and @jsname="kn3ccd"]'  # Side panel image XPath
            high_res_img = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, high_res_xpath))
            )
            img_url = high_res_img.get_attribute('src')

            # Save the image if URL is valid
            if img_url and img_url.startswith("http"):
                save_image(img_url)

            time.sleep(1)  # Small delay before moving to the next thumbnail

        except Exception as e:
            print(f'Error processing thumbnail {i}: {e}')

def close_popups():
    try:
        close_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close']")
        close_button.click()
        time.sleep(1)  # Wait for close action to complete
    except Exception:
        pass  # No close button found, continue

def save_image(img_url):
    global img_count
    save_dir = 'Acne'
    os.makedirs(save_dir, exist_ok=True)

    try:
        if img_count >= num_images:
            return

        response = requests.get(img_url, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            filename = f'image_{uuid.uuid4().hex[:8]}.jpg'
            image_path = os.path.join(save_dir, filename)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f'Image {img_count}/{num_images} saved as: {filename}')
            img_count += 1
        else:
            print('Failed to download image, status code:', response.status_code)
    except Exception as e:
        print(f'Error saving image: {e}')
    finally:
        gc.collect()

if __name__ == "__main__":
    img_count = 0
    num_images = int(input("Enter the number of images: "))

    url="https://www.google.com/search?sca_esv=a573f3704a16bd57&sxsrf=ADLYWIJMvtU7iPWnGaqCUf767130mdrO-w:1730026968907&q=chicken+pox+skin+disease&udm=2&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3J_86uWOeqwdnV0yaSF-x2jon2iao6KWCaVjfn7ahz_sf_uPKlBgHiXUTxuTOrBgkEHAZKBArNMIg_JaUOYCTVNreNhAlJbFKEmzPuAQkoiBtIhrPYKQR3WHGzgZYwxf2NkHIa-s&sa=X&ved=2ahUKEwiL2bvXtK6JAxWhRvEDHeVeATkQtKgLegQIFRAB&biw=1536&bih=703&dpr=1.25"
    len_containers = scrap_web(url)
    get_img_links(len_containers)

    if img_count >= num_images:
        print("Success")
    else:
        print("Failed")

    driver.quit()
