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
#list = '09a7fee6c3' # RG Daily Digest list --- OLD LIST
list = 'ebb49abb5c' # RG Daily Digest NEW list
subject = "RG Daily Digest: *|DATE:l, F j, Y|*"
title = "RG Daily Digest: {0}".format(date)
folder = '9f4465721a'

# Create campaign and get ID
id = createCampaign(list, subject, title, folder)
#id = "ea9d94e671" # For testing (use last created campaign ID)
#print id

# Vars for setting content
url = 'http://registerguard.com/csp/cms/rg/pages/newsletters/news.csp'

# Set content
setContent(id, url)

# Vars for test email
test_emails = ['robdentonrg@gmail.com']

#Send test (Normally commented out)
#sendTest(id, test_emails)

# Call method
sendEmail(id)
