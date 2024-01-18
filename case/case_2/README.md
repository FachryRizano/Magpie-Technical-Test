# Case 2

### 1. Issue: IP Bans and CAPTCHAS

**Problem:** High-volume scraping can be easily detected by Tokopedia's anti-scraping systems. This could lead to IP blocking or serving of CAPTCHAs, hindering data collection.

**Solution:** Implement a more sophisticated scraping strategy. Use rotating proxies to mask the scraper's IP address, reducing the risk of being blocked. Additionally, consider implementing 'human-like' interaction patterns in the scraping script (like varying request timings) to mimic natural browsing behavior, which is less likely to trigger anti-bot measures.

### Challenge 2: Scalability and Efficiency

**Problem:** As the scraping task scales up to cover more brands and pages, the process can become inefficient and time-consuming, especially if done sequentially.

**Solution:** Utilize a multi-threaded or asynchronous approach to make requests in parallel, significantly reducing the overall scraping time or API scraping directly (need Proof Of Concept). Care should be taken to balance the load to avoid overwhelming the server, which could lead to detection or errors.

### 3. Issue: Web Page Element Changes

**Problem:** A significant redesign or update of the Tokopedia website can render existing scraping scripts ineffective, as they rely on specific elements and their attributes to extract data.

**Solution:** Regularly monitor and update the scraping code to accommodate changes in the website's structure and layout. This might involve adjusting XPath or CSS selectors used in the script to align with the new webpage elements.

Based on the provided Study Case 1, which involves scraping SKU data from Tokopedia's search pages for certain brands, let's address the potential challenges in Study Case 2. Here, we'll focus on issues that could arise when scaling up the scraping process and propose solutions to mitigate these challenges.

