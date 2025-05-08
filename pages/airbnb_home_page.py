from playwright.async_api import Page


class AirBnbHomePage:
    def __init__(self, page: Page):
        self.page = page
        # Locators
        self.search_location_input = self.page.get_by_role("searchbox", name="Where")
        self.search_header = self.page.get_by_text("Where")
        self.check_in_button = self.page.get_by_text("Check in")
        self.check_out_button = self.page.get_by_text("Check out")
        self.who_button = self.page.get_by_text("Who")
        self.add_adult_button = self.page.get_by_test_id(
            "stepper-adults-increase-button"
        )
        self.add_child_button = self.page.get_by_test_id(
            "stepper-children-increase-button"
        )
        self.search_button = self.page.get_by_test_id(
            "structured-search-input-search-button"
        )

    async def goto(self):
        await self.page.goto("https://www.airbnb.com", wait_until="load")
        assert self.page.url == "https://www.airbnb.com/"

    async def enter_location(self, location: str):
        await self.search_location_input.click()
        await self.search_location_input.fill(location)
        await self.page.locator(
            "div[id='bigsearch-query-location-suggestion-0'][role='option']"
        ).click(force=True)

    async def select_dates(self, check_in_date: str, check_out_date: str):
        await self.page.get_by_role(
            "button", name=f"{check_in_date}. Available. Select as check-in date."
        ).click()
        await self.page.get_by_role(
            "button", name=f"{check_out_date}. Available. Select as checkout date."
        ).click()

    async def set_guests(self, adults: int = 2, children: int = 1):
        await self.who_button.click()
        for _ in range(adults):
            await self.add_adult_button.click()
        for _ in range(children):
            await self.add_child_button.click()

    async def submit_search(self):
        await self.search_button.click()

    async def get_destination_value(self):
        return await self.search_location_input.input_value()
