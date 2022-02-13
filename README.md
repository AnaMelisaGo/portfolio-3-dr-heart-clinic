# Dr Heart Clinic - Portfolio 3
***
 
## Table of Contents:
* [What does it do and what does it need to fulfill?](#what-does-it-do-and-what-does-it-need-to-fulfill)
* [Functionality of Project](#functionality-of-project)
* [Wireframing](#wireframing)
* [Technology Used](#technology-used)
* [Database](#database)
* [Features](#features)
   * [Future Features](#future-features)
* [Testing](#testing)
   * [Defensive Design](#defensive-design)
* [Deployment](#deployment)
* [Credits](#credits)
   * [Special Thanks & Acknowledgements](#special-thanks--acknowledgements)
 
***
 
## Welcome to Dr. Heart Clinic!
 
![The final project](static/images/screenshot-responsive.png)

[This is the deployed project](https://portfolio-3-dr-heart-clinic.herokuapp.com/)

[To access the dr-heart-clinic spreadsheet](https://docs.google.com/spreadsheets/d/1WnWbp-BpXRPl4qDXBxWytC5SYB3dAyzomdwumLzJAzE/edit?usp=sharing)
 
***
 
## What does it do and what does it need to fulfill?
The application is to help the "Dr. Heart Clinic" to control data of each patient's tests and visualize all monthly tests statistics and tests revenue data.
 
### Functionality of Project
This application contains functions:
 - to gather data of each patient
 - to save data into a google spreasheet
 - to calculate total tests
 - to calculate amount value of each tests and update the clinic's monthly revenue.
 - view worksheets data
 
[Back to top](#table-of-contents)
 
## Chart
 
The flow chart

![Flow](static/images/clinic-flow-chart.png)
 
## Technology Used
 
#### Languages, Frameworks, Editors & Version Control:
 
* Tech stack used:

   - [Python](https://www.python.org/)

* Editor and Version Control:

   - Git for version control

   - [Gitpod](https://www.gitpod.io/) is used as the editor

   - [Github](https://github.com/) is used to store the project

   - [Heroku](https://www.heroku.com) is used to deploy the project
 
#### Tools Used:
 
* Google Drive is used to store the spreadsheet of the project
* Google Sheets to store all patients data and all the calculated data

[Back to Top](#table-of-contents)

## Features
 
The project boasts several key features:

* WELCOME MESSAGE AND CHECKING FILE TO UPDATE

![Welcome message](static/images/screenshot-start.png)

Welcomes the user when the app is opened. It checks all files and get the last file for data update. The name of the file to be updated appears underneath so the user knows what file to update, which is, the current month.

* NEW WORKSHEET

![Create new worksheet](static/images/screenshot-create-new-worksheet.png)

If the app detects that there is no file to update when user opens the app (meaning last file is already calculated and tallied), it asks the user to create a new worksheet before starting to work.

* MAIN MENU

![Working options](static/images/screenshot-main-menu.png)

There are different options in the main menu of the app:

- Add data to update file
- Tally, calculate and update worksheets
- View worksheets data
- Exit

* ADD DATA

![To update file with new data](static/images/screenshot-update-file.png)

To enter new data to update current month worksheet:

      - data should be separated with comma, no spaces.
      - Patient name can have spaces.
      - Use only the tests keywords to update file

An example is shown to guide the user.

* TALLY, CALCULATE AND UPDATE WORKSHEET

![Tally and calculate](static/images/screenshot-tally.png)

When tally option is selected, a message is prompted to the user reminding that the worksheet will not be accessible for new data and a new worksheet will be created.

This feature includes:

      - Appending "CLOSED" text into the worksheet as a sign that the worksheet is tallied and closed
      - Gets all the patients tests and tally them
      -  Calculates the amount value of each tallied tests to get the revenue
      - Updates the worksheets to save all gathered data and the calculated revenue

* VIEW DATA FROM WORKSHEET

![To view worksheet data](static/images/screenshot-view-files.png)

   * View patients

      To view all patients name and tests.

   * Test statistics
   
      To view all tests tally result.

   * Revenue File
   
      To view monthly revenue by test.

[Back to Top](#table-of-contents)
 
#### Future Features:
 
* For future features:

   * Search patient and view history of patient's test
   * Add date when updating patients data
   * Calculate total revenue of a specific range (6 months / yearly)
 
## Testing
 
[Pep8online](http://pep8online.com/) is used to check code for validation to make sure there are no errors or bugs.

Manual testing was done during the development of the application. The terminal is used for testing before pushing to branch to see there's no error in the code.

Tested all new data are saved to the worksheet, new worksheet is accessible when app is running. Tested all the calculations are right and each worksheet are updated when tallied and data is calculated.

Tested deployed app to make sure all functions are working well and no error or bugs.
 
### Found Bugs and Fixes:

My initial code for the back option was calling the function that called another function. My mentor helped me fix the problem since it can consume a lot of memory and it's not a good practice. I fixed the problem using while loops and the back option is done by breaking out from the loop.

I manage to create a code to keep the working cycle without rerunning the app after tallying and calculating data. I used a while loop and validates the answer (Y or N) and if the answer is in the options it breaks the loop and afterwards it returns the validated answer and a function is executed according to the user's answer. 'Y' means create new worksheet and continue working on the new worksheet. 'N' means exiting app.

String formatting was a life-saver for printing data from a worksheet into the terminal. It aligns all the data for readability.

Time module is very handy for pausing code for a few seconds so that the user doesn't get lost when a message prompts. It's also handy for showing data one at a time specially in View patients option.
 
[Back to Top](#table-of-contents)
 
## Deployment
 
Detail deployment here...
 
[Back to Top](#table-of-contents)
 
## Credits
 
* Love Sandwich
* Geeks for geeks
* Stackoverflow
 
[Back to Top](#table-of-contents)
 
#### Special Thanks & Acknowledgements:
 
* Team 11 🤜
* To my mentor, who patiently guided me along my coding journey.
* To all my family, especially my husband and my daughter for encouraging me everyday.
* To my work and co-workers for inspiring me in making this project.
* To the tutors and the CI slack community.
 
###### <i>Disclaimer: This project was created for educational use only as part of the portfolio 3</i>
 
[Back to Top](#table-of-contents)
