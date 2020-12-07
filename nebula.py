# coding=utf-8
import time
import webbrowser
import selenium
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import glob
import argparse
import sys


class Nebula:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        # No way to test otherwise.
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=self.options)

        self.parser = argparse.ArgumentParser(description='Nebula')
        self.parser.add_argument('-i', '--inputfile', help="Specify a text file with line-separated domains")
        self.parser.add_argument('-r', '--report', action="store_true", help="Regenerate the report instead of running another long-winded scan.")

        self.args = self.parser.parse_args()
        self.input_file = ""

    def run(self):
        if self.args.report:
            print("Regenerating report...")
            self.create_html_document()
            print("Done")

            sys.exit(0)

        if self.args.inputfile:
            self.input_file = self.args.inputfile
        else:
            print("You need to specify an input file.")
            sys.exit(0)

        with open(self.input_file, "r") as f:
            file = f.read().splitlines()

            current_site = 0

            for site in file:
                port = ""
                website = ""
                try:
                    self.driver.set_window_size(1280, 1080)
                    self.driver.get(site)

                    if site.count(":") == 2:
                        port = site.split("/")[2].split(":")[1]
                    if "https://" in site:
                        website = site.split("/")[2]
                    if "http://" in site:
                        website = site.split("/")[2]

                    if port == "":
                        if "https://" in site:
                            port = 443
                        if "http://" in site:
                            port = 80

                    body = self.driver.find_element_by_tag_name("body")
                    body.screenshot(f"shots/{website}_{port}.png")

                    print(f"Finished getting screenshot for {site} (#{current_site})")

                except urllib3.exceptions.MaxRetryError:
                    print(f"[???] Couldn't connect to {site}")
                except urllib3.exceptions.NewConnectionError:
                    print(f"[???] Couldn't connect to {site}")
                except ConnectionRefusedError:
                    print(f"[???] Couldn't connect to {site}")
                except selenium.common.exceptions.WebDriverException:
                    print(f"[???] Couldn't connect to {site} because of SSL Protocol Problems")

                current_site += 1
        self.driver.quit()
        self.create_html_document()

    def create_html_document(self):
        start = self.get_html_as_string("template_start.html")
        end = self.get_html_as_string("template_end.html")
        img = self.get_html_as_string("template_image.html")

        html_string = start

        screenshot_files = glob.glob("shots/*.png")

        for file in screenshot_files:
            port = file.split("_")[1].split(".")[0]
            site = file.split("_")[0]
            html_string += img.replace("!", file).replace("@", self.get_port_desc(port)).replace("*", port).replace("$", site.replace("shots/", ""))

        html_string += end

        with open("report.html", "w") as w:
            w.write(html_string)
        self.open_site("report.html")

    @staticmethod
    def get_html_as_string(file):
        with open(file, "r") as f:
            return f.read()

    @staticmethod
    def get_port_desc(port):
        if port == "80":
            return "http"
        if port == "443":
            return "https"
        else:
            return port

    @staticmethod
    def open_site(url):
        try:
            webbrowser.open(url)
        except Exception:
            print("Couldn't open a web browser. This script hates you. Contact author.")


if __name__ == "__main__":
    nebby = Nebula()
    nebby.run()
