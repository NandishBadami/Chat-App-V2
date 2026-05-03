# CS50W Capstone Project - Chat App

I have deployed this website on the internet, here is the live website link: 
https://chatappv2.pythonanywhere.com

## Description

This project in totaly inspired from some of the chat applications out there(What's App, iMessages, Signal). The main reason to create this app is because when I started using internet for me internet was all about social media and messaging applications. I always wanted to build my own social media and chat app of my own, as i have already built social media as part of the CS50W project i have noticed that many other social media apps have a messaging app as feature in the same social media app, there was no such feature in the social media app of CS50W so i thought of to build a messaging app of my own.

## Distinctiveness and Complexity:

This project was made from scratch. My project is not a reimplementation of any of the problem sets.

The Main focus of the app is to connect 2 individuals make them friends and let them text/chat/communicate between each other.

It is not a social network because it is a communication tool for texting other people. When compared to social networks, it does not have posting, commenting, or 'liking', which are the basic features most social networks have. On top of that, a social network usually includes many features that allow for networking.

My application is merely an application with one feature in mind, texting/chating. Texting may be part of a social network, but by itself it is not one.

This app might look similar to the mail project of CS50W but the replaying to the user was not very sufficiant in the mail app. So this app staisfies that problem.

And speaking of complexity, things like showing notifications to one user who as got new messages from anouther user was a bit more difficult compared to other parts of the web app. 

Making sure both the users get messages in real time was definetly very hard and I have used 'Socket.io' to achive this functionality. 

Showing weather a user is online or not was also hard. Checking weather the user has read the recived messages or not and showing how many messages are still not read that were sent by other individuals was also very hard to implement.

My project includes 2 Django models on the back end, exceeding the minimum, which is 1 model. It is mobile responsive as well.

Users can see whether the oposite person is online or not, and when a new message is sent it is marked as read if user is online and marked as not read if the user is offline. Messages are given timestamp so that users can come to know when was the message sent or recived. Messages are stored in database along with their timestamp and message read status. Messages gets marked as read automatically when user comes back online again.

In the home page all the friends names will be listed and if the user has got new messages but he has still not seen then it will show user u have got these many number of new messages from these individuals/friends.

Most of these features were able to build because of 'Socket.io' so huge credit goes to the 'python-sokcetio' package.

## How to run the app:

To run this app make sure to install all the packages that are listed in requirements.txt file by running this command:

'pip install -r requirements.txt'.

Next run the below commands in the same directory where manage.py file is present to migrate the server:

'py manage.py migrate'.

Run this Command to actually run the server:

'uvicorn capstone.asgi:application --host 
0.0.0.0 --port 8000 --reload'

Then visit this url: '127.0.0.1:8000' in the browser. Change the port if you hsve entered other than 8000. 

Using uvicorn to run the app because the site uses ASGI instead of old WSGI.

## How to use the app:

To use the app the user must be registerd to the website which can be easily done at "/register" route and the user must be logged in to use the app. After login/register, the user needs to type the username of the user that he wants to chat with if the user with the username exists he/she can chat with each other.

## Application Structure

The back end is made with Python and Django. The front end is mostly HTML and Django Templates and javascript mainly to connect to client side socket.io to the backend and to handle connect, disconnect, status, receiving and transmitting messages to clients.

## Files

### Code
- `chat/views.py`: Contains the logical views for the application.

- `chat/models.py`: Defines the database structure.

- `chat/urls.py`: Handles path registration.

- `chat/admin.py`: Registers models to the Django admin interface.

- `chat/socketio_events.py`: Contains code for establishing connection to socketio and handle user connection, disconnection and messaging features.

- `capstone/asgi.py`: Configures the app to use ASGI server instead of WSGI

### Django Templates

- `chat/templates/chat/chat_app.html`: Displays the chat box interface and all the chat history with that perticuler individual. Contains javascript code to handle socket.io events.

- `chat/templates/chat/index.html`: Displays all people who the user has already texted before(friends) and also shows number of unread new messages as notifications(if any).

- `chat/templates/chat/layout.html`: General App Layout.

- `chat/templates/chat/login.html`: Displays Login Page.

- `chat/templates/chat/register.html`: Displays registration Page.

### Documentation
- `README.md`: This documentation file.

## Additional Information
- **Security:** Databases store hashed passwords for security.
- **Privacy Note:** Chat messages are not currently encrypted.