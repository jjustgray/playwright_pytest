import uuid

import pytest
import requests

from pages.login_page import LoginPage
from pages.main_page import MainPage


@pytest.fixture
def start_login_signup_flow(main_page: MainPage, login_page: LoginPage):
    from playwright.sync_api import expect

    expect(main_page.slider_section).to_be_visible()
    main_page.click_signup_login_button()


@pytest.fixture
def registered_user():
    user_name = f"Testuser_{uuid.uuid4().hex[:8]}"
    user_data = {
        "name": user_name,
        "email": f"{user_name.lower()}_{uuid.uuid4().hex}@existing.com",
        "password": "Password123!",
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "January",
        "birth_year": "2000",
        "firstname": "Test",
        "lastname": "User",
        "company": "QA Company",
        "address1": "Street 1",
        "address2": "Apt 2",
        "country": "United States",
        "zipcode": "10001",
        "state": "State",
        "city": "City",
        "mobile_number": "1234567890",
    }

    response = requests.post(
        "https://automationexercise.com/api/createAccount",
        data=user_data,
    )
    assert response.status_code == 200

    yield user_data

    requests.delete(
        "https://automationexercise.com/api/deleteAccount",
        data={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )


@pytest.fixture
def order_user_data():
    user_name = f"Shopper{uuid.uuid4().hex[:8]}"
    return {
        "name": user_name,
        "email": f"{user_name.lower()}_{uuid.uuid4().hex}@example.com",
        "password": "Password123!",
        "title": "Mr",
        "day": "1",
        "month": "January",
        "year": "2000",
        "birth_date": "1",
        "birth_month": "January",
        "birth_year": "2000",
        "first_name": "Test",
        "last_name": "Shopper",
        "firstname": "Test",
        "lastname": "Shopper",
        "company": "QA Company",
        "address1": "123 Main Street",
        "address2": "Suite 4",
        "country": "United States",
        "state": "California",
        "city": "Los Angeles",
        "zipcode": "90001",
        "mobile_number": "1234567890",
    }


@pytest.fixture
def registered_order_user(order_user_data):
    response = requests.post(
        "https://automationexercise.com/api/createAccount",
        data=order_user_data,
    )
    assert response.status_code == 200

    yield order_user_data

    requests.delete(
        "https://automationexercise.com/api/deleteAccount",
        data={
            "email": order_user_data["email"],
            "password": order_user_data["password"],
        },
    )
