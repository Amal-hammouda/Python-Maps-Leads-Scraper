import pandas as pd
from playwright.sync_api import sync_playwright


def run_maps_scraper(search_keyword, total_results=10):
    """
    Professional Google Maps Scraper.
    Extracts: Name, Phone, Website, and Address.
    """
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print(f"[*] Starting search for: {search_keyword}")

        # Navigate to Google Maps
        formatted_query = search_keyword.replace(" ", "+")
        page.goto(f"https://www.google.com/maps/search/{formatted_query}")

        # Wait for the results list to load
        page.wait_for_timeout(5000)

        results = []

        # Locate all business result links
        listings = page.locator('//a[contains(@href, "/maps/place/")]').all()

        # Limit results based on requirements
        for i, listing in enumerate(listings[:total_results]):
            try:
                listing.click()
                page.wait_for_timeout(3000)  # Wait for details pane to open

                # 1. Extract Business Name
                name = "N/A"
                if page.locator('//h1[contains(@class, "DUwDvf")]').is_visible():
                    name = page.locator('//h1[contains(@class, "DUwDvf")]').inner_text()

                # 2. Extract Phone Number
                phone = "N/A"
                phone_locator = page.locator('//button[contains(@data-item-id, "phone:tel")]')
                if phone_locator.is_visible():
                    phone = phone_locator.inner_text()

                # 3. Extract Website
                website = "N/A"
                website_locator = page.locator('//a[contains(@data-item-id, "authority")]')
                if website_locator.is_visible():
                    website = website_locator.get_attribute("href")

                # 4. Extract Physical Address
                address = "N/A"
                address_locator = page.locator('//button[contains(@data-item-id, "address")]')
                if address_locator.is_visible():
                    address = address_locator.inner_text()

                results.append({
                    "Business Name": name,
                    "Phone Number": phone,
                    "Website": website,
                    "Address": address
                })

                print(f"[+] Extracted ({i + 1}): {name}")

            except Exception as e:
                print(f"[!] Error extracting item {i + 1}: {e}")
                continue

        # Create DataFrame and Export to Excel
        df = pd.DataFrame(results)
        file_name = "business_leads_pro.xlsx"
        df.to_excel(file_name, index=False)

        print(f"\n[SUCCESS] Data saved to {file_name}")
        browser.close()


if __name__ == "__main__":
    # You can change the search keyword here to anything you want to sell
    # Example: "Dentists in Paris" or "Real Estate Agencies in Lyon"
    target_search = "Real Estate Agencies in Lyon"
    run_maps_scraper(target_search, total_results=15)