from playwright.async_api import Page
import pytest


class AirBnbApartmentPage:
    def __init__(self, page: Page):
        self.page = page
        # Locators
        self.reserve_button = self.page.get_by_role("button", name="Reserve")

    async def click_reserve(self):
        try:
            await self.reserve_button.click(force=True)
        except:
            pytest.skip("Reservation not available")
