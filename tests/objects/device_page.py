from seleniumbase import BaseCase


class DevicePage(BaseCase):

    device_title = 'div.product-content .name'
    add_to_cart_button = '[onclick^="addToCart"]'

    def get_device_title(self):
        return self.wait_for_element_visible(self.device_title).text

    def add_to_card(self):
        self.click(self.add_to_cart_button)
        alert = self.switch_to_alert()
        self.assertTrue(alert.text.__contains__('Product added'), 'Expected alert message to be: Product added.')
        alert.accept()
