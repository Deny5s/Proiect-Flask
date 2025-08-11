Event Manager Web Application
📌 Overview
Event Manager is a simple Flask-based web application that allows users to create, view, edit, and book events.
It is designed as a beginner-friendly project for learning Flask and basic web development concepts such as routing, templates, sessions, and forms.

✨ Features
1. User Authentication
Login & Logout system with simple forms (username and password only).

User credentials stored in memory (list of dictionaries in the code).

Logged-in user is stored in the session.

Bonus: password encryption support (optional).

2. Event Management
View Events: All users (logged in or not) can see a list of events with full details.

Add Event: Logged-in users can create new events.

The logged-in user is automatically set as the event organizer.

Edit/Delete Event: Only the event organizer can modify or delete their event.

3. Booking System
Logged-in users can book seats for an event.

Booking is allowed only if:

The user hasn’t booked before for the same event.

There are available seats.

Available seats decrease automatically after booking.

4. Extra Functionalities
Filter events by location or date.

Sort events by event date.

Show a confirmation message after booking.

