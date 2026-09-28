import re

import allure
from playwright.sync_api import Page, expect

from pages.main_page import MainPage
from pages.products_page import ProductsPage


@allure.feature("Products")
class TestProducts:

    @allure.story("TC-08: Verify All Products and Product Detail Page")
    def test_all_products_and_product_details(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        main_page.click_products_button()
        expect(page).to_have_url(re.compile(r".*/products/?$"))
        expect(products_page.all_products_heading).to_be_visible()
        expect(products_page.product_cards.first).to_be_visible()

        products_page.click_first_view_product()
        expect(page).to_have_url(re.compile(r".*/product_details/\d+/?$"))
        expect(products_page.product_name).to_be_visible()
        expect(products_page.product_category).to_be_visible()
        expect(products_page.product_price).to_be_visible()
        expect(products_page.product_availability).to_be_visible()
        expect(products_page.product_condition).to_be_visible()
        expect(products_page.product_brand).to_be_visible()

    @allure.story("TC-09: Search Product")
    def test_search_product(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        page: Page,
    ):
        search_term = "Top"

        expect(main_page.slider_section).to_be_visible()
        main_page.click_products_button()
        expect(page).to_have_url(re.compile(r".*/products/?$"))
        expect(products_page.all_products_heading).to_be_visible()

        products_page.search_product(search_term)
        expect(products_page.searched_products_heading).to_be_visible()
        expect(products_page.product_cards.first).to_be_visible()
        for product_card in products_page.product_cards.all():
            expect(product_card).to_be_visible()