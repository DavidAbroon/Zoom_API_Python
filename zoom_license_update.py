import time
import aiohttp
import asyncio
import json
import csv

start_time = time.time()

async def main():

    jwt_token = ''

    user_list = []
    with open('users.csv', newline='') as f:
        for row in csv.reader(f):
            user_list.append(row[0])

    #Type:1 = 'Basic', Type:2 = 'Licensed', Type:3 = 'On-Prem'
    payload = {
    "type":"1"
    }
    headers = {
    "Authorization":"Bearer " + jwt_token,
    "User-Agent":"Zoom-Jwt-Request",
    "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        with open('AsyncResults.csv', 'w', encoding='UTF8', newline='') as csvfile:
            #initialize 'writer' variable to work with CSV file
            writer = csv.writer(csvfile)
            #Create column headers
            writer.writerow(['User Email', 'Response code', 'Response text'])
            user_counter = 0

            for user in range(len(user_list)):
                user_to_update = user_list[user]
                print("User being updated: " + user_to_update)
                uri = f'https://api.zoom.us/v2/users/{user_to_update}'
                #Create API request to server
                async with session.patch(url=uri, data=json.dumps(payload)) as resp:
                    
                    response_string = ("Success: " + str(resp.status))
                    if (resp.status != 204):
                        response_string = ("Error: " + await resp.text())
                        print(response_string)
                    else:
                        print(response_string)

                    writer.writerow([user_to_update, str(resp.status), str(response_string)])

                    #Counter to display in shell for every 20 Users completed
                    if (user % 20) == 0:
                        print("User update count: %d" % (user))

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    seconds_to_complete = (time.time() - start_time)
    print("Seconds to complete:", seconds_to_complete)
    minutes_to_complete = print("Minutes to complete: ", seconds_to_complete/60)
