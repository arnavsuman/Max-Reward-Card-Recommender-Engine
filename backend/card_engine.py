import json

# Hardcoded card data (from cards.json)
with open("cards.json", "r") as f:
    cards = json.load(f)

def recommend_card(spends):
    # Simple logic to recommend card based on spends
    best_card = min(cards, key=lambda x: abs(x['spend_limit'] - sum(spends.dict().values())))
    return best_card["name"]
