import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# --- CONFIGURATION ---
URL = "https://easycollegemate.com/ecmngdc/result"
START_ID = 20231217
END_ID = 20231670                               # s - 656 , c - 332, a - 310
EXAM_NAME = "Test Examination"  # Make sure this matches the website exactly
LEVEL_NAME = "HSC 2nd Year"         # Make sure this matches the website exactly

# Automatically find your Documents folder
documents_path = os.path.join(os.path.expanduser("~"), "Documents", "NGDC_Results")
if not os.path.exists(documents_path):
    os.makedirs(documents_path)

# --- BROWSER SETUP ---
chrome_options = Options()
prefs = {
    "download.default_directory": documents_path, # Saves directly to Documents/NGDC_Results
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,   # Forces download instead of preview
    "profile.default_content_settings.popups": 0
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# --- THE DOWNLOAD LOOP ---
for std_id in range(START_ID, END_ID + 1):
    print(f"Downloading ID: {std_id}...")
    driver.get(URL)
    time.sleep(.25) # Small pause for stability

    try:
        # 1. Enter ID
        driver.find_element(By.NAME, "student_id").send_keys(str(std_id))

        # 2. Select Level
        level_dropdown = Select(driver.find_element(By.NAME, "level"))
        level_dropdown.select_by_visible_text(LEVEL_NAME)

        # 3. Select Exam
        exam_dropdown = Select(driver.find_element(By.NAME, "exam_id"))
        exam_dropdown.select_by_visible_text(EXAM_NAME)
        #time.sleep(.5)
       
        # 4. Click View Result (This triggers the download)
        #driver.find_element(By.ID, "btnView").click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]").click()
        time.sleep(.5)

        error_messages = driver.find_elements(By.CLASS_NAME, "alert-danger")
        if len(error_messages) > 0:
            print(f" ID {std_id} skipped: No student found on the website.")
    # Skip to the next ID in the loop
            continue
        else:
    # 3. If no error, proceed to download
            try:
               download_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download Transcript')]"))
        )
               download_btn.click()
               print(f"✅ ID {std_id} download started.")
            except :
                print(f" Error: Search worked, but download button didn't appear for {std_id}.")

        #5. Click Download PDF (This triggers the download)
        """"download_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download Transcript')]")))
        download_btn.click()"""

        # 6. Wait for the file to land in the folder
        time.sleep(.67)
       
        # Find the most recently downloaded file and rename it to the ID
        """files = [f for f in os.listdir(documents_path) if f.endswith(".pdf")]
        if files:
            # Sort by time to find the newest one
            full_paths = [os.path.join(documents_path, f) for f in files]
            latest_file = max(full_paths, key=os.path.getctime)
           
            # Only rename if it's not already named correctly
            if not os.path.basename(latest_file).startswith(str(std_id)):
                os.rename(latest_file, os.path.join(documents_path, f"{std_id}.pdf"))
                print(f"Saved: {std_id}.pdf")"""
       
    except Exception as e:
        print(f"Could not download {std_id}. Check if the ID exists or if the dropdown names are correct.")

print(f"\nAll done! Your files are in: {documents_path}")
driver.quit()

