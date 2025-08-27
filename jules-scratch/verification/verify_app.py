from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto("http://localhost:8081", timeout=60000)

        # Wait for the KYC screen to appear
        expect(page.get_by_text("Let's get you verified")).to_be_visible(timeout=30000)

        # Fill out the KYC form
        page.get_by_placeholder("Enter your full name").fill("Jules Winnfield")
        page.get_by_text("Submit & Continue").click()

        # Wait for the main app to load
        expect(page.get_by_text("Send a Load")).to_be_visible(timeout=30000)

        # Take a screenshot of the "Loads" tab
        page.screenshot(path="jules-scratch/verification/loads_tab.png")

        # Navigate to other tabs and take screenshots
        page.get_by_text("Directory").click()
        expect(page.get_by_text("Directory", exact=True)).to_be_visible(timeout=10000)
        page.screenshot(path="jules-scratch/verification/directory_tab.png")

        page.get_by_text("Bookings").click()
        expect(page.get_by_text("Your Bookings")).to_be_visible(timeout=10000)
        page.screenshot(path="jules-scratch/verification/bookings_tab.png")

        page.get_by_text("Activity").click()
        expect(page.get_by_text("Your Activity")).to_be_visible(timeout=10000)
        page.screenshot(path="jules-scratch/verification/activity_tab.png")

        page.get_by_text("Profile").click()
        expect(page.get_by_text("Account Details")).to_be_visible(timeout=10000)
        page.screenshot(path="jules-scratch/verification/profile_tab.png")

    except Exception as e:
        print(f"An error occurred: {e}")
        page.screenshot(path="jules-scratch/verification/error.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
