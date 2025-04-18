import time
from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
import os
import csv
from botasaurus.request import request,Request

dontaions_data = []
Urls = []
Status = []
Income = []
Ids = []
Report = []

os.makedirs("output",exist_ok=True)
os.makedirs("error_logs",exist_ok=True)   # use for logging

output_file="output/crawled_url.csv"

with open(output_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["HEADINGS"])

def write_data_in_csv(link):
    with open(output_file,mode="a",newline="",encoding="utf-8") as file:
        writer=csv.writer(file)
        writer.writerow([link])

@browser
def scrape_heading_task(driver: Driver, data):

    driver.get("https://register-of-charities.charitycommission.gov.uk/en/charity-search/-/results/page/1/delta/20")
    driver.prompt()
    while True:
        c_ids=driver.select_all("td[class='table-cell govuk-table__cell first']")
        data=driver.select_all("td[class='table-cell govuk-table__cell']")
        reporting=driver.select_all("td[class='table-cell govuk-table__cell last']")
        for i in range(len(data)):
            try:
                url = data[i + 0]
                link = url.select('a')
                Urls.append(link.get_attribute('href'))
                print(link.get_attribute('href'))
                status = data[i + 1].text
                print("Status", status)
                Status.append(status)
                income = data[i + 2].text
                print("Income", income)
                Income.append(income)
            except Exception as e:
                print("Error :",e)
        for i in range(len(c_ids)):
            Ids.append(c_ids[i].text)
            print("ID :",c_ids[i].text)
            Report.append(reporting[i].text)
            print("Report :",reporting[i].text)

        #try last li to perform pagination
        next_page = driver.select("a[class='lfr-portal-tooltip page-link']")

        if next_page:
            driver.click("a[class='lfr-portal-tooltip page-link']")
            time.sleep(5)
        else:
            break



    # print("ID ",Ids)
    # print("Reports ",Report)
    # print("URLS ",Urls)
    # print("Status ",Status)
    # print("Income ",Income)




@request
def who_why_what_where():
    pass

scrape_heading_task()

