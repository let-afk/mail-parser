from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def mail_parser(mail_usr, password):
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    s = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get("https://account.mail.ru/")

    input_usr = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
    input_usr.send_keys("study.ai_172@mail.ru")

    btn = driver.find_element(
        By.XPATH, "//button[@data-test-id='next-button']")
    btn.click()

    input_pswd = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
    driver.implicitly_wait(0.1)
    input_pswd.send_keys("NextPassword172#")

    btn = driver.find_element(
        By.XPATH, "//button[@data-test-id='submit-button']")
    btn.click()

    mail_cnt_elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'nav__item_active ')]")))
    mail_cnt = int(mail_cnt_elem.get_attribute("title").split()[1])
    mails_link_set = set()
    last_elem = None
    while len(mails_link_set) < mail_cnt:
        mails = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'llc')]")))
        mails_link = [mail.get_attribute("href") for mail in mails]
        mails_link_set = mails_link_set.union(set(mails_link))
        actions = ActionChains(driver)
        actions.move_to_element(mails[-1])
        actions.perform()

    mails_info = []
    for mail_link in mails_link_set:
        if isinstance(mail_link, str):
            mail_info = {}
            driver.get(mail_link)
            mail_source = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "letter__author")))
            mail_author = mail_source.find_element(
                By.XPATH, ".//span[@class='letter-contact']")
            mail_info["author"] = f"{mail_author.text} {mail_author.get_attribute('title')}"
            mail_date = mail_source.find_element(
                By.XPATH, ".//div[@class='letter__date']")
            mail_info["date"] = mail_date.text
            mail_thread = driver.find_element(
                By.XPATH, "//h2[@class='thread-subject']")
            mail_info["thread"] = mail_thread.text
            mail_text = driver.find_element(
                By.XPATH, "//div[@class='letter__body']")
            mail_info["text"] = mail_text.text
            mails_info.append(mail_info)
    return mails_info
