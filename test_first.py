from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker
import pytest


class TestFirst:


    def verify_email_address(self, email):
        """Method to verify if email on account is correct user email."""
        verify_btn = driver.find_element(By.XPATH, "//div[@class='edit-gravatar is-unverified']")
        verify_btn.click()
        listed_email = driver.find_element(By.XPATH, "//p[@class='email-verification-dialog__confirmation-dialog-email']/span").get_attribute("textContent")
        driver.implicitly_wait(5)
        submit_btn = driver.find_element(By.XPATH, "//div[@class='dialog__action-buttons']/button[contains(text(), 'OK')]")
        submit_btn.click()
        if not listed_email == email:
            return False
        else:
            return True


    def fill_out_profile(self, f_name='fname', l_name='lname', p_name='pname', about_m='aboutMe', gv_toggle=True):
        """Method performs series of steps to complete the profile and save"""
        first_name = driver.find_element(By.ID, "first_name")
        last_name = driver.find_element(By.ID, "last_name")
        public_name = driver.find_element(By.NAME, "display_name")
        about_me = driver.find_element(By.TAG_NAME, "textarea")
        g_toggle = driver.find_element(By.ID, "inspector-toggle-control-0")
        g_toggle_value = g_toggle.is_enabled()
        submit_profile = driver.find_element(By.XPATH, "(//button)[5]")
        first_name.clear()
        first_name.send_keys(f_name)
        last_name.clear()
        last_name.send_keys(l_name)
        public_name.clear()
        public_name.send_keys(p_name)
        about_me.clear()
        about_me.send_keys(about_m)
        if gv_toggle and not g_toggle_value:
            g_toggle.click()
        elif not gv_toggle and g_toggle_value:
            g_toggle.click()
        submit_profile.click()


    def test_write_function(self):
        """Method to perform tasks to test the write button functionality"""
        write_btn = driver.find_element(By.XPATH, "//a[@title='Create a New Post']")
        write_btn.click()
        obj = driver.switch_to.alert
        driver.implicitly_wait(5)
        obj.accept()
        driver.back()


    def test_learn_more_link(self):
        """Method to test the learn more link and navigate to new tab"""
        learn_more = driver.find_element(By.XPATH, "//a/span[@class='inline-support-link__nowrap']")
        learn_more.click()
        access_site = driver.find_element(By.XPATH, "//a[@rel=' noopener noreferrer']")
        access_site.click()
        driver.implicitly_wait(4)
        driver.switch_to.new_window('tab')
        original_window = driver.window_handles[0]
        driver.switch_to.window(original_window)
        close_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Close')]")
        close_btn.click()


    def add_url_link(self, url, description):
        """Method to perform tests on saving urls and limiting the urls saved to five."""
        url_names = ['.net', 'com', '.biz', '.org', '.info']
        add_button = driver.find_element(By.XPATH, "(//div[@class='section-header__actions'])[2]")
        add_button.click()
        add_url_btn = driver.find_element(By.XPATH, "//div/button[contains(text(), 'Add URL')]")
        driver.implicitly_wait(5)
        add_url_btn.click()
        url_entered = driver.find_element(By.XPATH, "//div/form/fieldset/input[@placeholder='Enter a URL']")
        description_enter = driver.find_element(By.XPATH, "//div/form/fieldset/input[@placeholder='Enter a description']")
        submit_site_btn = driver.find_element(By.XPATH, "//button[@class='button profile-links-add-other__add form-button is-primary']")
        dot_index = [x for x in range(len(url)) if url[x] == '.']
        if not url[int(dot_index[0]):] in url_names:
            url_entered.clear()
            url_entered.send_keys(f"{url}.com")
        else:
            url_entered.send_keys(url)
        description_enter.send_keys(description)
        driver.implicitly_wait(15)
        submit_site_btn.click()
        driver.implicitly_wait(15)

        listed_urls = driver.find_elements(By.XPATH, "//ul[@class='profile-links__list']/li")
        if len(listed_urls) > 5:
            for x in (range(len(listed_urls))-5):
                li_item_del = driver.find_element(By.XPATH, "//ul[@class='profile-links__list']/li/button")
                li_item_del.click()


    def toggle_profile_submit(self):
        """Method to toggle the value of the gravatar toggle switch"""
        toggle_value = driver.find_element(By.ID, "inspector-toggle-control-0")
        toggle_value1 = toggle_value.is_enabled()
        switch = False if toggle_value1 else True
        return switch


    def test_first(self):
        s = Service(ChromeDriverManager().install())
        global driver
        driver = webdriver.Chrome(service=s)

        assert_list = []
        fake = Faker()
        fake_name = fake.name()
        fake_text = fake.text()
        fake_url = fake.domain_name()
        fake_url_img = fake.image_url()
        email1 = "barbenjade@gmail.com"
        pswd = "6#^5SVW!h7VewCp"

        driver.get("https://wordpress.com/me")
        driver.implicitly_wait(3)
        username_input = driver.find_element(By.ID, "usernameOrEmail")
        pswd_input = driver.find_element(By.ID, "password")
        continue1 = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")

        username_input.send_keys(email1)
        continue1.click()
        driver.implicitly_wait(5)
        pswd_input.send_keys(pswd)
        log_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")
        log_in_btn.click()
        if not self.verify_email_address(email1):
            assert_list.append("Invalid email address.")
        self.fill_out_profile(fake_name, about_m=fake_text, gv_toggle=self.toggle_profile_submit())
        add_btn_goto = driver.find_element(By.XPATH, "(//div[@class='section-header__actions'])[2]")
        webdriver.ActionChains(driver).move_to_element(add_btn_goto).perform()
        self.test_write_function(fake_url_img)
        self.test_learn_more_link()
        self.add_url_link(fake_url, fake_text)

        assert not assert_list, assert_list
        driver.quit()
