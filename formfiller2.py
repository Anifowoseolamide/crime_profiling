"""
Google Form Auto-Filler 2
Form: Personnel motivation and productivity in the National Youth Service Corps (NYSC)
URL: https://docs.google.com/forms/d/e/1FAIpQLSd7YsuvAoo6Aqds9t3s6YBIzouT0m9UqUDm8vLlYFJSMxiFOg/viewform
"""

import time
import logging
import random
import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Target Google Form URL
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd7YsuvAoo6Aqds9t3s6YBIzouT0m9UqUDm8vLlYFJSMxiFOg/viewform"

# 100+ Realistic Igbo and Yoruba Dummy Gmail Addresses
DUMMY_EMAILS = [
    # Igbo Gmail Addresses
    "chinedu.okeke88@gmail.com", "emeka.nwachukwu92@gmail.com", "nneka.anyanwu91@gmail.com",
    "chioma.eze20@gmail.com", "ifeanyi.okafor95@gmail.com", "obinna.nwosu11@gmail.com",
    "amaka.okoro99@gmail.com", "chiamaka.umeh84@gmail.com", "uchenna.ik12@gmail.com",
    "ikechukwu.onyeka@gmail.com", "chika.nnamdi89@gmail.com", "ngozi.madu93@gmail.com",
    "ebuka.kelechi96@gmail.com", "kenechukwu.ijeoma@gmail.com", "ozioma.tochukwu@gmail.com",
    "adaeze.okeke94@gmail.com", "chukwudi.okafor87@gmail.com", "nkiru.okoro90@gmail.com",
    "somtochukwu.eze@gmail.com", "osinachi.anyanwu@gmail.com", "chinwe.nwosu@gmail.com",
    "kosi.nwachukwu@gmail.com", "ebere.umeh91@gmail.com", "uche.okeke95@gmail.com",
    "nonso.okafor98@gmail.com", "oluchi.eze93@gmail.com", "chisom.nwosu@gmail.com",
    "chekwube.okoro@gmail.com", "ijeoma.anyanwu@gmail.com", "ekene.nwachukwu@gmail.com",
    "ifeoma.okeke@gmail.com", "chinedum.okafor@gmail.com", "kamsi.eze@gmail.com",
    "somto.nwosu@gmail.com", "chibuzor.okoro@gmail.com", "nwakaego.anyanwu@gmail.com",
    "ebube.nwachukwu@gmail.com", "chidebere.okeke@gmail.com", "obianuju.okafor@gmail.com",
    "lotanna.eze@gmail.com", "amara.nwosu@gmail.com", "chima.okoro@gmail.com",
    "gozie.anyanwu@gmail.com", "kanayo.nwachukwu@gmail.com", "ndidi.okeke@gmail.com",
    "tochi.okafor@gmail.com", "ugochi.eze@gmail.com", "chigozie.nwosu@gmail.com",
    "chinwendu.okoro@gmail.com", "ifechukwu.anyanwu@gmail.com",

    # Yoruba Gmail Addresses
    "olamide.adebayo91@gmail.com", "babatunde.balogun@gmail.com", "folake.ajayi88@gmail.com",
    "oluwaseun.owolabi94@gmail.com", "titilayo.afolabi@gmail.com", "kayode.bakare93@gmail.com",
    "bukola.olatunji87@gmail.com", "tunde.alabi89@gmail.com", "damilola.babalola96@gmail.com",
    "ayomide.adeleke90@gmail.com", "temitope.ogundipe@gmail.com", "kehinde.adebayo@gmail.com",
    "taiwo.balogun@gmail.com", "gbenga.ajayi92@gmail.com", "bolaji.owolabi@gmail.com",
    "yetunde.afolabi@gmail.com", "opeyemi.bakare@gmail.com", "segun.olatunji@gmail.com",
    "funke.alabi@gmail.com", "adeleke.babalola@gmail.com", "eniola.adebayo@gmail.com",
    "pelumi.balogun@gmail.com", "bimpe.ajayi@gmail.com", "kolade.owolabi@gmail.com",
    "motunrayo.afolabi@gmail.com", "olasunkanmi.bakare@gmail.com", "adeola.olatunji@gmail.com",
    "bosede.alabi@gmail.com", "dayo.babalola@gmail.com", "femi.adeleke@gmail.com",
    "fola.ogundipe@gmail.com", "gbemisola.adebayo@gmail.com", "ibukun.balogun@gmail.com",
    "jide.ajayi@gmail.com", "kemi.owolabi@gmail.com", "lanre.afolabi@gmail.com",
    "mide.bakare@gmail.com", "niyi.olatunji@gmail.com", "olaitan.alabi@gmail.com",
    "peju.babalola@gmail.com", "rasheed.adeleke@gmail.com", "sade.ogundipe@gmail.com",
    "tobi.adebayo@gmail.com", "yemi.balogun@gmail.com", "biodun.ajayi@gmail.com",
    "dare.owolabi@gmail.com", "femi.afolabi@gmail.com", "gbenga.bakare@gmail.com",
    "korede.olatunji@gmail.com", "muyiwa.alabi@gmail.com", "ronke.babalola@gmail.com"
]


