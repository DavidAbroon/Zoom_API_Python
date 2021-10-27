import requests
import json
import csv

#Authorization details
jwt_token= ''
headers = {
    "Authorization": "Bearer " + jwt_token,
    "Content-Type": "application/json"
}

def getRooms():

    uri = "https://api.zoom.us/v2/rooms/zrlist"
    payload = {
        "method": "list",
        "params": {
            #Zoom Room Name starts with:
            "zr_name": "Parramatta.C 2"
        }
    }
    with open('get_rooms_response.csv', 'w', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        response = requests.request('POST', uri, headers=headers, json=payload)
        json_data = json.loads(response.text)
        room_information = json_data['result']['data']
        writer.writerow(['Room Name', 'Room ID'])
        #Store Zoom Room name & ID in CSV
        for x in room_information:
            room_name = x.get('zr_name')
            room_id = x.get('zr_id')
            writer.writerow([room_name, room_id])
            

def startMeeting():
    
    with open('get_rooms_response.csv', 'r', encoding='UTF8', newline='') as csvfile:
        #Read Room CSV file and store Zoom Room IDs & Name in lists
        room_id_list = []
        room_name_list = []
        for row in csv.reader(csvfile):
            room_name_list.append(row[0]) 
            room_id_list.append(row[1])

        #Removes first item in the list (column header)
        room_name_list = room_name_list[1:]
        room_id_list = room_id_list[1:]

    payload = {
        "method": "join",
        "params": {
            "meeting_number": 88549513264,
            "password": "5111",
            "force_accept": "false"
        }
    }
    
    #Read Zoom Room IDs in above created list and send POST request to start meeting
    for room in range(len(room_id_list)):
        room_id = room_id_list[room]
        room_name = room_name_list[room]
        uri = f'https://api.zoom.us/v2/rooms/{room_id}/meetings'
        
        response = requests.request('POST', uri, headers=headers, json=payload)
        print("Joining: " + room_name)
        print(response)

def main():
    while True:
        selection = input("Enter '1' to get Zoom Rooms or '2' to join rooms in get_rooms_response.csv to meeting: ")
        if selection == '1':
            getRooms()
        elif selection =='2':
            startMeeting()
        else:
            print("Invalid selection. Press Ctrl + C to exit")

if __name__ == "__main__":
    main()
    

    
