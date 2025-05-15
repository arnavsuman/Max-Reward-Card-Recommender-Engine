from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from pydantic import BaseModel
import json
from card_engine import recommend_card

# Create the FastAPI app instance
app = FastAPI()

# Add CORS middleware to allow requests from the frontend (localhost:3000)
origins = [
    "http://localhost:3000",  # Allow frontend to access backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define the data model for the request
class Spends(BaseModel):
    travel: float
    groceries: float
    dining: float


@app.get("/")
def read_root():
    return {"message": "Credit Card Recommendation API is running"}
# Define a route for the recommendation endpoint
@app.post("/recommend")
def recommend(spends: Spends):
    recommended_card = recommend_card(spends)
    return {"recommended_card": recommended_card}
