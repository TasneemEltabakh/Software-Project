# Software-Project :
This Project is a Fashion Trading website where users can upload clothing items with a description and rate and exchange these items with another user's items with similar rate.

# Table of Contents:
1. Installation
2. Configuration
3. Usage
4. Features
5. Directory structure
6. Contributing
7. How Badelha works
8. License

# Installation
## Prerequisites
- Python 3.7 or higher
- Flask
- SQLAlchemy

## Steps
1. Clonning:
https://github.com/TasneemEltabakh/Software-Project.git

2. Create a virtual environment:
python -m venv venv

3. Activate the virtual environment:

- On Windows:
venv\Scripts\activate

- On macOS/Linux
source venv/bin/activate

4. Set up the database:

python 
from app import app
from models import db
with app.app_context():   
    #db.create_all()


5. Run the application:
python app.py



# How Badelha works:

Upload and Rate: Users can easily upload photos of their clothes along with a rating (1-5) based on their condition. This system ensures transparency and helps users find the perfect items.
Trade Options: We offer two convenient options for trading. Users can choose to ship their items or arrange meet-ups with other users for an in-person exchange. We facilitate safe and secure transactions to ensure a smooth trading experience.
Sustainable Shopping: Badelha opens up a new world of sustainable and affordable shopping. Instead of buying new clothes, you can explore a vast collection of pre-loved items and find hidden gems that align with your style.
Join us on this exciting journey towards a more sustainable future. Together, we can make a difference and create a culture of conscious consumption. Visit our website [website URL] to learn more about Badelha and start exchanging clothes today.

Let's make fashion sustainable, stylish, and socially responsible with Badelha!

#how to run the code
-first connect to the database on phy my admin using a server (we used Xampp)
-run this in the terminal to create the database
-python 
from app import app
from models import db

with app.app_context():
    
    #db.create_all()
-Now the database should be created and connected
-Run python app.py 
-open your local host to view the website
