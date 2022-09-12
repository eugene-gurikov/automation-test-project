from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from .api_call import ApiCall


class CartPage(BaseCase, ApiCall):

    cart_table = '#page-wrapper h2 + .table-responsive'
    cart_table_rows = '#tbodyid .success'
    cart_device_title = 'td:nth-of-type(2)'
    cart_device_price = 'td:nth-of-type(3)'
    total_price = 'h3#totalp'
    calculated_total_price = 0
    # place order
    place_order_button = '[data-target="#orderModal"]'
    place_order_modal = 'div#orderModal'
    place_order_name = 'input#name'
    place_order_credit_card = 'input#card'
    place_order_purchase_button = '[onclick="purchaseOrder()"]'
    sweet_alert_message = 'div.sweet-alert h2 + p'
    sweet_alert_ok = 'div.sweet-alert button.confirm'


    def cart_page_visible(self):
        self.assert_element_visible(self.cart_table)

    def validate_devices_list(self, devices):
        # wait for element to load
        self.wait(2)
        devices_list = self.find_elements(self.cart_table_rows)
        self.assertEqual(self.calculated_total_price, 0, 'Expected validation to be performed only once!')

        for device in devices_list:
            title = device.find_element(By.CSS_SELECTOR, self.cart_device_title).text
            self.assertTrue(title in devices.values())
            price = int(device.find_element(By.CSS_SELECTOR, self.cart_device_price).text)
            self.calculated_total_price = self.calculated_total_price + price

    def validate_total_price(self):
        self.presented_total_price = int(self.get_text(self.total_price))
        self.assertEqual(self.presented_total_price, self.calculated_total_price, 'Total price doesnt match: '
                         + str(self.presented_total_price) + '|' + str(self.calculated_total_price))

    def place_order(self, name, credit_card):
        self.click(self.place_order_button)
        self.wait_for_element_visible(self.place_order_modal)
        self.input(self.place_order_name, name)
        self.input(self.place_order_credit_card, credit_card)

    def purchase(self):
        self.click(self.place_order_purchase_button)

    def get_purchased_amount(self):
        sweet_amount_message = self.get_text(self.sweet_alert_message).split('\n')[1]
        return int(sweet_amount_message.split(' ')[1])

    def validate_purchased_amount(self, amount):
        self.assertEqual(self.calculated_total_price, amount,
                         'Purchased amount is not expected: ' + str(amount)
                         + ' | ex:' + str(self.calculated_total_price))

    def validate_cart_items(self, api_url, assertions):
        cookie = self.driver.get_cookies()[0]
        self.assertEqual(cookie.get('name'), 'tokenp_')
        item_id = self.get_item_id(api_url, cookie.get('value'), assertions.get('items_amount'))
        item_json = self.get_item_details(api_url, item_id)
        self.assertEqual(item_json['price'], assertions.get('price'))
        self.assertEqual(item_json['title'], assertions.get('title'))
        self.assertEqual(item_json['id'], assertions.get('id'))
