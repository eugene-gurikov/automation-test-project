from .header import Header
from .cart_page import CartPage
from .device_page import DevicePage


class HomePage(Header, CartPage, DevicePage):
    images_carousel = 'div#carouselExampleIndicators'
    categories = 'a#itemc.list-group-item'
    card_titles = 'div.card-block h4.card-title a'

    def homepage_visible(self):
        Header.header_visible(self)
        self.wait_for_element_visible(self.images_carousel)

    def add_device_to_cart(self, category, device):
        self.select_category(category)
        self.open_device_page(device)
        self.add_to_card()

    def select_category(self, target_category):
        self.click_link(target_category)

    def open_device_page(self, target_device):
        self.click_link(target_device)
        self.assert_equal(self.get_device_title(), target_device, 'Expected device title to be the one that selected!')
