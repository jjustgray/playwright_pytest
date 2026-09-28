import re

import allure
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.main_page import MainPage
from pages.products_page import ProductsPage


@allure.feature("Cart")
class TestCart:

    @allure.story("TC-12: Add Products in Cart")
    def test_add_products_to_cart(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        main_page.click_products_button()

        products_page.add_product_to_cart(0)
        products_page.continue_shopping()
        products_page.add_product_to_cart(1)
        products_page.view_cart_from_modal()

        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.cart_heading).to_be_visible()
        expect(cart_page.product_rows).to_have_count(2)

        first_product = cart_page.product_row(1)
        second_product = cart_page.product_row(2)
        expect(first_product.locator(".cart_description")).to_contain_text(
            "Blue Top")
        expect(first_product.locator(".cart_price")).to_contain_text("Rs. 500")
        expect(first_product.locator(".cart_quantity")).to_contain_text("1")
        expect(first_product.locator(".cart_total")).to_contain_text("Rs. 500")
        expect(second_product.locator(".cart_description")).to_contain_text(
            "Men Tshirt")
        expect(second_product.locator(".cart_price")
               ).to_contain_text("Rs. 400")
        expect(second_product.locator(".cart_quantity")).to_contain_text("1")
        expect(second_product.locator(".cart_total")
               ).to_contain_text("Rs. 400")

    @allure.story("TC-13: Verify Product Quantity in Cart")
    def test_product_quantity_in_cart(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        products_page.click_first_view_product()
        expect(page).to_have_url(re.compile(r".*/product_details/1/?$"))

        products_page.set_quantity(4)
        products_page.add_product_details_to_cart()
        products_page.view_cart_from_modal()

        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(1)
        expect(cart_page.product_row(1).locator(
            ".cart_quantity button")).to_have_text("4")

    @allure.story("TC-17: Remove Products From Cart")
    def test_remove_product_from_cart(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        main_page.click_products_button()
        products_page.add_product_to_cart(0)
        products_page.continue_shopping()
        products_page.add_product_to_cart(1)
        products_page.view_cart_from_modal()

        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(2)
        cart_page.remove_product(1)
        expect(cart_page.product_row(1)).to_have_count(0)
        expect(cart_page.product_rows).to_have_count(1)
