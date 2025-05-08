import re
from playwright.async_api import Page


class AirBnbSearchResultsPage:
    def __init__(self, page: Page):
        self.page = page
        # Locators
        self.heading_location = self.page.locator(
            "span[data-testid='stays-page-heading'][aria-hidden='true']"
        )
        self.location_search_summary = self.page.get_by_test_id(
            "little-search-location"
        )
        self.guests_search_summary = self.page.get_by_test_id("little-search-guests")
        self.dates_selected_summary = self.page.get_by_test_id("little-search-anytime")
        self.apartment_cards = self.page.locator(
            "div[role='group'][data-testid='card-container']"
        )

    async def get_apartment_cards(self):
        return self.apartment_cards

    async def get_best_apartment(self, checkin, checkout):
        listings = []
        apartments_cards_count = await self.apartment_cards.count()
        for i in range(apartments_cards_count):
            card = self.apartment_cards.nth(i)

            try:
                href = await card.locator("a").first.get_attribute("href")
                if not href:
                    continue

                if checkin not in href or checkout not in href:
                    continue
            except:
                pass

            # Extract price
            try:
                price_text = await card.locator(
                    "span[aria-hidden='true']", has_text="total"
                ).first.text_content()
                price_match = re.search(r"[^\d\s]?([\d,]+)", price_text)
                price = (
                    int(price_match.group(1).replace(",", "")) if price_match else None
                )
            except:
                price = None

            # Extract rating
            try:
                rating_text = await card.locator(
                    "span", has_text="out of 5 average rating"
                ).first.text_content()
                rating_match = re.search(
                    r"(\d+(\.\d+)?) out of 5 average rating", rating_text
                )
                rating = float(rating_match.group(1)) if rating_match else None
            except:
                rating = None

            if price is not None and rating is not None:
                listings.append(
                    {
                        "price": price,
                        "rating": rating,
                        "price_text": price_text,
                        "rating_text": rating_text,
                        "card_index": i,
                    }
                )

        if not listings:
            raise Exception("No complete listings found")

        # Find max rating and best listing with min price
        max_rating = max(l["rating"] for l in listings)
        top_rated = [l for l in listings if l["rating"] == max_rating]
        best_listing = min(top_rated, key=lambda x: x["price"])

        print("Best listing:", best_listing)
        return best_listing

    async def get_apartment_title(self, card_index: int):
        apartment_card = self.apartment_cards.nth(card_index)
        apartment_title = apartment_card.get_by_test_id("listing-card-name")
        return await apartment_title.text_content()

    async def select_apartment(self, card_index: int):
        apartment_card = self.apartment_cards.nth(card_index)
        await apartment_card.click(force=True)
