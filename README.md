# wellness-auto-healthyme
Automatically enter your HealthyME Lifestyle Tracker information into the http://wellness.byu.edu/ site so you don't have to enter it manually.  There are many ways to track your activities that are automated.  Why not automate the reporting of that activity info HealthyME?

HealthyME is a service to BYU employees and it is accessible from the http://wellness.byu.edu/ site.  Lifestyle Tracker is one of the sections of HealthyME where BYU employees enter their daily health-related activities as one of a few ways to gain points.  If you gains enough points in a period you win prizes.

This codebase uses python, docker and selenium webdriver.

Here's how to use it.
- clone the repo
- run `cp config-example.py config.py` and edit `config.py` with your information.
- build the docker container with `./build.sh`
- create an `import.json` file in the [following format](#importjson-file-format).  The `dailygoals2json.py` script is an example that I use to create an `import.json` file from a google spreadsheet where I keep this data.
- run the selenium script that will import the data in `import.json` into the wellness.byu.edu site like so, `./run-chrome.sh`
- enjoy all the time you saved!

## import.json file format
```
{
  "rows": [
    {
      "date_str": "2016-07-01", 
      "sleep_7_or_more_hours": true, 
      "activity_minutes": "0", 
      "water_5_or_more_cups": true, 
      "fruit_veg_3_or_more_servings": true, 
      "physical_activity_description": "walking"
    }
  ]
}
```

# current limitations (PRs welcome!)
- only supports minutes exercised not number of steps
