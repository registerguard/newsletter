#!/home/newsoper/Envs/mailchimp/bin/python2.7
#
#            !!! DANGER !!!
#            !!! DANGER !!!
#            !!! DANGER !!!
#
# This script will send an email to all recipients of campaign
#
# Comment out sendEmail() and uncomment sendTest() to test
#

import datetime
from shared import createCampaign, setContent, sendTest, sendEmail

today = datetime.date.today()
date = "{:%x}".format(today)

# Vars for campaign creation
#list = "" # Safety
list = 'da06b9d3a2' # Duck News Daily list
subject = "Duck News Daily: *|DATE:l, F j, Y|*"
title = "Duck News Daily: {0}".format(date)
folder = '8a260761a0'

# Create campaign and get ID
id = createCampaign(list, subject, title, folder)
#id = "ea9d94e671" # For testing (use last created campaign ID)
#print id

# Vars for setting content
url = 'http://registerguard.com/csp/cms/rg/pages/newsletters/football.csp'

# Set content
setContent(id, url)

# Vars for test email
test_emails = ['robdentonrg@gmail.com']

#Send test (Normally commented out)
#sendTest(id, test_emails)

# Call method
sendEmail(id)
