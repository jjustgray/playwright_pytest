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
):
    main_page.click_products_button()
    products_page.add_product_to_cart(0)
    products_page.continue_shopping()
    products_page.add_product_to_cart(1)
    products_page.continue_shopping()
    main_page.click_cart_button()


def _register_user(
    login_page: LoginPage,
    signup_page: SignupPage,
    user_data: dict,
):
    login_page.fill_signup_form(user_data["name"], user_data["email"])
    login_page.click_signup_button()
    signup_page.fill_account_form(user_data)
    signup_page.fill_address_form(user_data)
    signup_page.click_create_account_button()
    signup_page.click_continue_button()


def _place_order(checkout_page: CheckoutPage):
    checkout_page.enter_comment("Please deliver my order carefully.")
    checkout_page.place_order()


def _pay_for_order(payment_page: PaymentPage):
    payment_page.fill_payment_details(PAYMENT_DATA)
    payment_page.pay_and_confirm_order()
