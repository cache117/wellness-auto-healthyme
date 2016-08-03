# wellness-auto-healthyme
Automatically enter your HealthyME Lifestyle Tracker information into the http://wellness.byu.edu/ site so you don't have to enter it manually.  There are many ways to track your activities that are automated.  Why not automate the reporting of that activity info HealthyME?

HealthyME is a service to BYU employees and it is accessible from the http://wellness.byu.edu/ site.  Lifestyle Tracker is one of the sections of HealthyME where BYU employees enter their daily health-related activities as one of a few ways to gain points.  If you gains enough points in a period you win prizes.

This codebase uses python, docker and selenium webdriver.

Here's how to use it.
- clone the repo on a machine that can run docker.
- create a file called `~/.byu/netid.ini`[^fn-config-path] with the [following format](#netidini-format).  Note, the file is not part of the repo to lessen the possibility that it is checked into github.  
- create a file called `~/.byu/wellness.ini`[^fn-config-path] with the [following format](#wellnessini-format).  
- build the docker container with `./build.sh`
- create an `import.json` file in the [following format](#importjson-file-format).  The `dailygoals2json.py` script is an example that I use to create an `import.json` file from a google spreadsheet where I keep this data. Also, see [this repo](https://github.com/cache117/fitbit-csv-data) to turn Fitbit data into an `import.json` file.
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
      "steps": "5000",
      "water_5_or_more_cups": true, 
      "fruit_veg_4_or_more_servings": true, 
      "physical_activity_description": "walking"
    }
  ]
}
```

## netid.ini format
```
[netid]
username = 
password = 
```

## wellness.ini format
```
[wellness]
# a number between 1 and 6 inclusive
current_challenge = 
```


# current limitations (PRs welcome!)
- Because of the nature of the Wellness site, only steps *or* active minutes can be recorded. Not both. However, the one that gives you the most points (up to 4) will be chosen, with preference given to steps.

[^fn-config-path]: In Windows, ~ likely refers to `C:\Users\your-user\`. So, you would have`C:\Users\your-user\.byu\netid.ini`. Additionally, to create a directory starting with `.`, you name it like this `.byu.`
