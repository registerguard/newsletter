## !!! DANGER !!! DANGER !!! DANGER !!!

If you clone this and run it you may be sending to the entire list. Please read instructions below carefully before operating scripts.

# RG Newsletters

### Intro

This repo contains the scripts used to generate, scrape and send MailChimp campaigns via the MailChimp API v3. These scripts have nothing to do with the design or content of the newsletters. Those templates can be edited at /rg/pages/newsletters/news.csp || football.csp. 

Additional notes can be found in tracker#617.

The only requirement for this is requests 2.11. You can install that via `pip install requests` or `pip install -r requirements.txt`. Please note: I have a virtualenv set up on my local machine and on the server called "mailchimp".

Before beginning you will need to add a file called APIKEY in the root that contains the MailChimp APIKEY. This is being kept secret just in case this repo was ever accidentally made public. This can be found [here](https://us2.admin.mailchimp.com/account/api/)

### Getting started

Clone the repo, `mkvirtualenv mailchimp`, `pip install -r requirements.txt`.

First things first, go into the config.py and check your APIKEY path (it's in two places). When the cron runs on the server, it needs an absolute path but during testing that absolute path is incorrect so it needs to be changed.

Second, go into duck.py and rg.py and make sure the very last line is commented out. This is the line that sends the campaign. Later on, you may or may not want to do this but it is **really** easy to accidentally send out a campaign during testing so it's good to double check this before running the script.

Now, you can go in and make whatever changes are necessary.

When you're ready to test, go into the test function and add your email where mine is. Then go down to the bottom and uncomment the testEmail function line and make sure that the sendEmail function **is** still commented out. Now you can run the script (ie: `python rg.py`) and it should say "TEST SENT!!!". This test email will only be sent to those included in the script. This is the same on both scripts.

Once you've made the correct changes and you're ready to push back up there are two things to change.

1. Change the APIKEY path back for the server
2. Comment out the testEmail function and uncomment the sendEmail function

Add, commit, push your changes. 

SSH to newsoper@wave and `cd Envs/mailchimp/newsletter`. Do a `git status` to double check that there are no changes on production. Do a `git remote update && git status` to do a sanity check on how many commits you're behind or to see if there are any potential conflicts. When you're ready do a `git pull`. Now production is up to date and the next time the cron runs your updated script will run. 

### Misc.

#### cron

The wave machine datetime is about five minutes early, meaning that I schedule the crons to go out five minutes before we want them. The Duck News Digest is set for `55 10 * * * ...` and the RG Daily Digest is set for `55 4 * * * ...`.

Absolute paths to the virtualenv python and the script are necessary. Any errors will be emailed to John and I via the MAILTO functionality. I previously had them writing out to a log file via:

```
55	10	*	*	*	/home/newsoper/Envs/mailchimp/bin/python2.7  home/newsoper/Envs/mailchimp/newsletter/duck.py > /home/newsoper/Envs/mailchimp/newsletter/logs/duck.log 2>&1
```

### Helpful links and hints

* [Mailchimp documentation](http://developer.mailchimp.com/documentation/mailchimp/reference/overview/)
* You can find the campaign ID as the c value in the unsubscribe or preferences button on the bottom of the email, from that you can find the list/group/interest IDs from a get() on the campaign information. Look for the `recipients` data. (Pro tip: Use an online JSON validator to format the data and make it readable.)
* I used [merge tags](http://kb.mailchimp.com/merge-tags/all-the-merge-tags-cheat-sheet) as much as I could but had to use the system date for the title, can't remember why at the moment.
* "inline css" is helpful because some email clients won't read head style tags (ahem, Google).


### To-do

* [ ] Modify scripts to that they're pulling in communal functions, each one of those could be stripped off into a class.