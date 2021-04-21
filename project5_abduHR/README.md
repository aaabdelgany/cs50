Welcome to abduHR! abduHR is a web app that is intended to be used as an in-house HR system to keep track of employee communication data. Users can log on and access a common shared pool of employees to edit their data or create / add new employees. Users can also do mass-updates or imports of their employee data via a csv file. This project primarily uses Django, Javascript, HTML,CSS (implemented mainly via the bootstrap 5 library). This project in some ways is similar to the social network site, but I believe it's complexity exceeds that by implementing file processing, improved pagination, and improved front end javascript for displaying / posting data. I have also enforced the use of csrf tokens in all post requests by grabbing the csrf token from the browser cookies, which is not something I did in earlier projects.

The core appeal of this app is the use of csv files to create/update/export employee data en masse. Data Integrity is enforced by adding a unique clause to the employee email, as well as forced checking of submitted phone number / email format through Regular Expressions. Users have the ability to export their employee data in the form of a csv file, as well as import a csv file to add on to their existing employee base. Users can additionally use a csv file to update their current employees en masse. This was included in the event that there were layoffs or any other reason to change the employment status of a group of employees to inactive at once.

---------------------------------------------------------
Project Specifications:
1. Create New Employees manually. This will be done via javascript without reloading the page. If an invalid phone number or email are entered, the system will flash a warning. If an email is entered that is already taken, the system will flash a warning.
2. Display all employees on the home page. The home page will display employee id, first and last name, as well as a link to edit that employees information.
3. Create New Employees via a csv file. This will be done using a file that has the following format: 
    Column A: First Name
    Column B: Last Name
    Column C: Email
    Column D: Phone Number
    Column E: The employees status with the company. This will either be active or inactive.
4. Export all current employees via a csv file. This will generate a file that is in the same format as the import file.
5. Update employees via a csv file. This will use the email field(a unique field) to perform updates to employee data using the same import file format.
6. Display Inactive Employees. This page will display all current inactive employees
7. Editable Pagination. The Home page and Inactive page will have pagination and let users decide if they want to display 10, 25, or 50 employees at once.
8. Editing Employees: Editing an employee will allow you to change their information. If a phone number or email are entered in incorrect format, the system will flash a warning. If an email is entered that is already taken, the system will flash a warning.
9. Search: Search for an employee by their email will take you to their edit page. If no employee with that email is found the system will display a warning.

---------------------------------------------------------
Files & Directories that I created:
abduHR
    models.py - User model and Employee model
    urls.py - Contains all app paths 
    views.py - main file that handles the server side processing of all web requests sent through the app.

    static/abduHR:
        main.js - Main javascript file used throughout the app. Chose to only use one javascript file that is used for all pages. The file looks for an element and if it exists adds an event listener / some extra JS code. If the file doesn't exist, the system won't try to touch the DOM element and cause an error
    templates/abduHR:
        edit.html - edit page
        impemp.html - Import / Export page
        inactive.html - Page that displays all inactive employees
        index.html - login page
        landing.html - home page after authentication, shows all employees
        layout.html - template that is extended by all the others
        login.html - 
        register.html - registration page
        update.html - page that allows users to update employees via a csv file


---------------------------------------------------------
Running the application:

After downloading the application distribution and making the necessary migrations, the django server can be run via the following cli command at the projects top directory: python3 manage.py runserver

Users can then navigate to localhost:8000/abduHR/ to register and begin using the application.