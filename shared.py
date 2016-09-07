import requests, json
from config import MailChimpConfig

config = MailChimpConfig()

def createCampaign(list, subject, title, folder):
    path = "campaigns"
    endpoint = config.api_root + path
    
    meta = {}
    
    meta['recipients'] = {
#       'segment_opts': { # This stuff only for testing
#           'conditions': [{
#               ### Send to Rob
#               'field': 'EMAIL',
#               'condition_type': 'EmailAddress',
#               'value': 'rob.denton',
#               'op': 'contains'
#               ###################################
#               ### Send to Test group
#               #'field': 'interests-3fcd22fb3e',
#               #'condition_type': 'Interests',
#               #'value': ['a51e8d83ce'],
#               #'op': 'interestcontains'
#           }],
#           'match': 'any'
#       },
#       ### Test list
#       'list_id': '824c7efd1d'
        'list_id': list
    }
    
    meta['settings'] = {
        'subject_line': subject,
        'from_name': 'The Register-Guard',
        'title': title,
        'inline_css': True,
        'fb_comments': False,
        'auto_footer': False,
        'athenticate': True,
        'to_name': '*|FNAME|* *|LNAME|*',
        'folder_id': folder,
        'reply_to': 'promotions@registerguard.com',
        'auto_tweet': False,
    }
    
    meta['type'] = 'regular'
    
    #print meta
    
    payload = json.dumps(meta)
    
    #print payload
    
    response = requests.post(endpoint, auth=('apikey', config.apikey), data=payload)
    
    #print response.json()
    
    try:
        response.raise_for_status()
        body = response.json()
        id = body['id']
        return id
    except requests.exceptions.HTTPError as err:
        print '\n\n\nError: %s' % err

def setContent(id, url):
    content = "campaigns/{0}/content".format(id)
    endpoint = config.api_root + content
    
    payload = json.dumps({"url": url})
    
    response = requests.put(endpoint, auth=('apikey', config.apikey), data=payload)
    
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print "\n\n\nError: %s" % err
        print response.json()

def sendTest(id, test_emails):
    test = "campaigns/{0}/actions/test".format(id)
    endpoint = config.api_root + test
    
    payload = json.dumps({'test_emails': test_emails,'send_type':'html'})
    
    #print  "\nPayload: " + payload
    
    response = requests.post(endpoint, auth=('apikey', config.apikey), data=payload)
    #print response.json()
    
    #print "\nURL: " + response.url + "\n\n"
    
    try:
        response.raise_for_status()
        print "\n\nTEST SENT!!!\n\n"
    except requests.exceptions.HTTPError as err:
        print "\n\n\nError: %s" % err
        
    

def sendEmail(id):
    email = "campaigns/{0}/actions/send".format(id)
    endpoint = config.api_root + email
    
    response = requests.post(endpoint, auth=('apikey', config.apikey))
    
    #print "\nURL: " + response.url + "\n\n"
    
    try:
        response.raise_for_status()
        #print "\n\nCAMPAIGN SENT!!!\n\n"
    except requests.exceptions.HTTPError as err:
        print "\n\n\nError: %s" % err
        print response.json()
        