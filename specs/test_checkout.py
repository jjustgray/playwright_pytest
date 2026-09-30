import re
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.payment_page import PaymentPage
from pages.products_page import ProductsPage
from pages.signup_page import SignupPage
from specs.fixtures.checkout_helpers import (
    _add_two_products_to_cart,
    _pay_for_order,
    _place_order,
    _register_user,
)


@allure.feature("Checkout")
class TestCheckout:

    @pytest.mark.regression
    @allure.story("TC-14: Place Order - Register while Checkout")
    def test_register_while_checkout(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        payment_page: PaymentPage,
        login_page: LoginPage,
        signup_page: SignupPage,
        order_user_data: dict,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        _add_two_products_to_cart(main_page, products_page)
        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(2)
        cart_page.proceed_to_checkout()
        expect(cart_page.register_login_button).to_be_visible()
        cart_page.click_register_login()

        expect(login_page.signup_heading).to_be_visible()
        _register_user(login_page, signup_page, order_user_data)
        expect(main_page.logged_in_as_text).to_contain_text(
            f"Logged in as {order_user_data['name']}"
        )
        main_page.click_cart_button()
        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        cart_page.proceed_to_checkout()
        expect(page).to_have_url(re.compile(r".*/checkout/?$"))
        expect(checkout_page.delivery_address).to_be_visible()
        expect(checkout_page.invoice_address).to_be_visible()
        expect(checkout_page.order_review).to_be_visible()
        _place_order(checkout_page)
        expect(page).to_have_url(re.compile(r".*/payment/?$"))
        _pay_for_order(payment_page)
        expect(payment_page.order_success_message).to_contain_text(
            "Congratulations! Your order has been confirmed!"
        )

        main_page.click_delete_account_button()
        expect(main_page.deleted_account_heading).to_be_visible()
        signup_page.click_continue_button()

    @pytest.mark.regression
    @allure.story("TC-15: Place Order - Register before Checkout")
    def test_register_before_checkout(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        payment_page: PaymentPage,
        login_page: LoginPage,
        signup_page: SignupPage,
        order_user_data: dict,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        main_page.click_signup_login_button()
        expect(login_page.signup_heading).to_be_visible()
        _register_user(login_page, signup_page, order_user_data)
        expect(main_page.logged_in_as_text).to_contain_text(
            f"Logged in as {order_user_data['name']}"
        )
        _add_two_products_to_cart(main_page, products_page)
        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(2)
        cart_page.proceed_to_checkout()
        expect(page).to_have_url(re.compile(r".*/checkout/?$"))
        expect(checkout_page.delivery_address).to_be_visible()
        expect(checkout_page.invoice_address).to_be_visible()
        expect(checkout_page.order_review).to_be_visible()
        _place_order(checkout_page)
        expect(page).to_have_url(re.compile(r".*/payment/?$"))
        _pay_for_order(payment_page)
        expect(payment_page.order_success_message).to_contain_text(
            "Congratulations! Your order has been confirmed!"
        )

        main_page.click_delete_account_button()
        expect(main_page.deleted_account_heading).to_be_visible()
        signup_page.click_continue_button()

    @pytest.mark.smoke
    @allure.story("TC-16: Place Order - Login before Checkout")
    def test_login_before_checkout(
        self,
        main_page: MainPage,
        login_page: LoginPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        payment_page: PaymentPage,
        signup_page: SignupPage,
        registered_order_user: dict,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        main_page.click_signup_login_button()
        expect(login_page.login_heading).to_be_visible()
        login_page.fill_login_form(
            registered_order_user["email"],
            registered_order_user["password"],
        )
        login_page.click_login_button()
        expect(main_page.logged_in_as_text).to_contain_text(
            f"Logged in as {registered_order_user['name']}")

        _add_two_products_to_cart(main_page, products_page)
        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(2)
        cart_page.proceed_to_checkout()
        expect(page).to_have_url(re.compile(r".*/checkout/?$"))
        expect(checkout_page.delivery_address).to_be_visible()
        expect(checkout_page.invoice_address).to_be_visible()
        expect(checkout_page.order_review).to_be_visible()
        _place_order(checkout_page)
        expect(page).to_have_url(re.compile(r".*/payment/?$"))
        _pay_for_order(payment_page)
        expect(payment_page.order_success_message).to_contain_text(
            "Congratulations! Your order has been confirmed!"
        )

        main_page.click_delete_account_button()
        expect(main_page.deleted_account_heading).to_be_visible()
        signup_page.click_continue_button()

    @pytest.mark.regression
    @allure.story("TC-23: Verify Address Details in Checkout Page")
    def test_address_details_in_checkout(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        login_page: LoginPage,
        signup_page: SignupPage,
        order_user_data: dict,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        main_page.click_signup_login_button()
        expect(login_page.signup_heading).to_be_visible()
        _register_user(login_page, signup_page, order_user_data)
        expect(main_page.logged_in_as_text).to_contain_text(
            f"Logged in as {order_user_data['name']}"
        )
        _add_two_products_to_cart(main_page, products_page)
        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(2)
        cart_page.proceed_to_checkout()

        expect(page).to_have_url(re.compile(r".*/checkout/?$"))
        for address in (
            checkout_page.delivery_address,
            checkout_page.invoice_address,
        ):
            address_text = address.inner_text()
            for field in (
                "first_name",
                "last_name",
                "company",
                "address1",
                "address2",
                "city",
                "state",
                "zipcode",
                "country",
                "mobile_number",
            ):
                assert order_user_data[field] in address_text

        main_page.click_delete_account_button()
        expect(main_page.deleted_account_heading).to_be_visible()
        signup_page.click_continue_button()

    @pytest.mark.regression
    @allure.story("TC-24: Download Invoice after Purchase Order")
    def test_download_invoice_after_purchase(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        cart_page: CartPage,
        checkout_page: CheckoutPage,
        payment_page: PaymentPage,
        login_page: LoginPage,
        signup_page: SignupPage,
        order_user_data: dict,
        page: Page,
    ):
        expect(main_page.slider_section).to_be_visible()
        _add_two_products_to_cart(main_page, products_page)
        expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
        expect(cart_page.product_rows).to_have_count(2)
        cart_page.proceed_to_checkout()
        expect(cart_page.register_login_button).to_be_visible()
        cart_page.click_register_login()

        expect(login_page.signup_heading).to_be_visible()
        _register_user(login_page, signup_page, order_user_data)
        expect(main_page.logged_in_as_text).to_contain_text(
            f"Logged in as {order_user_data['name']}"
        )
        main_page.click_cart_button()
        cart_page.proceed_to_checkout()
        expect(page).to_have_url(re.compile(r".*/checkout/?$"))
        expect(checkout_page.delivery_address).to_be_visible()
        expect(checkout_page.invoice_address).to_be_visible()
        expect(checkout_page.order_review).to_be_visible()
        _place_order(checkout_page)
        expect(page).to_have_url(re.compile(r".*/payment/?$"))
        _pay_for_order(payment_page)
        expect(payment_page.order_success_message).to_contain_text(
            "Congratulations! Your order has been confirmed!"
        )

        invoice = payment_page.download_invoice()
        assert invoice.failure() is None
        invoice_path = invoice.path()
        assert invoice_path is not None
        assert Path(invoice_path).is_file()

        payment_page.click_continue_button()
        main_page.click_delete_account_button()
        expect(main_page.deleted_account_heading).to_be_visible()
        signup_page.click_continue_button()
