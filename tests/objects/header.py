import os
from seleniumbase import BaseCase


class Header(BaseCase):
    header_icon = "a#nava"
    header_name_of_user = 'a#nameofuser'
    header_log_in_button = '[data-target="#logInModal"]'
    header_sign_up_button = '[data-target="#signInModal"]'
    header_card_button = 'a#cartur'

    # signup modal
    sign_up_modal = 'div#signInModal .modal-dialog'
    sign_username = 'input#sign-username'
    sign_password = 'input#sign-password'
    sign_in_button = 'div#signInModal button[onclick="register()"]'

    # login modal
    log_in_modal = 'div#logInModal .modal-dialog'
    log_in_username = 'input#loginusername'
    log_in_password = 'input#loginpassword'
    log_in_button = 'div#logInModal button[onclick="logIn()"]'

    def header_visible(self):
        return self.wait_for_element_visible(self.header_icon)

    def open_cart_page(self):
        self.click(self.header_card_button)

    def create_user(self, username, password):
        self.click(self.header_sign_up_button)
        self.wait_for_element_visible(self.sign_up_modal)
        self.input(self.sign_username, username)
        self.input(self.sign_password, password)
        self.click(self.sign_in_button)
        try:
            alert = self.switch_to_alert(2)
            self.assertTrue(alert.text.find('successful') != -1, 'Expected SignUp alert to be successful! user:' + username)
            alert.accept()
        except Exception:
            # for this case login step failure will show the result
            pass

    def login(self, username, password):
        self.click(self.header_log_in_button)
        self.wait_for_element_visible(self.log_in_modal)
        self.input(self.log_in_username, username)
        self.input(self.log_in_password, password)
        self.click(self.log_in_button)
        self.wait_for_partial_link_text_present('Welcome')
        self.assert_elements_visible(self.header_name_of_user)
        os.environ['user_created'] = 'True'
