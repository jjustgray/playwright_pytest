import re

import allure
import pytest
from playwright.sync_api import Page, expect

from pages.main_page import MainPage
from pages.products_page import ProductsPage


@allure.feature("Products")
class TestProducts:

    @pytest.mark.smoke
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

    @pytest.mark.regression
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

    @pytest.mark.regression
    @allure.story("TC-18: View Category Products")
    @pytest.mark.parametrize(
        "category, subcategory, url_pattern, expected_heading",
        [
            ("women", "Tops", r".*/category_products/2/?$", "WOMEN - TOPS PRODUCTS"),
            ("men", "Tshirts", r".*/category_products/3/?$", "MEN - TSHIRTS PRODUCTS"),
        ],
        ids=["women_tops", "men_tshirts"],
    )
    def test_view_category_products(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        page: Page,
        category: str,
        subcategory: str,
        url_pattern: str,
        expected_heading: str,
    ):
        main_page.click_products_button()
        expect(products_page.category_sidebar).to_be_visible()

        if category == "women":
            expect(products_page.women_category).to_be_visible()
            products_page.expand_women_category()
            products_page.click_women_subcategory(subcategory)
        elif category == "men":
            expect(products_page.men_category).to_be_visible()
            products_page.expand_men_category()
            products_page.click_men_subcategory(subcategory)

        expect(page).to_have_url(re.compile(url_pattern))
        expect(products_page.brand_products_heading).to_contain_text(
            expected_heading, ignore_case=True
        )

    @pytest.mark.regression
    @allure.story("TC-19: View and Cart Brand Products")
    @pytest.mark.parametrize(
        "brand_index",
        [0, 1],
        ids=["first_brand", "second_brand"],
    )
    def test_view_brand_products(
        self,
        main_page: MainPage,
        products_page: ProductsPage,
        page: Page,
        brand_index: int,
    ):
        main_page.click_products_button()
        expect(products_page.all_products_heading).to_be_visible()
        expect(products_page.brands_sidebar).to_be_visible()
        expect(products_page.brand_links).not_to_have_count(0)

        text = products_page.brand_links.nth(brand_index).inner_text()
        text = text.splitlines()[-1].strip() if "\n" in text else text.strip()
        brand_name = re.sub(r"^\(\d+\)\s*", "", text)

        products_page.click_brand(brand_index)
        expect(page).to_have_url(re.compile(r".*/brand_products/.+/?$"))
        expect(products_page.brand_products_heading).to_contain_text(
            re.compile(rf"Brand\s*-\s*{re.escape(brand_name)} Products", re.I)
        )
        expect(products_page.product_cards.first).to_be_visible()

    @pytest.mark.regression
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
