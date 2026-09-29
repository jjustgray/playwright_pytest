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

    @allure.story("TC-18: View Category Products")
    def test_view_category_products(
        self,
        products_page: ProductsPage,
        page: Page,
    ):
        expect(products_page.category_sidebar).to_be_visible()
        expect(products_page.women_category).to_be_visible()
        expect(products_page.men_category).to_be_visible()

        products_page.expand_women_category()
        products_page.click_women_subcategory("Tops")
        expect(page).to_have_url(re.compile(r".*/category_products/2/?$"))
        expect(products_page.brand_products_heading).to_contain_text(
            "WOMEN - TOPS PRODUCTS", ignore_case=True)

        products_page.expand_men_category()
        products_page.click_men_subcategory("Tshirts")
        expect(page).to_have_url(re.compile(r".*/category_products/3/?$"))
        expect(products_page.brand_products_heading).to_contain_text(
            "MEN - TSHIRTS PRODUCTS", ignore_case=True)

    @allure.story("TC-19: View and Cart Brand Products")
    def test_view_brand_products(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        page: Page,
    ):
        main_page.click_products_button()
        expect(products_page.all_products_heading).to_be_visible()
        expect(products_page.brands_sidebar).to_be_visible()
        expect(products_page.brand_links).not_to_have_count(0)

        first_brand = products_page.brand_links.nth(
            0).inner_text().splitlines()[-1].strip()
        products_page.click_brand(0)
        expect(page).to_have_url(re.compile(r".*/brand_products/.+/?$"))
        expect(products_page.brand_products_heading).to_contain_text(
            re.compile(rf"Brand\s*-\s*{re.escape(first_brand)} Products", re.I))
        expect(products_page.product_cards.first).to_be_visible()

        second_brand = products_page.brand_links.nth(
            1).inner_text().splitlines()[-1].strip()
        products_page.click_brand(1)
        expect(page).to_have_url(re.compile(r".*/brand_products/.+/?$"))
        expect(products_page.brand_products_heading).to_contain_text(
            re.compile(rf"Brand\s*-\s*{re.escape(second_brand)} Products", re.I))
        expect(products_page.product_cards.first).to_be_visible()

    @allure.story("TC-21: Add Review on Product")
    def test_add_review_on_product(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
    ):
        main_page.click_products_button()
        expect(products_page.all_products_heading).to_be_visible()
        products_page.click_first_view_product()

        expect(products_page.review_heading).to_be_visible()
        products_page.fill_review_form(
            "Test Reviewer",
            "reviewer@example.com",
            "A useful product review for automated testing.",
        )
        products_page.submit_review()
        expect(products_page.review_success_message).to_contain_text(
            "Thank you for your review.")