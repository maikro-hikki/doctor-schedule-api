_This is a quick summary of the project along with the required deliverables. More details about the project and demonstration can be done with a meeting._

_With the requirement of the project to be around 8 hours for development, the development aspect of the project was done over 2 days with around 4 hours of development on each day. The third day was used for documentation, such as making the README file._

# Starting the Server
The python version used during development is 3.12.3 on Windows 10.

It is recommended to work inside a isolated virtual environment to maintain a cleaner setup and prevent conflicts.

After cloning the project and going into the project directory and use the [requirements.txt](requirements.txt) file to install all the packages used in the project using the command `pip install -r requirements.txt`.

The [.gitignore](.gitignore) file is simply used to ignore the sqlite database files when commiting changes to the repo.

To start the server, go into the [myproject](myproject/) directory and run the command `python manage.py runserver`. The available APIs will be discussed in the API section.

To run all the tests automatically, go to the [root directory](myproject/) and run `python manage.py test`.

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
There are 3 APIs as per the project requirements and a 4th extra helper API. The view definitions can be seen in the [views.py](myproject/api/views.py) file and the url path definitions can be seen in [urls.py](myproject/api/urls.py) file.
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
   - To associate a doctor with a hospital, the hospital have to be registered into the database first, which can then be associated with the doctor using the hospital ID. A helper API for registering a hospital has been implemented to help with the demo as seen in point 4.
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
4. Create a hospital: `http://localhost:8000/add-hospital`
   - This is just a quick helper API that can be used to register some hospitals in the database to be used for demonstration when associating doctors with hospitals.
   - The API takes in the hospital information and returns the stored hospital object from the database.
   - An example request and reponse body looks as such:
     ```python
     # Example request body
     {
          "name": "Some Hospital",
          "phone_number": "12345678",
          "address_line_1": "Room 1, 12/F, Some Tower, Some Street",
          "district": "Some Disctrict",
          "region": "Some Region"
      }

     # response body
       {
          "id": "0f2384f9-01d3-47fd-959b-9eabf228abcc",
          "name": "Some Hospital",
          "phone_number": "12345678",
          "address_line_1": "Room 1, 12/F, Some Tower, Some Street",
          "district": "Some Disctrict",
          "region": "Some Region"
      }
     ```
## 3. Testing
All the tests for the project can be seen in the [tests_suite](myproject/myapp/tests_suite/) directory.

To run all the tests automatically, go to the [root directory](myproject/) and run `python manage.py test`.

If only tests from one of the test files needs to be run, then go to the [root directory](myproject/) and run the command `python manage.py test myapp.tests_suite.name_of_test_file`.

## 4. README questions
1. Choice of Framework & Library
   - I have chosen to use Django framework with SQLite database along with the Django REST framework to develop the backend. The main assumptions for these choices is for quick and efficient development (due to the 8 hour deadline) and being able to expand and scale the project even further in the future.
   - The benefits of them are as such:
     - Django allows developers to build applications quickly due to all the built-in features included, such as Object Relational Mapping (ORM), admin panel, etc., and it is also very scalable. It also has a large and active community with a lot of documentation and packages available for developers to use. All of this allows for fast and efficient development, which is really useful to handle the 8 hour time limit of this assignment.
     - SQLite database doesn't need any configuration and is extremely lightweight. It is also very fast and efficient when running queries compared to other databases due to its design and being serverless.
     - Django REST framework provides serialization with can be used to validate and convert data to python data types efficiently which further speeds up development. There are also a lot of other features, such as mechanisms for authentication and API abuse.
   - The drawbacks are as such:
     - Due to all the built in features of Django, there could be a lot of overhead which could be unnecessary for small projects. The structure of Django is also restricted which makes developers less free to choose what they want and don't want to use.
     - SQLite is limited when it comes to scalability as it can struggle with heavy database changes and have storage limitations, such as reduced performance, with large datasets. It also has limited support for concurrency and should only be used in scenarios with low to moderate concurrency requirements.
     - Django REST framework might also have a lot of overhead, especially for smaller projects, due to all the features it has.
2. If I was given more time, I'd focus on improving the security of the project by adding more validations for requests, securing the APIs through authentication and throttling mechanisms, and adding more test cases. I'd also add a logging feature to easily monitor everything that happens in the project, including errors.
3. Stuff to consider for deploying my app to a production environment:
   - Handle all the improvments I have mentioned in the second question.
   - Change the database to a something more scalable, such as PostgreSQL, MySQL, etc.
   - Securing the application is a huge priority as deploying the software to production exposes it to attacks.
   - A lot more test cases should be added, potentially having 100% code coverage, or as close as possible to it.
   - Automating the build process should also be considered to make deployment as consistent and reliable as possible.
   - The database schema should also be revisited for potential expansion of the project.
   - Consider scalability of the project by thinking about load handling and traffic of the server.
   - Documentation is also important to consider to allow for efficient development by developers.
   - Having a backup methods for the data should also be considered to prevent data loss and security in unexpected situations.
4. Assumptions and opinions I have made are as such:
   - For doctors to be associated with any hospitals, the hospital must first be registered.
   - A doctor can only be associated with one hospital but a hospital can be associated with many doctors.
   - A doctor does not need to be associated with a hospital. (This is particularly done as there are more and more "virtual doctors" who does all their consulting through online means. It's just here in case "virtual doctors" are allowed to work with the company in the future)
   - Each time period in the Availability table is associated to one doctor, but a doctor can be associated with many time periods. If the doctor is removed from the database, the related time periods will also be removed.
   - The API responses to retrieve doctors currently contain all the information needed to fill out everything that is seen in the example UI in the requirements, which makes the body really large. I would cosider utilizing multiple APIs with smaller bodies depending on the situation to improve performance.
