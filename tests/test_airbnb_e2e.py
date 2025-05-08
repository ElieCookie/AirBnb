# 1. Navigate to Airbnb: Open the Airbnb website.
# 2. Search for Apartments: Search apartments for 2 adults and a child in Tel Aviv with random check-in and check-out dates.
# 3. Validate your search parameters in the results (both from the url and the ui)
# 4. Analyze Results:
#   a. Identify the cheapest result among the highest-rated ones (if i have 4 results with 5 stars - choose the cheapest one)
#   b. Log the above result details and save it to a json file in a “temp” folder
# 5. Attempt Reservation:
#   a. Click the "Reserve" button.
#   b. Enter a phone number with a prefix of your choice.
#   c. Re-Validate reservation details, log the and save to a json file in a “temp” folder

import json
import os
import pytest
from pages.airbnb_apartment_page import AirBnbApartmentPage
from pages.airbnb_home_page import AirBnbHomePage
from pages.airbnb_search_results_page import AirBnbSearchResultsPage
from pages.confirm_pay_page import ConfirmPayPage
from utils.date_formatter import random_date_range_airbnb_format
from faker import Faker

fake = Faker()


@pytest.mark.asyncio
async def test_airbnb_search_and_reservation(browser_context):
    page = browser_context
    # Navigate to AirBnb home page
    airbnb_home_page = AirBnbHomePage(page)
    await airbnb_home_page.goto()

    # Step 2: Search
    # Fill location
    await airbnb_home_page.enter_location("Tel Aviv")
    assert "Tel Aviv" in await airbnb_home_page.get_destination_value()

    # Fill dates
    check_in, check_out, iso_check_in, iso_check_out, month_name, start_day, end_day = (
        random_date_range_airbnb_format()
    )
    await airbnb_home_page.select_dates(check_in, check_out)

    # Guests
    adults = 2
    children = 1
    num_guests = 3
    await airbnb_home_page.set_guests(adults, children)

    # Submit search
    await airbnb_home_page.submit_search()
    airbnb_search_results_page = AirBnbSearchResultsPage(airbnb_home_page.page)
    await airbnb_search_results_page.page.wait_for_timeout(3000)

    # Step 3: Validate URL & UI
    assert "Tel-Aviv" in airbnb_search_results_page.page.url
    assert "adults=2" in airbnb_search_results_page.page.url
    assert "children=1" in airbnb_search_results_page.page.url
    assert f"checkin={iso_check_in}" in airbnb_search_results_page.page.url
    assert f"checkout={iso_check_out}" in airbnb_search_results_page.page.url

    # Validate UI details
    assert airbnb_search_results_page.page.get_by_text("Tel Aviv", exact=False)

    assert airbnb_search_results_page.page.get_by_text(
        f"{num_guests} guests", exact=False
    )

    assert airbnb_search_results_page.page.get_by_text(
        f"{month_name} {start_day} – {end_day}", exact=False
    )

    # Step 4: Analyze results
    checkin = f"check_in={iso_check_in}"
    checkout = f"check_out={iso_check_out}"
    best_listing = await airbnb_search_results_page.get_best_apartment(
        checkin, checkout
    )

    os.makedirs("temp", exist_ok=True)
    with open("temp/best_listing.json", "w") as f:
        json.dump(best_listing, f, indent=2)

    apartment_name = await airbnb_search_results_page.get_apartment_title(
        best_listing["card_index"]
    )

    async with page.context.expect_page() as new_page_info:
        await airbnb_search_results_page.select_apartment(best_listing["card_index"])

    new_page = await new_page_info.value
    await new_page.wait_for_load_state()

    airbnb_apartment_page = AirBnbApartmentPage(new_page)

    assert airbnb_apartment_page.page.locator(f"heading[name={apartment_name}]")

    await airbnb_apartment_page.page.wait_for_timeout(1000)
    await airbnb_apartment_page.page.keyboard.press("Escape")

    # Step 5: Attempt reservation
    await airbnb_apartment_page.click_reserve()
    confirm_pay_page = ConfirmPayPage(airbnb_apartment_page.page)
    await confirm_pay_page.page.wait_for_load_state()

    raw_number = fake.msisdn()[-9:]
    await confirm_pay_page.fill_phone_number(f"{raw_number}")

    reservation_details = await confirm_pay_page.get_reservation_details()

    assert apartment_name in reservation_details["property_name"], (
        f'Expected property name to contain "{apartment_name}", '
        f'but got "{reservation_details["property_name"]}"'
    )

    expected_dates = f"{month_name} {start_day} – {end_day}"

    assert expected_dates in reservation_details["dates"], (
        f'Expected dates to contain "{expected_dates}", '
        f'but got "{reservation_details["dates"]}"'
    )

    assert reservation_details["guests"] == f"{num_guests} guests", (
        f'Expected guests to be "{num_guests} guests", '
        f'but got "{reservation_details["guests"]}"'
    )
    assert (
        abs(reservation_details["total_price_number"] - best_listing["price"]) <= 1
    ), (
        f'Expected price to be "{best_listing["price"]}", '
        f'but got "{reservation_details["total_price_number"]}"'
    )

    with open("temp/reservation_summary.json", "w") as f:
        json.dump(reservation_details, f, indent=2)
