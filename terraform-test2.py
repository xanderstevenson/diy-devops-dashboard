import requests
import json
from decouple import config

TOKEN = config("TERRAFORM_TOKEN")
ORG = config("TERRAFORM_ORG")
# http://man.hubwiz.com/docset/Terraform.docset/Contents/Resources/Documents/docs/enterprise/api/workspaces.html

## LIST ALL
print("List all the TFC ORGs dynamically...")
# TOKEN = ''
url = "https://app.terraform.io/api/v2/organizations/"
headers = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/vnd.api+json",
}
TFCListresponse = requests.request("GET", url, headers=headers)
if TFCListresponse.status_code == 200:
    print("Got read response successfully..")
    print(TFCListresponse.content)

    my_orgs = json.loads(TFCListresponse.content.decode("utf-8"))
    terraform_id = my_orgs["data"][0]["id"]
    return terraform_id

else:
    print(TFCListresponse.content)
    print("Did not get the required response")
