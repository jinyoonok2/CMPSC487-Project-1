# CMPSC487-Project-1
## CMPSC487 SunLab Access Database Interaction Project part 1

_Code was built on Pycharm IDE for Python programming_

## Getting Started

**Python Version: 3.11**

### 1. Clone the Repository
#### First, navigate to the directory where you want to store the project. Then, clone the project repository:

```
git clone https://github.com/jinyoonok2/CMPSC487-Project-1.git
cd CMPSC487-Project-1
```

### 2. Install Dependencies
#### Make sure you have `pip` (Python package installer) ready. Now, install the necessary packages:

```
pip install -r requirements.txt
```

### 3. Running the Program
#### With all dependencies installed, navigate to the project directory (if you haven't already) and run:

```
python db_login_final.py
```

#### This will launch the program.

## Usage

![Description of Image1](images/1.jpg)

When you run the program, you will be asked for the userId to open the database browsing interface.
only userId of the user that has "janitor" user type will be granted with access, otherwise it will be denied like picture above.

For the user documents you can find them in users.json file in this repository to see what user objects were added to the Mongo DB server. (You can also check accessLogs.json to check the accesslogs that were added to the database.)

![Description of Image2](images/2.jpg)

For now, you can use "999999999" for the userId to access the interface since it is the only userId that has userType of "janitor".

when the GUI opens, its first interface will ask you the password. The correct password is "jinyoon981023"

![Description of Image1](images/3.jpg)

If the password is invallid, the access will be denied.

![Description of Image1](images/4.jpg)

After the login, you will see the database browsing interface. 
It has Default Start Date, End date, Start time and End Time.
The default was given to prevent various errors that cause when the program retrieve the information from Mongo DB.
Start Time and End Time has default of the current time. (If current time is 20:00:00, it will be 20:00:00)
Start Date has date one week before the current date according to the user's machine environment.
End Date has date of the current date. (If the current date is 2023/09/02, it will be 2023/09/02)

![Description of Image1](images/5.jpg)

User also can give specific userId to browse the only accesslogs that has according userId from the input.

![Description of Image1](images/6.jpg)

The date can also be passed as input.
In the above picture, End date had been changed to 2023-08-26. and since there is no accesslogs that have date of 08/26 with userId 973997270, it does not print anything.

![Description of Image1](images/7.jpg)

This is an example of using date and time. browsed date 08/31 between time 00:08:45 and 19:08:45
Now we can see results that exist in the corresponding time interval.

![Description of Image1](images/8.jpg)

When user does not input anything, it will use default date/time and print every user between that time interval.

![Description of Image1](images/9.jpg)

The program prevent the user input end time prior to start time. This also works for date.

Thank you for reading.
