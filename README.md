_This is a quick summary of the project. More details about the project and demonstration can be done with a meeting._

# Starting the Server
The python version used during development is 3.12.3 on Windows 10.

It is recommended to work inside a isolated virtual environment to maintain a cleaner setup and prevent conflicts.

After cloning the project and going into the project directory and use the [requirements.txt](requirements.txt) file to install all the packages used in the project using the command `pip install -r requirements.txt`.

The [.gitignore](.gitignore) file is simply used to ignore the sqlite database files when commiting changes to the repo.

To start the server, go into the [myproject](myproject/) directory and run the command `python manage.py runserver`. The available APIs will be discussed in the API section.

To run the automatic tests, run `python manage.py test`.

# Deliverables
## 1. Models
The models can be seen in [models.py](myproject/myapp/models.py) file and was made based on the given UI shown on the assesment file. The summary of the database schema is as such:

**Doctor**
- id: randomly generated UUID 4 (primary key) 
- first_name: can have multiple words if applicable
- last_name: can have multiple words if applicable
- phone_number: phone number of the doctor
- hospital: hopital the doctor works in if applicable (forign key from the Hospital table) 
- category: type of doctor, such as "General Practitioner", "Cardiology", etc.
- member_price: exclusive price for members if applicable
- fee: consultation fee
- fee_notes: any extra notes related to the fee if applicable (shown as the note in brackets next to the consultation fee in the UI)
- language1: the doctor's preferred language to use (ISO 639-1 two-letter language codes was utilized ("en" for English, "zh" for Chinese, etc.) to represent language
- language2: the second language the doctor can use if applicable (not mandatory)

**Hospital**
- id: randomly generated UUID 4 (primary key) 
- name: name of the hospital
- phone_number: phone number of the hospital
- address_line_1: first line of address of the hospital which could include room number, floor, building name, street name, etc.
- district: district of the hospital location, such as Wan Chai, Tseung Kwan O, etc.
- region: region the hospital location, such as New Territories, Kowloon, etc.

**Availability**
- id: randomly generated UUID 4 (primary key) 
- doctor: the respective doctor this available time slot belongs to (forign key from the Doctor table) 
- day_of_week: the day of the week of this particular time slot
- start_time: the time format is "hh:mm:ss", such as "09:00:00" for 9am and "15:00:00" for 3pm
- end_time
- recurrence_pattern: indicates if this particular pattern can reoccur, such as "weekly", "bi-weekly", etc. This field is kept for further developing the project in case calendar scheduling gets involved

## 2. API
There are 3 APIs as per the project requirements.
1. Get doctor by ID: `http://localhost:8000/doctor/:id`
   - Returns the doctor, and all related info, associated with the id given as a query parameter.
   - An example url would be `http://localhost:8000/doctor/38933b58-57d2-41da-987b-836fe160eaca` as the id is in the form of UUID 4
   - The response will consist of ALL the relevant information to fill out all the information needed shown in the example UI in the requirements
   - An example response for the doctor Amber Tang shown in the example UI in the requirements is as such:
    ```python
     {
          "first_name": "Amber",
          "last_name": "Tang",
          "phone_number": "34206622",
          "hospital": {
              "name": "Marina Medical Central",
              "phone_number": null,
              "address_line_1": "Room 2005, New World Tower One, 16-18 Queen's Road",
              "district": "Central",
              "region": "Hong Kong Island"
          },
          "category": "General Practitioner",
          "member_price": null,
          "fee": 540.00,
          "fee_notes": "not inclusive Western medicine",
          "language1": "zh",
          "language2": "en",
          "availability": [
              {
                  "day_of_week": "Monday",
                  "start_time": "08:30:00",
                  "end_time": "18:30:00"
              },
              {
                  "day_of_week": "Wednesday",
                  "start_time": "08:30:00",
                  "end_time": "18:30:00"
              },
              {
                  "day_of_week": "Thursday",
                  "start_time": "08:30:00",
                  "end_time": "18:30:00"
              }
          ]
      }
     ```
2. Get doctors with filter: `http://localhost:8000/doctor`
   - Returns an array of doctors based on filters indicated in the requirements. If no filters are there, then it will return all the doctors in the database.
   - The array in the response will consist of the same object as seen in the example response from "Get doctor by ID".
   - For filtering by price range, 2 values are put into the url as query parameters, `min_price` and `max_price`, and would return all relevant doctors between those two values (inclusive) 
   - An example url with the language and price range filters is `http://localhost:8000/doctor?min_price=100.00&max_price=1000.00&language=zh`
3. Create a doctor: `http://localhost:8000/add-doctor`
   - Creates a doctor based on the given information in the request body.
   - The request body will include information about the doctor, available time slots, and hospital ID.
   - To associate a doctor with a hospital, the hospital have to be registered into the database first, which can then be associated with the doctor using the hospital ID.
   - An example request body will look as such:
     ```python
     {
          "first_name": "Jacob",
          "last_name": "Smith",
          "phone_number": "12345678",
          "hospital": "72fd9bde-e9f6-4cb6-990d-adfdd7d5a718",
          "category": "Cardiologist",
          "member_price": null,
          "fee": "600.00",
          "fee_notes": "includes Western medicine",
          "language1": "en",
          "language2": null,
          "availability": [
              ["Monday", "09:00:00", "15:00:00", "weekly"],
              ["Wednesday", "12:00:00", "18:00:00", "weekly"],
              ["Friday", "15:00:00", "10:00:00", "weekly"]
          ]
      }
     ```
   
