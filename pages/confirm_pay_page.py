import re
from playwright.async_api import Page


def normalize_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()


class ConfirmPayPage:
    def __init__(self, page: Page):
        self.page = page
        # Locators
        self.phone_input = self.page.get_by_test_id("login-signup-phonenumber")
        self.continue_button = self.page.get_by_role("button", name="Continue")

    async def fill_phone_number(self, phone: str):
        try:
            await self.phone_input.click()
            await self.phone_input.fill(phone)
        except:
            return

    async def get_reservation_details_template_2(self):
        reservation_details = {}
        summary_header = self.page.get_by_test_id(
            "checkout-product-details-listing-card"
        )
        summary_details = await summary_header.text_content()
        reservation_details["property_name"] = summary_details

        # Locate the parent container of trip details
        trip_container = (
            await self.page.locator("div:has-text('Trip details')")
            .nth(0)
            .locator("xpath=..")
        )

        # Extract dates and guest info
        dates_text = await trip_container.locator(
            "div >> nth=1 >> div >> nth=0"
        ).text_content()
        guests_text = await trip_container.locator(
            "div >> nth=1 >> div >> nth=1"
        ).text_content()

        reservation_details["dates"] = dates_text
        reservation_details["guests_text"] = guests_text
        guest_numbers = list(map(int, re.findall(r"\d+", guests_text)))
        total_guests = sum(guest_numbers)
        reservation_details["guests"] = f"{total_guests} guests"
        total_price_locator = self.page.get_by_test_id("pd-value-TOTAL")
        reservation_details["total_price"] = await total_price_locator.text_content()

        match_price = re.search(r"[\d,]+", reservation_details["total_price"])

        if match_price:
            number_str = match_price.group().replace(",", "")
            reservation_details["total_price_number"] = int(number_str)

        print("Reservation details", reservation_details)
        return reservation_details

    async def get_reservation_details(self):
        reservation_details = {}

        # Extract Dates
        dates_parent = self.page.locator("h3:has-text('Dates')").locator("xpath=../..")
        dates_text = await dates_parent.locator("div >> nth=1").text_content()
        reservation_details["dates"] = dates_text

        # Extract Guests
        guests_parent = self.page.locator("h3:has-text('Guests')").locator(
            "xpath=../.."
        )
        guests_text = await guests_parent.locator("div >> nth=1").text_content()
        reservation_details["guests"] = normalize_whitespace(guests_text)

        # Extract Property Name
        property_name_locator = self.page.locator("#LISTING_CARD-title")
        property_name = await property_name_locator.text_content()
        reservation_details["property_name"] = normalize_whitespace(property_name)

        # Extract Total Price
        total_price_locator = self.page.get_by_test_id("price-item-total")
        reservation_details["total_price"] = await total_price_locator.text_content()

        match_price = re.search(r"[\d,]+", reservation_details["total_price"])

        if match_price:
            number_str = match_price.group().replace(",", "")
            reservation_details["total_price_number"] = int(number_str)

        print("Reservation details", reservation_details)
        return reservation_details
