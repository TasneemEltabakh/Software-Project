# Software-Project :
This Project is a Fashion Trading website where users can upload clothing items with a description and rate and exchange these items with another user's items with similar rate.

## Table of Contents:
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Accessing the Application](#application)
4. [Directory Structure](#directory-structure)
5. [How Badelha works](#how-badelha-works)
6. [License](#license)

## Installation
### Prerequisites
- Python 3.7 or higher
- Flask
- SQLAlchemy

### Steps
1. **Clonning:**
 ```sh
   git https://github.com/TasneemEltabakh/Software-Project.git
 ``` 
2. ***Create a virtual environment:***
```sh
python -m venv venv
 ``` 
3. ***Activate the virtual environment:***
- ***On Windows:***
```sh
venv\Scripts\activate
 ``` 
- On macOS/Linux
 ```sh
source venv/bin/activate
 ``` 
4. ***Set up the database:***
```sh
python 
from app import app
from models import db
with app.app_context():   
    db.create_all()
``` 


5. ***Run the application:***
```sh
python app.py
 ``` 
## Configuration:

The application configuration is managed through the Config class in config.py. You can modify this file to change settings such as the database URl, secret key, and other application-specific settings.

## Application:
after every thing is done, you can:
- Open your web browser and navigate to 
```sh
http://127.0.0.1:5000
 ``` 
## Directory Structure:
```
project-root/
│
├── templates/
│ ├── index.html
│ ├── productMain.html
│ ├── contact.html
│ ├── shop-cart.html
│ ├── All_Published.html
│ ├── UpdateProduct.html
│ ├── About.html
│ ├── basic.html
│ ├── Login.html
│ ├── main.html
│ ├── Product-details.html
│ ├── Profile.html
│ ├── Register.html
│ ├── search-results.html
│ ├── SellItem.html
│ ├── shop.html
│ └── OrderTracking.html
│
├── static/
│ ├── css/
│ ├── fonts/
│ ├── img/
│ ├── js/
│ ├── sass/
│ └── Source/
│
├── models.py
├── app.py
├── test.py
├── config.py
├── README.md
└── azure-pipline
```

## How Badelha works:

Upload and Rate: Users can easily upload photos of their clothes along with a rating (1-5) based on their condition. This system ensures transparency and helps users find the perfect items.
Trade Options: We offer two convenient options for trading. Users can choose to ship their items or arrange meet-ups with other users for an in-person exchange. We facilitate safe and secure transactions to ensure a smooth trading experience.
Sustainable Shopping: Badelha opens up a new world of sustainable and affordable shopping. Instead of buying new clothes, you can explore a vast collection of pre-loved items and find hidden gems that align with your style.
Join us on this exciting journey towards a more sustainable future. Together, we can make a difference and create a culture of conscious consumption. Visit our website: (still under construction) to learn more about Badelha and start exchanging clothes today.

Let's make fashion sustainable, stylish, and socially responsible with Badelha!

## License:
This project is licensed under the MIT License. See the LICENSE file for more information.

---
Please don't hesitate to reach out if you require any further assistance.

- s-tasneem.attia@zewailcity.edu.eg
- s-rghda.ahmed@zewailcity.edu.eg
- s-nada.soudi@zewailcity.edu.eg
- s-nourhan.mahgoub@zewailcity.edu.eg