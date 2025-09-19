"""Chrome integration for web research and automation."""

import asyncio
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from ..core.config import Config

logger = logging.getLogger(__name__)


class ChromeIntegration:
    """Chrome browser integration for web research and automation."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize Chrome integration."""
        self.config = config or Config.from_env()
        self.driver = None
        self.playwright_browser = None
        self.playwright_context = None
        self.playwright_page = None
        
        if not SELENIUM_AVAILABLE and not PLAYWRIGHT_AVAILABLE:
            logger.warning("Neither Selenium nor Playwright is available. Chrome integration will be limited.")
    
    async def search_web(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Search the web using Google and return results."""
        try:
            if PLAYWRIGHT_AVAILABLE:
                return await self._search_with_playwright(query, num_results)
            elif SELENIUM_AVAILABLE:
                return await self._search_with_selenium(query, num_results)
            else:
                return [{
                    "title": "Chrome Integration Not Available",
                    "url": "",
                    "description": "Neither Selenium nor Playwright is installed. Please install one of them for web search functionality."
                }]
        except Exception as e:
            logger.error(f"Error in web search: {e}")
            return [{
                "title": "Search Error",
                "url": "",
                "description": f"An error occurred during web search: {str(e)}"
            }]
    
    async def _search_with_playwright(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """Search using Playwright."""
        results = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.config.chrome_headless)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Go to Google
                await page.goto("https://www.google.com")
                
                # Accept cookies if present
                try:
                    await page.click('button:has-text("Accept all")', timeout=3000)
                except:
                    pass
                
                # Search
                await page.fill('input[name="q"]', query)
                await page.press('input[name="q"]', 'Enter')
                
                # Wait for results
                await page.wait_for_selector('.g')
                
                # Extract results
                search_results = await page.query_selector_all('.g')
                
                for i, result in enumerate(search_results[:num_results]):
                    try:
                        title_element = await result.query_selector('h3')
                        link_element = await result.query_selector('a')
                        description_element = await result.query_selector('.VwiC3b')
                        
                        title = await title_element.inner_text() if title_element else "No title"
                        url = await link_element.get_attribute('href') if link_element else ""
                        description = await description_element.inner_text() if description_element else ""
                        
                        results.append({
                            "title": title,
                            "url": url,
                            "description": description
                        })
                    except Exception as e:
                        logger.debug(f"Error extracting result {i}: {e}")
                        continue
                
                await browser.close()
                
        except Exception as e:
            logger.error(f"Playwright search error: {e}")
            results = [{
                "title": "Search Error",
                "url": "",
                "description": f"Error during search: {str(e)}"
            }]
        
        return results
    
    async def _search_with_selenium(self, query: str, num_results: int) -> List[Dict[str, str]]:
        """Search using Selenium."""
        results = []
        
        try:
            # Set up Chrome options
            chrome_options = Options()
            if self.config.chrome_headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            # Initialize driver
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # Go to Google
                driver.get("https://www.google.com")
                
                # Accept cookies if present
                try:
                    accept_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I agree')]"))
                    )
                    accept_button.click()
                except TimeoutException:
                    pass
                
                # Find search box and search
                search_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "q"))
                )
                search_box.send_keys(query)
                search_box.submit()
                
                # Wait for results
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "g"))
                )
                
                # Extract results
                search_results = driver.find_elements(By.CLASS_NAME, "g")
                
                for i, result in enumerate(search_results[:num_results]):
                    try:
                        title_element = result.find_element(By.TAG_NAME, "h3")
                        link_element = result.find_element(By.TAG_NAME, "a")
                        
                        title = title_element.text if title_element else "No title"
                        url = link_element.get_attribute("href") if link_element else ""
                        
                        # Try to get description
                        description = ""
                        try:
                            desc_element = result.find_element(By.CLASS_NAME, "VwiC3b")
                            description = desc_element.text
                        except:
                            pass
                        
                        results.append({
                            "title": title,
                            "url": url,
                            "description": description
                        })
                    except Exception as e:
                        logger.debug(f"Error extracting result {i}: {e}")
                        continue
            
            finally:
                driver.quit()
                
        except Exception as e:
            logger.error(f"Selenium search error: {e}")
            results = [{
                "title": "Search Error",
                "url": "",
                "description": f"Error during search: {str(e)}"
            }]
        
        return results
    
    async def scrape_webpage(self, url: str) -> Dict[str, str]:
        """Scrape content from a webpage."""
        try:
            if PLAYWRIGHT_AVAILABLE:
                return await self._scrape_with_playwright(url)
            elif SELENIUM_AVAILABLE:
                return await self._scrape_with_selenium(url)
            else:
                return {
                    "title": "Scraping Not Available",
                    "content": "Neither Selenium nor Playwright is installed for web scraping.",
                    "url": url
                }
        except Exception as e:
            logger.error(f"Error scraping webpage: {e}")
            return {
                "title": "Scraping Error",
                "content": f"Error scraping webpage: {str(e)}",
                "url": url
            }
    
    async def _scrape_with_playwright(self, url: str) -> Dict[str, str]:
        """Scrape webpage using Playwright."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.config.chrome_headless)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto(url)
            
            title = await page.title()
            content = await page.inner_text('body')
            
            await browser.close()
            
            return {
                "title": title,
                "content": content[:5000],  # Limit content length
                "url": url
            }
    
    async def _scrape_with_selenium(self, url: str) -> Dict[str, str]:
        """Scrape webpage using Selenium."""
        chrome_options = Options()
        if self.config.chrome_headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            driver.get(url)
            
            title = driver.title
            content = driver.find_element(By.TAG_NAME, "body").text
            
            return {
                "title": title,
                "content": content[:5000],  # Limit content length
                "url": url
            }
        finally:
            driver.quit()
    
    async def close(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
        
        if self.playwright_browser:
            await self.playwright_browser.close()