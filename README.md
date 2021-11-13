# Bookido

Developer: Neda Keshavarzi

![Screen shot of start page]()

[Deployed page]()

## Table of Content


1. [Project Goals](#project-goals)
2. [User Goals](#user-goals)
3. [Structure](#structure)
    1. [Home Screen](home-screen)
    2. [Booking a Product](#booking-a-product)
    3. [Admin section](#admin-section)
    4. [Booking Schedule](#booking-schedule)
4. [User Stories](#user-stories)
    1. [Customer User Stories](#customer-user-stories)
    2. [Admin Member User Stories](#admin-member-user-stories)
    3. [Site Owner Goals](#site-owner-goals)
5. [Technical Design](#technical-design)
    1. [Flow Chart](#flow-chart)
    2. [Data Models](#data-models)
    3. [User Interface](#user-interface)
6. [Features](#features)
    1. [Feature 1: The Product Booking System](#feature-1-the-product-booking-system)
    2. [Feature 2: The Schedule](#feature-2-the-schedule)
    3. [Feature 3: The Admin section](#feature-3-the-admin-section)
    4. [Features to be implemented](#features-to-be-implemented)
7. [Technologies Used](#technologies-used)
    1. [Languages](#languages)
    2. [Applications, Platforms and Libraries](#applications-platforms-and-libraries)
        1. [Applications and Platforms](#applications-and-platforms)
        2. [Python Libraries](#python-libraries)
        3. [Third Party Libraries](#third-party-libraries)
8. [Validation](#validation)
9. [Testing of Customer User Stories](#testing-of-customer-user-stories)
10. [Testing of Admin Member User Stories](#testing-of-admin-member-user-stories)
11. [Testing of Site Owner Goals](#testing-of-site-owner-goals)
12. [Bugs](#bugs)

## Project Goals

Create a SAS service that the owner can add products and services and customers can book those product and services. The scope is wide in a sense that the products and services can be anything from a meal in a restaurant to a service like massage, tourism, booking a hotel or any kind of event that can be scheduled.


## User Goals

Users should be able to book their desired product or service via the interface of this product.

### Target Audience

- General public
- Tourism, Hotels and service providers providing service to the public.


## Structure

The Bookido Booking System is a command prompt based system that gets inputs from users to book a product and also create new products. It extensively relies on user input to be able to store given data in the product catalog and also user information to the products when a user books a service or a product.

### 1. Home Screen

<details>
    <summary>Click here to view the home screen</summary>

![Screenshot of Home screen]()

</details>

The first thing that the user sees when starting the application is a welcome message and the options to choose what to do.

- Book a product - It takes the user to book their desired product that is in the system.
- Admin section - takes users to the admin section where they can create a new product.

### 2. Booking a product

<details>
    <summary>Click to view image</summary>

![Product booking]()

</details>

Users will be taken in the process of booking a product which leads to their email being stored in the data store, Google spreadsheet, and ultimately adding them to the Google calendar event summary section.

### 3. Admin section

Admins of Bookado can enter the admin section via a password and after logged in, they can add new products.

<details>
    <summary>Click to view image</summary>

![Admin section]()

</details>

### 4. Booking Schedule

Each product while getting created need to have defined date, time and duration. if duration not set it will default to 45 minutes. This leads to creation of a Google calendar event with the respective information of that product.


## User Stories


### Customer User Stories:

1. As a user, I would like to book a product that is available in the system
1. I would like to be notified if I have entered the correct data
1. I would like to be able to confirm my booking before it happens.
1. I would like to get a confirmation of my booking with proper information about the product I booked.
1. I would like to cancel my booking at any time during the booking process.
1. I would like to go to the main menu anytime during the application flow


### Admin Member User stories:

1. As an admin, I would like to create products in the system
1. As an admin, I would like the products that are created to be stored in the data store, Google spreadsheet
1. As an admin, I would like to have a Google calendar event based on the information added when creating a product
1. As an admin, I would like the description of the Google calendar event summary be updated with the email address and number of users booked
1. As an admin, I would like the product catalog to be updated by the email address of customers who booked a given product


### Site Owner Goals

I would like for the application to contain validated Python code without returning any errors, whatever the user does

## Technical Design

### Flowchart

Below is a flowchart describing the structure of the application, created with [Lucidchart](https://lucid.co/product/lucidchart).

<details>
    <summary>View flowchart here</summary>

![Flowchart]()

</details>

### Data models

There are two main data models used in this project. First one is the **Product** model which holds information about a product in the system and the other one is **ProductRow** which holds the __row_number__ of a product in Google spreadsheet that can be used to update a product in the sheet.

These models will be converted to Python dict at the time of storage and also the data retrieved from the spreadsheet in the form of Python dict will be converted to Pydantic data models to be used more reasily and properly throughout the application.

### User interface

The user interface is in the from of command prompt and command line input. It's very important that the system shows proper and enough information to the user to be able to decide on which flow to take and also what direction to go to. 

## Features

### Feature 1: The Product Booking System

This is the main feature of the application. Products information in the system get shown to the user and their email address is taken to book the product.

The flow is as follow:

1. Customer will be presented with the list of products available in the system
1. If a products date is in the past that product will not be shown to the customer
1. When the customer chooses a product, the information about that product is shown including summary and the date.
1. If the customer confirms by choosing continue, their email address is asked.
1. After their email address is taken and validated, system will save their information in the spreadsheet and also add their email to the Google event calendar summary to be viewed by the admin.
1. Finally a confirmation is shown to the user with the date of the product so that they can take note of that.


<details>
  <summary>Click to view images of feature 1</summary>

*Entering month*
![Product Booking System]()

*Booking confirmation*
![Confirm product booking]()

*Google Calendar entry*
![Google calendar entry]()

*Entry in Google Sheets*
![Google sheets]()

</details>


### Feature 2: The Schedule

When a product is created by an admin, the date, time and duration is asked. Based on these information along with the title and summary of the product, a Google calendar event is created. This will be the key for the admin to view who has booked a product by looking at Google calendar of the company for this service.


<details>
    <summary>Click to view images of feature 2</summary>

*The schedule*
![The Schedule]()


</details>


### Feature 3: The Admin section

This section is where an admin can add a new product. information about a new product is asked from the admin. This information includes following:
- title
- description
- address
- capacity
- price
- date and time

The system will generate unique ids for both the product and also for the calendar_id that will be used to create the Google calendar event.
On successful product creation, admin will be presented with a confirmation.

<details>
    <summary>Click to view images of feature 3</summary>

![Create a product]()


</details>


### Features to be implemented
One feature that would be great to have is to be able to create reccuring products in that instead of having one slot available for a product to be booked, a reccuring event can be setup for the customers to choose from.
Also it would be great to create a reminder event on the customers calendar when they book a product.


## Technologies used

### Languages

- [Python 3](https://www.python.org/) - Was used solely to create this project.


### Applications, Platforms and Libraries


#### Applications and Platforms

- [Git](https://git-scm.com/) - Version control system used to commit and push to Github via Gitpod.

- [Github](https://github.com/) - The projects repository and all its branches were commited, pushed and deployed to Github.

- [Gitpod](https://gitpod.com/) - All code was written and tested using the Gitpod web-based IDE.

- [Heroku](https://www.heroku.com) - Used to deploy the application.

- [Lucidchart](https://lucid.co/product/lucidchart) - Lucidchart was used to create the [flowchart](#flowchart) of the project.

- [Google Calendar](https://calendar.google.com/) - The users input data creates and edits events on Google Calendar

- [Google Sheets](https://calendar.google.com/) - - The users input data creates and edits content on Google Sheets

- [Google Cloud Platform](https://console.cloud.google.com/) - All data send and received with the help of the Google API, through the Google Cloud Platform


#### Python Libraries

I have used these third party libraries and Python libraries for this project:

- datetime: As time is of essence when working with calendars, this was essential.

- os: By using os I was able to both have my password in the workspace without pushing it to github, but also use it as a config var on heroku.

- re: to be able to validate using regular expressions

- uuid: to generate universally unique ids

- pydantic: Data validation and settings management using python type annotations.

#### Third Party Libraries

- googleapiclient.discovery: needed to work with the Google API

- google.oauth2.service_account: So the application can access the account that the sheet and calendar are on with the credentials

- gspread: so the application can read Google Spreadsheets

## Validation
To be added.

## Testing of Customer User Stories

User stories are tested with the features that cover them. All user stories passed the tests.
To be added.

## Testing of Admin Member User Stories

To be added.

## Testing of Site Owner Goals

To be added

# Bugs

To be added
