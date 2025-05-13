# Item 1 MaxxMai Card Recommender Engine

The MaxxMai Card Recommender is a web application built using FastAPI for the backend and React for the frontend. The goal of this project is to provide users with personalized credit card recommendations based on their monthly spending in categories like travel, groceries, and dining.

How the System Works
The overall workflow is divided into two parts: the Frontend (React) and the Backend (FastAPI). Here’s a breakdown of each component and how they interact.

Frontend: React
User Input:

The user visits the frontend of the application, which is a simple form with three fields: Travel, Groceries, and Dining.

The user inputs their estimated monthly spending in these categories.

Form Submission:

When the user submits the form, the data is sent to the backend using a POST request. This data includes the amount the user spends in each of the three categories.

The frontend makes a network request to the backend (http://localhost:8000/recommend), passing the user's spending data as a JSON object.

Displaying Results:

After the backend processes the data, it sends back the recommended card.

The frontend then displays the recommended card to the user.

Styling:

The frontend uses a simple React interface with inline styling and a form for input. The result of the recommendation (the name of the recommended credit card) is displayed dynamically below the form.

Backend: FastAPI
FastAPI Setup:

The backend is built using FastAPI, which is a modern web framework for building APIs with Python. FastAPI is known for being fast and easy to use, and it supports asynchronous request handling out-of-the-box.

The backend is running on localhost:8000.

CORS Configuration:

CORS (Cross-Origin Resource Sharing) is configured to allow requests from https://localhost:3000 (the address where the React frontend is running). This ensures that the frontend can securely communicate with the backend even though they are running on different ports.

Recommendation Logic:

The backend has an endpoint /recommend that listens for POST requests containing the spending data (travel, groceries, dining).

Once the backend receives the data, it calls the function recommend_card (imported from the card_engine.py file) to process the user's input and determine the best card recommendation.

The result of the recommendation is then returned to the frontend as a JSON object.

Recommendation Model (card_engine.py):

The backend logic in card_engine.py contains the rules or algorithms used to recommend a credit card based on the user's spending habits.

For simplicity, this might involve:

Checking which category the user spends the most on (e.g., travel, dining, or groceries).

Suggesting a card with the best rewards in that category.

The recommendation is based on predefined logic (which can later be enhanced with machine learning or a more sophisticated model).


INSTALIING

Install Dependencies:

```bash
git clone https://github.com/
cd maxxmaicard/backend
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```


RUN BACKEND
Start the FastAPI server:
```bash
uvicorn main:app --reload

```

Run FRONTEND
```bash
cd ../
cd frontend
npm install   
npm run dev   # Or use `yarn dev` if you prefer yarn
```

# Item 2: MongoDB Email Statement and User Profile Uploader

This Python script processes email sender information and associated statement content, storing both in a MongoDB database. It extracts user details from the email header and saves user preferences and associated financial statements into separate MongoDB collections.

Extracts sender's name and email address from email headers.

Prompts for user preference (Preferred Banking Partner).

Inserts statement content into the statements collection.

Links and stores user profile details (including preferences) in the user_profiles collection.

Automatically maintains the relationship between statement and user using MongoDB _id.
Installation
Ensure MongoDB is running locally.
```bash
pip install pymongo
python email_auth.py
```

# NOTES

The frontend form collects values for travel, groceries, and dining, and sends them as the JSON payload to the backend for processing.

The backend API (POST /recommend) expects the following JSON structure:
{
  "travel": 100.0,
  "groceries": 50.0,
  "dining": 25.0
}

It will return a JSON response like this:
{
  "recommended_card": "Card Name"
}



# CURL EXAMPLES
run backend server before running curl

 RUNNING ON TERMINAL BELOW COMMAND

1.   Basic Spend Input
```bash
curl -X POST http://localhost:8000/recommend  -H "Content-Type: application/json"  -d "{\"travel\": 100.0, \"groceries\": 50.0, \"dining\": 25.0}"
```
EXPECTED OUTPUT : {"recommended_card":"Dining Card"}
AcTUAL OUTPUT : {"recommended_card":"Dining Card"}

2. Above Normal Spending
```bash
curl -X POST http://localhost:8000/recommend  -H "Content-Type: application/json"  -d "{\"travel\": 100.0, \"groceries\": 500.0, \"dining\": 2005.0}"
```
EXPECTED OUTPUT : {"recommended_card":"Groceries Card"}
AcTUAL OUTPUT : {"recommended_card":"Groceries Card"}

3. High Spending Edge Case
```bash
curl -X POST http://localhost:8000/recommend  -H "Content-Type: application/json"  -d "{\"travel\": 10000, \"groceries\": 20000, \"dining\": 150000}"
```
EXPECTED OUTPUT : {"recommended_card":"Travel Card"}
AcTUAL OUTPUT : {"recommended_card":"Travel Card"}
