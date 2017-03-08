### !!! DANGER !!! DANGER !!! DANGER !!!

If you clone this and run it you may be sending to the entire list. Please read instructions below carefully before operating scripts.

# RG Newsletters

### Intro notes

* Before you begin, you might want to take a look at how the basic.py script works. You may also need to check out our fork of the [MailChimp API v3 repo](https://github.com/registerguard/APIv3-examples) that has some additional documentation.

* This repo contains the scripts used to generate, scrape and send MailChimp campaigns via the MailChimp API v3. These scripts have nothing to do with the design or content of the newsletters. Those templates can be edited at /rg/pages/newsletters/news.csp || football.csp || etc.

* Additional RG-specific notes can be found in [tracker#617](https://github.com/registerguard/tracker/issues/617) (private).

* The only requirement for this is requests 2.11. You can install that via `pip install requests` or `pip install -r requirements.txt`. Please note: I have a virtualenv set up on my local machine and on the server called "mailchimp". If you do this, you can also use that virtualenv for work with our fork of the [MailChimp API v3 repo](https://github.com/registerguard/APIv3-examples).

* **Before beginning you will need to add a file called APIKEY in the root that contains our MailChimp APIKEY. This file is excluded to make this repo public. The file should be one line only and named APIKEY. API keys can be found on the [MailChimp site](https://us2.admin.mailchimp.com/account/api/).**

### Getting started from scratch

Clone the repo, `mkvirtualenv mailchimp`, `pip install -r requirements.txt`.

**Depending on what file you want to edit, you'll want to comment out the last line in that file.** This line is responsible for sending the campaign to our hundreds of subscribers. Later on, you may or may not want to do this but it is **really** easy to accidentally send out a campaign during testing so it's good to double check this before running the script.

*You do not want to send out a blast to all subscribers during dev work.* Down below there are some [other ways to test send the campaign](#user-content-testing-sendemail).

Now, go into the config.py and check your APIKEY path (it's on two lines). When the cron runs on the server, it needs an absolute path but during testing that absolute path is incorrect so it needs to be commented out and replaced with a relative path. This could be set by some sort of dev bool conditional but I like the added safety of not being able to send if you don't know what you're doing. It's an added reminder to comment out `sendEmail()`.

Now, you can go in and make whatever changes are necessary.

...

When you're ready to test, go into the test function and add your email where mine is. Then go down to the bottom and uncomment the testEmail function line and *make sure that the sendEmail function is still commented out*. Now you can run the script (ie: `python rg.py`) and it should say "TEST SENT!!!". This test email will only be sent to those included in the script. This is the same on both scripts.

Once you've made the correct changes and you're ready to push back up there are two things to change.

1. Change the APIKEY path back for the server
2. Comment out the `testEmail()` function and uncomment the `sendEmail()` function

Add, commit and push your changes.

SSH to newsoper@wave (only available inside building, see [here](https://github.com/registerguard/tracker/wiki/Accessing-Wave%2C-the-cron-machine) for additional instructions on how to do this) and `cd Envs/mailchimp/newsletter`. Do a `git status` to double check that there are no changes on production. Do a `git remote update && git status` to do a sanity check on how many commits you're behind or to see if there are any potential conflicts. 

When you're ready do a `git pull`. Now production is up to date and the next time the cron runs your updated script will run.

### Adding a new newsletter to the mix

* Set up stuff locally
* Make new file for script, possibly made off of news.py
* Go into your MailChimp account and make a new list (be sure to set up the form styling [you can copy the styling of the other newsletters, they're all the same])
* While you're in there, be sure to create a new folder for all the emails to be collected in or else Melissa will get mad at you :)
* Now you need to get the IDs for that list and folder, the easiest way is to use `folders.py` and `lists.py` from the [MailChimp API v3 repo](https://github.com/registerguard/APIv3-examples)
* With `testEmail()` and `sendEmail()` commented out, try to create a new campaign in order to confirm that the list and folder are correct - YOU DO NOT WANT TO ACCIDENTALLY `sendEmail()` TO THE WRONG LIST.
* Try to send a `testEmail()`
* If you are the only one in the new list, try `sendEmail()`
* Change the APIKEY path to what's needed on wave
* Add, commit, push changes
* Pull changes on [wave](https://github.com/registerguard/tracker/wiki/Accessing-Wave%2C-the-cron-machine)
* Set up cron on wave (make sure config file set up correctly and that the `sendEmail()` is ready to rock and roll)

### Misc.

#### The cron

The [wave](https://github.com/registerguard/tracker/wiki/Accessing-Wave%2C-the-cron-machine) machine datetime is about five minutes early, meaning that I schedule the crons to go out five minutes before we want them. The Duck News Digest is set for `55 10 * * * ...` and the RG Daily Digest is set for `55 4 * * * ...`.

Absolute paths to the virtualenv python and the script are necessary. Any errors will be emailed to John and I via the MAILTO functionality. I previously had them writing out to a log file via:

```
55	10	*	*	*	/home/newsoper/Envs/mailchimp/bin/python2.7  home/newsoper/Envs/mailchimp/newsletter/duck.py > /home/newsoper/Envs/mailchimp/newsletter/logs/duck.log 2>&1
```

#### Testing `sendEmail()`

It may seem difficult to test the `sendEmail()` function because you don't want to send to everyone in the list, but you can do this by targeting a "test" list and specify that the campaign should only be sent to emails containing "rob.denton". This is very similar to how we originally wanted to target campaigns via interest groups within lists. We no longer do this but the logic is good to remember. It can also be found by setting up logic from the MailChimp UI and doing a read on the the API on the campaign ID.

```python
'segment_opts': { # This stuff only for testing
    'conditions': [{
        ### Send to Rob
        'field': 'EMAIL',
        'condition_type': 'EmailAddress',
        'value': 'rob.denton',
        'op': 'contains'
        ###################################
        ### Send to Test group (~6 people out of 13 in list)
        #'field': 'interests-3fcd22fb3e',
        #'condition_type': 'Interests',
        #'value': ['a51e8d83ce'],
        #'op': 'interestcontains'
    }],
    'match': 'any'
},
### Test list
'list_id': '824c7efd1d'
```

Of course, you can also send test emails to the emails designated in the script.

```python
# Vars for test email
test_emails = ['robdentonrg@gmail.com']

#Send test (Normally commented out)
sendTest(id, test_emails)
```

### Helpful links and hints

* [Mailchimp documentation](http://developer.mailchimp.com/documentation/mailchimp/reference/overview/)
* You can find the campaign ID as the c value in the unsubscribe or preferences button on the bottom of the email, from that you can find the list/group/interest IDs from a get() on the campaign information. Look for the `recipients` data. (Pro tip: Use an online JSON validator to format the data and make it readable.)
* I used [merge tags](http://kb.mailchimp.com/merge-tags/all-the-merge-tags-cheat-sheet) as much as I could but had to use the system date for the title, can't remember why at the moment.
* "inline css" is helpful because some email clients won't read head style tags (ahem, Google).

## Future Rob problems

* Find a better way to organize all the newsletter scripts into a folder so they don't clutter the root

