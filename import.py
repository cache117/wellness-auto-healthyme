#!/usr/bin/env python
# Copyright 2016 Brigham Young University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
import os
import datetime
import time
import json
import config

time.sleep(1)

def date_is_sunday(date_str):
    dateobj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return dateobj.weekday() == 6 # https://docs.python.org/3/library/datetime.html#datetime.date.weekday

def assert_valid_rows(rows, start_date, end_date):
    for row in rows:
        if date_is_sunday(row['date_str']):
            print(row)
            raise Exception("This row is invalid.  The date is a sunday which is not allowed by the site.")
        if not (start_date <= datetime.datetime.strptime(row['date_str'], '%Y-%m-%d') <= end_date):
            print(row)
            raise Exception("This row is invalid.  The date ({}) is not inside within the current challenge dates ({} - {})".format(row['date_str'], start_date, end_date))

def get_obj_from_json_filename(json_filename):
    reader = open(json_filename, 'r')
    json_str = reader.read()
    reader.close()
    return json.loads(json_str)['rows']

def get_dates_for_challenge(driver):
    seconds_waited = 0
    while driver.current_url != 'http://wellness.byu.edu/healthyME/':
        time.sleep(1)
        seconds_waited += 1
        print("waited {} seconds to redirect after cas authn".format(seconds_waited))
        if seconds_waited > 60:
            raise Exception("Login problem > 60 seconds after login")
    if config.current_challenge == 1:
        element = driver.find_element_by_css_selector('#challenges > tbody > tr:nth-child(1) > td:nth-child(1) > p:nth-child(3)')
    elif config.current_challenge == 2:
        element = driver.find_element_by_css_selector('#challenges > tbody > tr:nth-child(1) > td:nth-child(2) > p:nth-child(3)')
    elif config.current_challenge == 3:
        element = driver.find_element_by_css_selector('#challenges > tbody > tr:nth-child(1) > td:nth-child(3) > p:nth-child(3)')
    elif config.current_challenge == 4:
        element = driver.find_element_by_css_selector('#challenges > tbody > tr:nth-child(2) > td:nth-child(1) > p:nth-child(3)')
    elif config.current_challenge == 5:
        element = driver.find_element_by_css_selector('#challenges > tbody > tr:nth-child(2) > td:nth-child(2) > p:nth-child(3)')
    elif config.current_challenge == 6:
        element = driver.find_element_by_css_selector('#challenges > tbody > tr:nth-child(2) > td:nth-child(3) > p:nth-child(3)')
    else:
        raise Exception("Invalid value ({}) for config.current_challenge.  It must be an integer between 1 and 6 inclusive.".format(config.current_challenge))
    
    if element.text.startswith("Begins in"):
        raise Exception("Invalid value ({}) for config.current_challenge.  The specified challenge hasn't started yet.  It {}.".format(config.current_challenge, element.text.lower()))
    else:
        # 'From July 1st\nto August 31th'
        date_pair_str = element.text
        date_pair = date_pair_str.replace('From ', '').split("\nto ")
        date_pair = [item[:-2] for item in date_pair]
        date_pair = [item + ' ' + str(datetime.datetime.today().year) for item in date_pair]
        date_pair = [datetime.datetime.strptime(item, '%B %d %Y') for item in date_pair]
    
    return date_pair

def get_current_points(driver):
    driver.get('http://wellness.byu.edu/healthyME/dashboard/challenge=' + str(config.current_challenge))
    element = driver.find_element_by_css_selector('#divProgress > input')
    return int(element.get_attribute('value'))
                
def run(json_filename):
    url = os.environ['SELENIUM_HUB_PORT_4444_TCP'].replace('tcp', 'http')
    driver = webdriver.Remote(url + '/wd/hub', webdriver.DesiredCapabilities.CHROME.copy())
    driver.implicitly_wait(30)

    # login
    driver.get("http://wellness.byu.edu/healthyME/")
    driver.find_element_by_id("netid").clear()
    driver.find_element_by_id("netid").send_keys(config.net_id)
    driver.find_element_by_id("password").clear()
    driver.find_element_by_id("password").send_keys(config.net_id_password)
    driver.find_element_by_css_selector("input.submit").click()

    # get and validate rows
    start_date, end_date = get_dates_for_challenge(driver)
    rows = get_obj_from_json_filename(json_filename)
    assert_valid_rows(rows, start_date, end_date)

    # open the import record file
    if not os.path.exists('.import_record_file'):
        open('.import_record_file', 'w').close()    
    import_records = [item.strip() for item in open('.import_record_file', 'r').readlines()]
    import_record_fileobj = open('.import_record_file', 'a')

    # enter rows in site
    for row in rows:
        if row['date_str'] in import_records:
            print('{} has already been imported.  It\'s in .import_record_file.  Skipping it.'.format(row['date_str']))
            continue
        driver.get("http://wellness.byu.edu/healthyME/index.php?page=tracker&date={}&challenge={}".format(row['date_str'], config.current_challenge))
        driver.find_element_by_id("activityDescription").clear()
        driver.find_element_by_id("activityDescription").send_keys(row['physical_activity_description'])
        driver.find_element_by_id("activityDuration").clear()
        driver.find_element_by_id("trackingTypeMinutes").click()
        driver.find_element_by_id("activityDuration").send_keys(row['activity_minutes'])
        # the following checkboxes are not idempotent
        if row['water_5_or_more_cups']:
            driver.find_element_by_id("dc_1").click() # 5 or more cups of water
        if row['fruit_veg_4_or_more_servings']:
            driver.find_element_by_id("dc_2").click() # 4 or more servings of fruit and/or veggies
        if row['sleep_7_or_more_hours']:
            driver.find_element_by_id("dc_3").click() # 7 or more hours of sleep
        driver.find_element_by_css_selector("button.greenButton").click() # Save Changes button
        print("{} imported".format(row['date_str']))
        import_record_fileobj.write(row['date_str'] + "\n")
        import_record_fileobj.flush()
        time.sleep(1)
        if EC.alert_is_present():
            alert = driver.switch_to_alert()
            alert.accept()

    import_record_fileobj.close()

    # show current points and percentage
    points = get_current_points(driver)
    print("{} of 150 points earned so far.  Challenge {} is {}% completed".format(points, config.current_challenge, round((points/150.0)*100, 0)))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Wellness.byu.edu activity tracker importer')
    parser.add_argument('jsonfilename', help='json input filename')
    args = parser.parse_args()
    if not os.path.exists(args.jsonfilename):
        parser.error("The jsonfilename passed in ({}) doesn't exist".format(args.jsonfilename))
    else:
        run(args.jsonfilename)

