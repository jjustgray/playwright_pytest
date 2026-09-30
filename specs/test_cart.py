import re

import allure
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.login_page import LoginPage
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

    @allure.story("TC-20: Search Products and Verify Cart After Login")
    def test_search_products_and_verify_cart_after_login(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        login_page: LoginPage,
        registered_order_user: dict,
        page: Page,
    ):
        search_term = "Top"
        main_page.click_products_button()
        expect(page).to_have_url(re.compile(r".*/products/?$"))
        expect(products_page.all_products_heading).to_be_visible()

        products_page.search_product(search_term)
        expect(products_page.searched_products_heading).to_be_visible()
        product_count = products_page.product_cards.count()
        assert product_count > 0
        for index in range(product_count):
            expect(products_page.product_cards.nth(index)).to_be_visible()
            products_page.add_product_to_cart(index)
            if index < product_count - 1:
                products_page.continue_shopping()

        products_page.continue_shopping()
        main_page.click_cart_button()
        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(product_count)
        for row in cart_page.product_rows.all():
            expect(row).to_be_visible()

        main_page.click_signup_login_button()
        expect(login_page.login_heading).to_be_visible()
        login_page.fill_login_form(
            registered_order_user["email"],
            registered_order_user["password"],
        )
        login_page.click_login_button()
        expect(main_page.logged_in_as_text).to_be_visible()

        main_page.click_cart_button()
        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(product_count)
        for row in cart_page.product_rows.all():
            expect(row).to_be_visible()

    @allure.story("TC-22: Add to Cart from Recommended Items")
    def test_add_recommended_product_to_cart(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        products_page.scroll_to_recommended_items()
        expect(products_page.recommended_items).to_be_visible()
        expect(products_page.recommended_product_cards.first).to_be_visible()

        products_page.add_recommended_product_to_cart()
        products_page.view_cart_from_modal()

        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(1)
