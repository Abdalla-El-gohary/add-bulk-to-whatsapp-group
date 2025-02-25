from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# List of contacts to add (you should add them to your contacts first)
contacts_to_add = ["+201121415216","+20101412719116","+201007447340"]



def search_and_open_group(group_name):
    """Searches for the group and opens it."""
    search_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
    search_box.click()
    search_box.send_keys(group_name)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)

def open_group_settings():
    """Opens the group settings to add members."""
    time.sleep(2)
    group_title = driver.find_element(By.XPATH, "//header//span[@title]")
    group_title.click()
    time.sleep(2)

def add_members(contacts):
    """Adds members to the group."""
    added_contacts = 0
    time.sleep(2)
    try:
        # Locate the "Add participant" button using the correct XPath
        add_button = driver.find_element(By.XPATH, "//span[@data-icon='add-user']")
        driver.execute_script("arguments[0].click();", add_button)  # Click using JavaScript
    except:
        print("Could not find the Add Participant button!")
        return

    time.sleep(2)
    for contact in contacts:
        search_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
        search_box.send_keys(contact)
        time.sleep(2)
        try:
            checkbox = driver.find_element(By.XPATH, "//div[@role='checkbox']")
            already_added = driver.find_elements(By.XPATH, "//div[contains(text(), 'Already added to group')]")
            # Check if the checkbox is disabled (meaning they are already a member)
            if already_added:
                
                print(f"⚠️ {contact} is already a member. Skipping...")
            else:
                driver.execute_script("arguments[0].scrollIntoView();", checkbox)  # Scroll into view if necessary
                time.sleep(1)
                checkbox.click()  # Click the checkbox
                print(f"✅ Clicked on {contact}")
                added_contacts += 1
            
        except Exception as e:
            inserted_text = search_box.get_attribute("value")
            print(f"❌ Couldn't find {contact}: {e}")

        search_box.send_keys(Keys.CONTROL + "a")  # Select all text (for Windows/Linux)
        search_box.send_keys(Keys.BACKSPACE)  # Delete text
        # search_box.clear()
        time.sleep(1)


    # Locate the button confirm
    confirm_button = driver.find_element(By.XPATH, "//span[@aria-label='Confirm']")

    # Click using JavaScript to avoid overlay issues
    driver.execute_script("arguments[0].click();", confirm_button)
    print("Confirm button clicked successfully!")

    time.sleep(4)

    # Click the "Add member" button
    if (added_contacts > 1):
        add_member_button = driver.find_element(By.XPATH, "//div[text()='Add members']")
    elif (added_contacts == 0):
        print("No contacts added!")
        return
    else:
        add_member_button = driver.find_element(By.XPATH, "//div[text()='Add member']")
    
    driver.execute_script("arguments[0].click();", add_member_button)  # Click using JavaScript

    time.sleep(2)


if __name__ == "__main__":
    
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()  # Change to the correct driver if needed
    driver.get("https://web.whatsapp.com")

    # Wait for manual login (wait until whatapp web if fully loaded before clicking enter)
    input("Press Enter after scanning the QR code...")

    group_name = "TestGroup01"  # Change to your actual group name
    search_and_open_group(group_name)
    open_group_settings()
    add_members(contacts_to_add)

    print("Contacts added successfully!")
    driver.quit()
