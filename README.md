# Django Library Project

This is a Django project for managing a library, including functionality for handling books, authors, user authentication, and favorite books. The project also includes JWT authentication for securing API endpoints.

## Project Setup

### 1. Install Requirements

Install the required packages using `pip`:

2. Run Migrations
Apply migrations to set up the database schema:

python manage.py makemigrations
python manage.py migrate

3. Create a Superuser
To create a superuser for accessing the Django admin panel:

python manage.py createsuperuser

4. Run the Development Server
To start the server, run:

python manage.py runserver

Access the application in your browser at http://127.0.0.1:8000/.

API Endpoints
1. User Registration and Authentication
Register: /register/
Login: /login/

2. Book Management
List Books: /books/ (GET)
Add a Book: /books/ (POST)
Retrieve/Update/Delete a Book: /books/<int:pk>/ (GET/PUT/DELETE)

3. Author Management
List Authors: /authors/ (GET)
Add an Author: /authors/ (POST)
Retrieve/Update/Delete an Author: /authors/<int:pk>/ (GET/PUT/DELETE)

4. Favorites and Recommendations
List Favorite Books: /favorites/ (GET)
Add a Book to Favorites: /favorites/ (POST)
Get Book Recommendations: /recommendations/ (GET)
