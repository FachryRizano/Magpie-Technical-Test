# Case 1

## Learnings and Solutions

### Overcoming Anti-Scraping Techniques

- **Challenge:** When attempting to scrape Tokopedia using Headless ChromeDriver, the website does not load, indicating detection and blocking of the scraping attempt.
- **Solution:** Switch to Firefox Driver, which seems to bypass Tokopedia's headless scraping detection. This necessitates changes in the scraping script to accommodate a different web driver.

### Handling Dynamic Element Structures

- **Challenge:** Tokopedia's web pages have a dynamic structure, where element selectors change frequently.
- **Solution:** Implement a strategy to identify and adjust to dynamic selectors. This may involve using more general selectors, XPath attributes, or developing a pattern recognition system to adapt to changes in the webpage structure.
