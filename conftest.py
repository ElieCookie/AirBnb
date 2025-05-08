from playwright.async_api import async_playwright, Page
import pytest_asyncio


@pytest_asyncio.fixture
async def browser_context() -> Page:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()
