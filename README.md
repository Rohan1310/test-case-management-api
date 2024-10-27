Test Case Management

Getting Started

To run the project, please follow these steps:

Prerequisites
Make sure you have the following installed on your system:

Python 3.x

Flask

pip (Python package installer)

Step 1: Create a Virtual Environment

Navigate to the project directory:

cd path/to/your/project

Create a virtual environment. You can name it as you prefer (e.g., venv):

python -m venv venv

Activate the virtual environment:

On Windows:

venv\Scripts\activate


On macOS and Linux:

source venv/bin/activate


Step 2: Install Required Packages


Install the necessary packages listed in requirements.txt:


pip install -r requirements.txt

Step 3: Create a .env File

Create a .env file in the root directory of your project.

Copy and paste the contents of sampleenv into your newly created .env file.

Step 4: Configure Google Client ID and Secret

Obtain your Google Client ID and Client Secret by creating a project on the Google Developer Console.

Add the following lines to your .env file, replacing <YOUR_CLIENT_ID> and <YOUR_CLIENT_SECRET> with your actual values:

GOOGLE_CLIENT_ID=<YOUR_CLIENT_ID>
GOOGLE_CLIENT_SECRET=<YOUR_CLIENT_SECRET>


Step 5: Create a Secret Key and JWT Key

Generate a random secret key and JWT key for your application. You can use the following command in Python to generate a secure key:

python

import os

print(os.urandom(24).hex())

Add the keys to your .env file:

SECRET_KEY=<YOUR_SECRET_KEY>

JWT_SECRET_KEY=<YOUR_JWT_SECRET_KEY>


Step 6: Run the Application

Finally, run the Flask application with the following command:

flask run

You’re All Set!

Your application should now be running. Open your web browser and navigate to http://127.0.0.1:5000 to access it.