class FormFiller2:
    def __init__(self, headless=True):
        self.driver = self._create_driver(headless)
        self.wait = WebDriverWait(self.driver, 15)

    def _create_driver(self, headless):
        opts = Options()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        opts.add_argument("--start-maximized")
        opts.add_argument("--log-level=3")
        opts.add_argument("--window-size=1920,1080")

        # Prioritize local cached drivers for fast start
        latest_driver = None
        try:
            wdm_base = os.path.join(os.environ.get('USERPROFILE', ''), '.wdm')
            search_pattern = os.path.join(wdm_base, "**", "chromedriver.exe")
            cached_drivers = glob.glob(search_pattern, recursive=True)
            if cached_drivers:
                latest_driver = max(cached_drivers, key=os.path.getmtime)
                logger.info(f"Found cached driver: {latest_driver}")
        except Exception as e:
            logger.debug(f"Error searching for cached driver: {e}")

        try:
            if latest_driver:
                service = Service(latest_driver)
            else:
                service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=opts)
            driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            return driver
        except Exception as e:
            logger.warning(f"Default driver initialization failed: {e}. Trying fallback.")
            try:
                import undetected_chromedriver as uc
                return uc.Chrome(options=opts)
            except Exception as e2:
                logger.error(f"Fallback driver initialization failed: {e2}")
                raise e2

    def _scroll_to(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', behavior:'auto'});", element
        )

    def _safe_click(self, element):
        """Force JavaScript click to avoid silent selection failures."""
        self._scroll_to(element)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
        time.sleep(0.02)  # Fast timing

    def get_header(self):
        """Find the main section header on the current page."""
        for selector in ["div.F9yp7b", "div.AHrquc", "div.M7eMe", "div[role='heading']"]:
            try:
                el = self.driver.find_element(By.CSS_SELECTOR, selector)
                if el.text.strip():
                    return el.text.strip()
            except NoSuchElementException:
                pass
        return "NYSC Survey Section"

    def _click_random_radio(self, group_el, preferred=None):
        """Click a radio in group_el. If preferred list given, pick from those first."""
        radios = group_el.find_elements(By.CSS_SELECTOR, "div[role='radio']")
        if not radios:
            return
        if preferred:
            candidates = [
                r for r in radios
                if any(p.lower() in (r.get_attribute("aria-label") or r.text or "").lower() for p in preferred)
            ]
            chosen = random.choice(candidates) if candidates else random.choice(radios)
        else:
            chosen = random.choice(radios)
        self._safe_click(chosen)

    def fill_visible_questions(self):
        """Fill every visible question on the current page quickly."""
        # 1. Check and fill Email fields (Google Forms email collector or Email text inputs)
        email_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[autocomplete='email']")
        if not email_inputs:
            text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input.whsOnd")
            for inp in text_inputs:
                lbl = (inp.get_attribute("aria-label") or "").lower()
                if any(k in lbl for k in ("email", "mail", "gmail")):
                    email_inputs.append(inp)

        for inp in email_inputs:
            if inp.is_displayed():
                if not inp.get_attribute("value"):
                    chosen_email = random.choice(DUMMY_EMAILS)
                    self._scroll_to(inp)
                    try:
                        inp.clear()
                        inp.send_keys(chosen_email)
                    except Exception:
                        self.driver.execute_script("arguments[0].removeAttribute('disabled');", inp)
                        inp.clear()
                        inp.send_keys(chosen_email)
                    logger.info(f"  Filled email: {chosen_email}")

        # 2. Fill visible listitem questions
        all_items = self.driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")

        for item in all_items:
            # Get question label
            label = ""
            for sel in ["div.M7eMe", "div[class*='ItemItemTitle']"]:
                try:
                    label = item.find_element(By.CSS_SELECTOR, sel).text.strip().lower()
                    break
                except NoSuchElementException:
                    pass
            if not label:
                try:
                    label = item.text.split("\n")[0].strip().lower()
                except Exception:
                    continue

            # Check if this item has a text/email input asking for email
            if any(k in label for k in ("email", "mail", "gmail")):
                try:
                    inp = item.find_element(By.CSS_SELECTOR, "input[type='text'], input[type='email'], input.whsOnd")
                    if not inp.get_attribute("value"):
                        chosen_email = random.choice(DUMMY_EMAILS)
                        self._scroll_to(inp)
                        try:
                            inp.clear()
                            inp.send_keys(chosen_email)
                        except Exception:
                            self.driver.execute_script("arguments[0].removeAttribute('disabled');", inp)
                            inp.clear()
                            inp.send_keys(chosen_email)
                        logger.info(f"  Filled email field ({label}): {chosen_email}")
                except NoSuchElementException:
                    pass

            # ── Socio-Demographic questions ────────────────────────────────
            if "age" in label:
                try:
                    rg = item.find_element(By.CSS_SELECTOR, "div[role='radiogroup']")
                    self._click_random_radio(rg, preferred=["20-29", "30-39"])
                except NoSuchElementException:
                    pass

            elif "gender" in label:
                try:
                    rg = item.find_element(By.CSS_SELECTOR, "div[role='radiogroup']")
                    self._click_random_radio(rg, preferred=["Male", "Female"])
                except NoSuchElementException:
                    pass

            elif "qualification" in label or "educational" in label:
                try:
                    rg = item.find_element(By.CSS_SELECTOR, "div[role='radiogroup']")
                    self._click_random_radio(rg, preferred=["HND/B.Sc", "Master Degree", "OND/NCE"])
                except NoSuchElementException:
                    pass

            elif "position" in label or "rank" in label:
                try:
                    rg = item.find_element(By.CSS_SELECTOR, "div[role='radiogroup']")
                    self._click_random_radio(rg, preferred=["Junior Staff", "Senior Staff"])
                except NoSuchElementException:
                    pass

            elif "experience" in label or "years" in label:
                try:
                    rg = item.find_element(By.CSS_SELECTOR, "div[role='radiogroup']")
                    self._click_random_radio(rg, preferred=["1-5  years", "6-10 years", "11-15 years"])
                except NoSuchElementException:
                    pass

            elif "employment status" in label:
                try:
                    rg = item.find_element(By.CSS_SELECTOR, "div[role='radiogroup']")
                    self._click_random_radio(rg, preferred=["Permanent", "Contract"])
                except NoSuchElementException:
                    pass

            elif "income" in label or "monthly" in label:
                try:
                    rg = item.find_element(By.CSS_SELECTOR, "div[role='radiogroup']")
                    self._click_random_radio(rg)
                except NoSuchElementException:
                    pass

        # ── Universal fill for any unanswered radiogroups (Likert / Scales / Remaining) ──
        all_rgs = self.driver.find_elements(By.CSS_SELECTOR, "div[role='radiogroup']")
        for rg in all_rgs:
            radios = rg.find_elements(By.CSS_SELECTOR, "div[role='radio']")
            if not radios:
                continue
            if any(r.get_attribute("aria-checked") == "true" for r in radios):
                continue  # already answered

            labels_text = " ".join(
                (r.get_attribute("aria-label") or r.text or "").lower() for r in radios
            )

            # For Likert scale items (Strongly Agree / Agree / etc.), favor Agree / Strongly Agree
            if any(kw in labels_text for kw in ("agree", "disagree", "undecided", "neutral")):
                positive = []
                others = []
                for r in radios:
                    lbl = (r.get_attribute("aria-label") or r.text or "").lower()
                    if "agree" in lbl and "disagree" not in lbl:
                        positive.append(r)
                    else:
                        others.append(r)
                if positive and others:
                    chosen = random.choice(positive) if random.random() < 0.75 else random.choice(others)
                else:
                    chosen = random.choice(radios)
            else:
                chosen = random.choice(radios)

            self._safe_click(chosen)

    def click_next(self):
        """Click the 'Next' button quickly without long delays."""
        next_xpaths = [
            "//div[@role='button'][.//span[normalize-space()='Next']]",
            "//span[normalize-space()='Next']/ancestor::div[@role='button']",
        ]
        for xp in next_xpaths:
            try:
                btn = self.driver.find_element(By.XPATH, xp)
                self._safe_click(btn)
                time.sleep(0.2)  # Fast transition wait
                return True
            except NoSuchElementException:
                pass
        return False

    def submit_form(self):
        """Click the 'Submit' button and confirm submission."""
        submit_xpaths = [
            "//div[@role='button'][.//span[normalize-space()='Submit']]",
            "//span[normalize-space()='Submit']/ancestor::div[@role='button']",
            "//input[@type='submit']",
        ]
        for xp in submit_xpaths:
            try:
                btn = self.driver.find_element(By.XPATH, xp)
                self._safe_click(btn)
                try:
                    self.wait.until(EC.url_contains("formResponse"))
                    logger.info("  Submitted ✓")
                    return True
                except TimeoutException:
                    raise RuntimeError("Form failed to confirm submission (Timeout waiting for response page).")
            except NoSuchElementException:
                pass
        return False

    def fill_once(self):
        """Perform a single form submission across all pages."""
        self.driver.get(FORM_URL)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))
        time.sleep(0.3)

        page_num = 1
        while True:
            header = self.get_header()
            logger.info(f"Page {page_num}: {header[:60]}")

            # Fill all visible questions on this page
            self.fill_visible_questions()
            time.sleep(0.1)

            # Click Next or Submit
            if self.click_next():
                page_num += 1
                time.sleep(0.2)
            else:
                logger.info("No Next button found. Submitting form...")
                if self.submit_form():
                    break
                else:
                    raise RuntimeError("Failed to advance or submit: neither Next nor Submit button found.")

    def close(self):
        self.driver.quit()


def main():
    while True:
        try:
            n = int(input("How many times do you want to fill the form? "))
            if n >= 1:
                break
            print("Enter a number greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

    while True:
        headless_input = input("Run in headless mode? (y/n): ").strip().lower()
        if headless_input in ['y', 'yes']:
            headless = True
            break
        elif headless_input in ['n', 'no']:
            headless = False
            break
        print("Please enter 'y' or 'n'.")

    filler = FormFiller2(headless=headless)
    success = 0
    failed = 0

    try:
        for i in range(1, n + 1):
            logger.info(f"Submission {i} of {n}")
            try:
                filler.fill_once()
                success += 1
                if i < n:
                    delay = random.uniform(2, 6)
                    logger.info(f"  Waiting {delay:.1f}s before next submission...")
                    time.sleep(delay)
            except Exception as e:
                failed += 1
                logger.error(f"Submission {i} failed: {e}")
                time.sleep(0.5)
    finally:
        filler.close()

    print(f"\nDone! Successful: {success}   Failed: {failed}")


if __name__ == "__main__":
    main()
