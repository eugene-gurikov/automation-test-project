import pytest
import os

from objects.home_page import HomePage
from objects.property_reader import get_prop
from datetime import datetime


class AllTests(HomePage):

    homepage_url = get_prop('homepage_url')
    api_url = get_prop('api_url')
    username = 'au_testUser_' + datetime.now().strftime("%d%m%Y_%H%M%S")
    password = get_prop('password')
    credit_card = get_prop('credit_card')
    devices = {'Phones': 'Nexus 6', 'Laptops': 'MacBook Pro'}
    api_call_assertions = {'items_amount': 1, 'price': 650.0, 'title': 'Nexus 6', 'id': 3}

    # additional way to handle user creation:
    # @pytest.fixture(scope='session', autouse=True)
    # def before_suite_create_user(self):
    #     super().setUp()
    #     ...

    def setUp(self):
        super().setUp()
        """Open home page"""
        self.open(self.homepage_url)
        self.homepage_visible()

        """Precondition steps: create user (if not) and login"""
        if os.environ.get('user_created') != 'True':
            self.create_user(self.username, self.password)
        self.login(self.username, self.password)

    @pytest.mark.order(0)
    def test_ui_based(self):
        """ Step 1 - Add devices to cart"""
        for category, device in self.devices.items():
            self.open(self.homepage_url)
            self.homepage_visible()
            self.add_device_to_cart(category, device)

        """Step 2 - Open cart page and do validations"""
        self.open_cart_page()
        self.cart_page_visible()
        self.validate_devices_list(self.devices)
        self.validate_total_price()

        """Step 3 - Place order, purchase and validate purchased amount"""
        self.place_order(self.username, self.credit_card)
        self.purchase()
        amount = self.get_purchased_amount()
        self.validate_purchased_amount(amount)

    @pytest.mark.order(1)
    @pytest.mark.depends(on=['test_ui_based'])
    def test_api_call(self):
        self.homepage_visible()

        """Step 1 - add Nexus 6 (first in the list) device to cart"""
        self.add_device_to_cart(list(self.devices.keys())[0], list(self.devices.values())[0])

        """Step 2 - Open cart page and validate device by api call"""
        self.open_cart_page()
        self.cart_page_visible()
        self.validate_cart_items(self.api_url, self.api_call_assertions)
