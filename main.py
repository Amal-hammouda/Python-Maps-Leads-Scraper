import pandas as pd
from playwright.sync_api import sync_playwright
import time


def run_maps_scraper(search_keyword, max_results=50):
    """
    Complete Google Maps Scraper with Auto-Scrolling.
    Optimized for lead generation and professional data extraction.
    """
    with sync_playwright() as p:
        # Launching the browser
        browser = p.chromium.launch(headless=False)  # Keep headless=False to watch the magic
        page = browser.new_page()

        print(f"[*] Starting Professional Scraping for: {search_keyword}")

        # Navigate to Google Maps
        formatted_query = search_keyword.replace(" ", "+")
        page.goto(f"https://www.google.com/maps/search/{formatted_query}")

        # Handle Cookie Consent if it pops up
        try:
            if page.locator('//button[@aria-label="Tout accepter"]').is_visible():
                page.locator('//button[@aria-label="Tout accepter"]').click()
        except:
            pass

        # SCROLLING LOGIC: To get more results
        print("[*] Scrolling to find more leads...")
        for _ in range(5):  # Scroll 5 times to load more listings
            page.mouse.wheel(0, 5000)
            time.sleep(2)

        results = []
        # Locate all business listings
        listings = page.locator('//a[contains(@href, "/maps/place/")]').all()

        print(f"[*] Found {len(listings)} potential leads. Extracting details...")

        for i, listing in enumerate(listings[:max_results]):
            try:
                listing.click()
                page.wait_for_timeout(2000)  # Wait for details pane

                # 1. Name
                name = "N/A"
                name_xpath = '//h1[contains(@class, "DUwDvf")]'
                if page.locator(name_xpath).is_visible():
                    name = page.locator(name_xpath).inner_text()

                # 2. Phone
                phone = "N/A"
                phone_xpath = '//button[contains(@data-item-id, "phone:tel")]'
                if page.locator(phone_xpath).is_visible():
                    phone = page.locator(phone_xpath).inner_text()

                # 3. Website
                website = "N/A"
                web_xpath = '//a[contains(@data-item-id, "authority")]'
                if page.locator(web_xpath).is_visible():
                    website = page.locator(web_xpath).get_attribute("href")

                # 4. Address
                address = "N/A"
                addr_xpath = '//button[contains(@data-item-id, "address")]'
                if page.locator(addr_xpath).is_visible():
                    address = page.locator(addr_xpath).inner_text()

                results.append({
                    "Business Name": name,
                    "Phone Number": phone,
                    "Website": website,
                    "Address": address
                })
                print(f"[+] {i + 1}/{max_results}: Extracted {name}")

            except Exception as e:
                print(f"[!] Error at result {i + 1}: Skip.")
                continue

        # Save to Excel
        df = pd.DataFrame(results)
        output_file = "final_business_leads.xlsx"
        df.to_excel(output_file, index=False)

        print(f"\n[SUCCESS] Extracted {len(results)} leads into '{output_file}'")
        browser.close()


if __name__ == "__main__":
    # Change the search here for your customer
    # Example: "Dentists in Paris" or "IT Companies in Lyon"
    target = "Real Estate Agencies in Lyon"
    run_maps_scraper(target, max_results=20)