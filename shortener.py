import requests
import time

# Authentication tokens
def authentication(user):
    if (not user):
        # Authentication tokens for the first 1000 URLs 
        access_token = ""

    else:
        # Authentication tokens for the remaining URLs (up to 1000)
        access_token = ""
 
    headers = {'Authorization': f"Bearer {access_token}",
                'Content-Type': 'application/json',
            }

    return headers

# Opens the file(assiming it's a Comma-Separated-Values file) and returns a list of IDs and a list of the long URls
def openFile(path):
    l = []
    ids = []
    lUrls = []
    with open(path, "r") as f:
        for i in f:
            l.append(i)
    f.close()
    
    for c in range(len(l)):
        s = l[c].split(",")
        ids.append(s[0])
        lUrls.append((s[1].split('\n'))[0])

    return ids, lUrls

#Writes the file with the new column
def writeFile(path, ids, longUrlsList, shortUrlsList):
    with open(path, "w") as f:
        for i in range(len(ids)):
            f.write(ids[i] + ',' + longUrlsList[i] + ',' + shortUrlsList[i] + '\n')
    f.close()

def shortenUrl(lUrl, headers):
    # Requests the Bitly shortener service, passing lUrl as the URL to be shortened.
    response = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"long_url": lUrl}, headers=headers)

    # if response is SUCCESS or CREATED, get the shortened URL
    if response.status_code == 200 or response.status_code == 201:
        link = response.json().get("link")

    #Otherwise, an error ocurred on the request and the output link is an error message.
    else:
        link = "AN_ERROR_OCURRED"

    return link

# ---> Use double '\'s on the path <---
# path to the file containing the URLs to be shortened
path = ""
idsList, longUrlsList = openFile(path)
failedUrlsIds = []
shortUrlsList = []
header = authentication(0)
for i in range(len(longUrlsList)):  
    if(i < 999): # The Bitly API (free version) has a limit of 1000 requests per user per month
        url = shortenUrl(longUrlsList[i], header)
        if url == "AN_ERROR_OCURRED":
            failedUrlsIds.append(idsList[i])
        shortUrlsList.append(url)
        time.sleep(0.7) # the Bitly API has a limit of 100 requests per minute
    else: # When the Bitly's month limit is reached, switches the authentication token
        header = authentication(1)
        url = shortenUrl(longUrlsList[i], header)
        if url == "AN_ERROR_OCURRED":
            failedUrlsIds.append(idsList[i])
        shortUrlsList.append(url)
        time.sleep(0.7) # the Bitly API has a limit of 100 requests per minute

writeFile(path, idsList, longUrlsList, shortUrlsList)

##############################OPTIONAL:
#Shows the IDs list of the failed cases.
# if len(failedUrlsIds) != 0:
#     for i in range(len(failedUrlsIds)):
#         print(failedUrlsIds[i])
    


