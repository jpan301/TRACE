# source: DjangoSafe / django/contrib/admin/tests.py
# function: _assertOptionsValues

class AdminSeleniumTestCase:
    def _assertOptionsValues(self, options_selector, values):
        from selenium.webdriver.common.by import By

        if values:
            options = self.selenium.find_elements(By.CSS_SELECTOR, options_selector)
            actual_values = []
            for option in options:
                actual_values.append(option.get_attribute("value"))
            self.assertEqual(values, actual_values)
        else:
            # Prevent the `find_elements(By.CSS_SELECTOR, …)` call from
            # blocking if the selector doesn't match any options as we expect
            # it to be the case.
            with self.disable_implicit_wait():
                self.wait_until(
                    lambda driver: not driver.find_elements(
                        By.CSS_SELECTOR, options_selector
                    )
                )