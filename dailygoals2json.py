import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import datetime

def go(startdate, enddate):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('daily_goals.json', ['https://spreadsheets.google.com/feeds'])
    gc = gspread.authorize(credentials)
    wks = gc.open("Daily Goals").worksheet("Sheet1")
    rows = wks.get_all_values()

    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')

    results = {}
    results['rows'] = []

    def str2num(val):
        if not val:
            return 0
        else:
            return float(val)

    for row in rows:
        date_str, wateroz, vitamins, scripture_study, exercised, pullups, divebombpushups, calories, sevenminuteworkout, weight, sat_fat_grams, sol_fiber_grams, hours_slept, servings_fruit_veg = row
        try:
            dateobj = datetime.datetime.strptime(date_str.split(' ')[0], '%Y-%m-%d')
        except ValueError:
            continue
        dateobj = dateobj - datetime.timedelta(days=1)
        if (startdate <= dateobj <= enddate) and (dateobj.weekday() != 6):
            results['rows'].append({'date_str': dateobj.date().strftime('%Y-%m-%d'),
                                    'physical_activity_description': 'walking',
                                    'activity_minutes': exercised,
                                    'water_5_or_more_cups': (str2num(wateroz)/8) >= 5,
                                    'fruit_veg_4_or_more_servings': str2num(servings_fruit_veg) >= 4,
                                    'sleep_7_or_more_hours': str2num(hours_slept) >= 7})
    print(json.dumps(results))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('startdate')
    parser.add_argument('enddate')
    args = parser.parse_args()
    go(args.startdate, args.enddate)
