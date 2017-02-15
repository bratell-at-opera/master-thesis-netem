#!/usr/bin/env python3

import threading
import time

# Description: Loads a web page with a given webdriver


class PageLoader(threading.Thread):

    def __init__(self, driver, url):
        self.url = url
        self.done = threading.Event()
        self.done.clear()
        self.driver = driver

        self.results = {}
        self.results["load_succeeded"] = False

        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        try:
            old_page = self.driver.find_element_by_tag_name("html")
            # self.driver.get(self.url)
            # Dev tools only open in new tabs. Create a new tab (ugly but works).
            # Dev tools are needed to capture HAR
            main_window = self.driver.current_window_handle
            self.driver.execute_script(
                "window.open(\'" +
                self.url +
                "\');"
            )
            switched_tab = False
            for tab in self.driver.window_handles:
                if tab != main_window:
                    switched_tab = True
                    self.driver.switch_to_window(tab)
                    time.sleep(1)
                    break
            if not switched_tab:
                print("ERROR: Failed to switch to tab with devtools!")
                sys.exit(100)
            # Wait for page load, this is workaround for
            # issue mentioned in init of browser-runner
            new_page = old_page
            while new_page.id == old_page.id:
                new_page = self.driver.find_element_by_tag_name("html")

            # Saving some important statistics for use.
            # See
            # http://www.sitepoint.com/profiling-page-loads-with-the-navigation-timing-api/

            # Before connection starts
            self.results["connect_start"] = self.driver.execute_script(
                "return window.performance.timing.connectStart")
            # TLS handshake time
            self.results["secure_conn_start"] = self.driver.execute_script(
                "return window.performance.timing.secureConnectionStart")
            # Time just after browser receives first byte of response
            self.results["response_start"] = self.driver.execute_script(
                "return window.performance.timing.responseStart")
            # Time just after browser receives last byte of response
            self.results["response_end"] = self.driver.execute_script(
                "return window.performance.timing.responseEnd")
            # Time just before dom is set to complete
            self.results["dom_complete"] = self.driver.execute_script(
                "return window.performance.timing.domComplete")
            # End of page load
            self.results["load_event_end"] = self.driver.execute_script(
                "return window.performance.timing.loadEventEnd")

            self.results["har"] = self.driver.execute_script(
                "chrome.devtools.network.getHAR()")

            # And we're done!
            if "this site can’t be reached" in self.driver.page_source.lower():
                self.results["load_succeeded"] = False
            else:
                self.results["load_succeeded"] = True
        except Exception as e:
            self.results["load_succeeded"] = False
            print("Got exception when fetching " + self.url)
            print(type(e).__name__ + str(e))
        self.done.set()

    def get_result(self):
        return self.results
