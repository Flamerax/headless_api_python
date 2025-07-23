from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import os

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    steps = data.get('steps', [])

    # Configuração do Chromium
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service("/usr/lib/chromium/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    results = []

    try:
        for step in steps:
            action = step.get('action')

            if action == 'goto':
                url = step['url']
                driver.get(url)
                results.append({'goto': url})

            elif action == 'click':
                el = wait.until(EC.element_to_be_clickable((getattr(By, step['by'].upper()), step['value'])))
                el.click()
                results.append({'click': f"{step['by']}={step['value']}"})

            elif action == 'type':
                el = wait.until(EC.presence_of_element_located((getattr(By, step['by'].upper()), step['value'])))
                el.clear()
                el.send_keys(step['text'])
                results.append({'type': f"{step['text']} into {step['by']}={step['value']}"})

            elif action == 'wait':
                el = wait.until(EC.presence_of_element_located((getattr(By, step['by'].upper()), step['value'])))
                results.append({'wait': f"{step['by']}={step['value']}"})

            elif action == 'extract_text':
                el = wait.until(EC.presence_of_element_located((getattr(By, step['by'].upper()), step['value'])))
                results.append({'text': el.text})

            elif action == 'refresh':
                driver.refresh()
                results.append({'refresh': 'ok'})

            elif action == 'screenshot':
                filename = step.get('filename', 'screenshot.png')
                driver.save_screenshot(filename)

                with open(filename, 'rb') as img:
                    encoded = base64.b64encode(img.read()).decode('utf-8')

                os.remove(filename)
                results.append({'screenshot': encoded})

    except Exception as e:
        return jsonify({'error': str(e), 'results': results}), 500
    finally:
        driver.quit()

    return jsonify({'results': results})
