import requests
import base64 
import json

def get_token():
    #AuthB64 = b64encode(bytes(Client ID:Client Secret))
    AuthB64 = base64.b64encode(b'boJK9xAlR1iI46VnO5FHRQ:mC82YBkj0ToLts49i2Lro05hpsWp71om').decode('utf-8')
    authorizationcode = "rbFDqEZFI5_jCvAaNG6RNmp20L4iF6MSg"
    url = "https://zoom.us/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": authorizationcode,
        "redirect_uri": "http://localhost:5000/MyApp"
    }
    headers = {
        "Authorization": "Basic " + AuthB64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    #Create POST Request to server for access_token
    response = requests.post(url, headers=headers, data=payload)
    print("Response code is: " + str(response.status_code))

    #If request is successful, assign access_token to variable and print
    if response.status_code in [200]:
        tok_dict = json.loads(response.text)
        access_token = tok_dict["access_token"]
        print("Access token obtained: " + str(access_token))
        return access_token
    else:
        print(response.text)
        exit()

def update_email(access_token):
  #Open both text files with old & new email addr and create variable as a list
    with open('oldEmail.txt') as f:
        old_lines = f.read().splitlines()
    with open('newEmail.txt') as f:
        new_lines = f.read().splitlines()

    #Clear APIResults.txt file before loop starts
    with open('APIResults.txt', 'r+') as file:
        file.truncate(0)

    with open('APIResults.txt', 'w') as file:
    #Loop thru each item and assign it to a new variable which is used in the PUT request
        for x in range(len(old_lines)):
            old_email_address = old_lines[x]
            new_email_address = new_lines[x]
            url = f"https://api.zoom.us/v2/users/{old_email_address}/email"
            payload = {
            "email":new_email_address
        }
            headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
            }
            response = requests.request('PUT', url, headers=headers, json=payload)
            print(response)
            print(response.text)

            #Write HTTP Response to APIResults.txt file
            file.write(str(response))
            file.write(str(response.text))
            file.write("\n")
            file.write("\n")

if __name__ == "__main__":
    loop = True
    while loop:
        print("Enter '1' to get access_token: ")
        print("Enter '2' to start the Zoom Update Email API: ")
        choice = input("Please make a choice: ")      

        if choice == "1":
            access_token = get_token()
        elif choice == "2":
            update_email(access_token)
        else:
            print("Please choose '1' or '2'")


    

    