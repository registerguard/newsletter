### See: http://developer.mailchimp.com/documentation/mailchimp/reference/overview/
import requests, json
from config import MailChimpConfig
config = MailChimpConfig()

### Change depending on what API content you're after
#path = "lists"
#path = "/campaigns/2ccdaab862" # Get campaign ID as c value of unsubscribe link
### Concatenate full API address
endpoint = config.api_root + path
#print endpoint

### Additional arguments can be constructed as meta...
#meta = {}
#meta['test'] = {'whatever'}
### ...and formatted as payload
#payload = json.dumps(meta)

### Change to request type, add payload if needed
response = requests.get(endpoint, auth=('apikey', config.apikey))
### Get response JSON
responsejson = response.json()
### Print out the response JSON
print json.dumps(responsejson, indent=4, separators=(',', ': '))
