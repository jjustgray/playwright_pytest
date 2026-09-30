import re

from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.payment_page import PaymentPage
from pages.products_page import ProductsPage
from pages.signup_page import SignupPage


PAYMENT_DATA = {
    "name": "Test Shopper",
    "card_number": "4111111111111111",
    "cvc": "123",
    "expiry_month": "12",
    "expiry_year": "2030",
}


def _add_two_products_to_cart(
    main_page: MainPage,
    products_page: ProductsPage,
    cart_page: CartPage,
    page: Page,
):
    main_page.click_products_button()
    products_page.add_product_to_cart(0)
    products_page.continue_shopping()
    products_page.add_product_to_cart(1)
    products_page.continue_shopping()
    main_page.click_cart_button()
    expect(page).to_have_url(re.compile(r".*/view_cart/?$"))
    expect(cart_page.product_rows).to_have_count(2)


def _register_user(
    main_page: MainPage,
    login_page: LoginPage,
    signup_page: SignupPage,
    user_data: dict,
):
    expect(login_page.signup_heading).to_be_visible()
    login_page.fill_signup_form(user_data["name"], user_data["email"])
    login_page.click_signup_button()
    expect(signup_page.signup_heading).to_be_visible()
    signup_page.fill_account_form(user_data)
    signup_page.fill_address_form(user_data)
    signup_page.click_create_account_button()
    expect(signup_page.account_created_heading).to_be_visible()
    signup_page.click_continue_button()
    expect(main_page.logged_in_as_text).to_contain_text(
        f"Logged in as {user_data['name']}"
    )


def _complete_order(
    checkout_page: CheckoutPage,
    payment_page: PaymentPage,
    page: Page,
):
    expect(page).to_have_url(re.compile(r".*/checkout/?$"))
    expect(checkout_page.delivery_address).to_be_visible()
    expect(checkout_page.invoice_address).to_be_visible()
    expect(checkout_page.order_review).to_be_visible()
    checkout_page.enter_comment("Please deliver my order carefully.")
    checkout_page.place_order()

    expect(page).to_have_url(re.compile(r".*/payment/?$"))
    payment_page.fill_payment_details(PAYMENT_DATA)
    payment_page.pay_and_confirm_order()
    expect(payment_page.order_success_message).to_contain_text(
        "Congratulations! Your order has been confirmed!"
    )
