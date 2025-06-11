from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict

app = FastAPI()

# Let's code models first


class User(BaseModel):
    id: str
    balances: Dict[str, int] = Field(..., description="balances stored as dictionary, " \
    "where key is the stock name and value is the number of that stock")

class Order(BaseModel):
    userId: str
    price: int
    quantity: int


# This is the stock we have listed, in future change this to array
TICKER = "KFIN"


# Using points as currency for trading
users: list[User] = [
    User(
        id = "1",
        balances = {
            TICKER:10,
            "POINTS": 100000
        }
    ),
    User(
        id = "2",
        balances = {
            TICKER: 10,
            "POINTS": 100000
        }
    )
]


bids : list[Order] = []
asks : list[Order] = []


# API endpoints for the people to hit for trading ;)


# Get all the data related to each user [Only for the admin to access ==> Me <:--)]
@app.get('/data')
def all_stock_data():
    return {"Data": users, "buyer queue": bids, "seller queue": asks}

# Hitting the order api
@app.post('/order')
def order(side:str, order: Order):
    #logs
    print(f"A {side} order of {order} data placed")

    remainingQty = fillOrder(side, order)

    if(remainingQty == 0):
        return users

    # bids => buy orders, asks => sell orders
    if(side=="bid"):
        bids.append(
            Order(
                userId = order.userId,
                price = order.price,
                quantity = remainingQty
            )
        )
        bids.sort(reverse=True, key=get_price)
    elif(side=="ask"):
        asks.append(
            Order(
                userId = order.userId,
                price = order.price,
                quantity = remainingQty
            )
        )
        asks.sort(key=get_price)

    return users

def get_price(e):
    return e.price

def fillOrder(side: str, order: Order):
    #implement logic
    remainingQty = order.quantity
    if(side=="ask"):
        for item in bids:
            if(item.price >= order.price):
                if(remainingQty > item.quantity):
                    remainingQty -= item.quantity
                    exchange(item.userId, order.userId, item.quantity, item.price)
                    bids.remove(item)
                else:
                    item.quantity -= remainingQty
                    exchange(item.userId, order.userId, remainingQty, item.price)
                    return remainingQty
            else:
                return remainingQty
    elif(side=="bid"):
        for item in asks:
            if(item.price <= order.price):
                if(remainingQty > item.quantity):
                    remainingQty -= item.quantity
                    exchange(order.userId, item.userId, item.quantity, item.price)
                    bids.remove(item)
                else:
                    item.quantity -= remainingQty
                    exchange(order.userId, item.userId, remainingQty, item.price)
                    return 0
            else:
                return remainingQty
            
    return remainingQty

# Exchange stocks for money
def exchange(buyer_id: str, seller_id: str, quantity: int, price: int):
    # Verifying if both users exist
    buyer_exists = 0
    seller_exists = 0
    for user in users:
        if user.id == buyer_id:
            buyer_exists = 1
            if(seller_exists):
                break
        elif user.id == seller_id:
            seller_exists = 1
            if(buyer_exists):
                break

    changed_buyer_data = 0
    changed_seller_data = 0
    
    # changes and update
    for user in users:
        if user.id == buyer_id:
            user.balances["POINTS"] -= price*quantity
            user.balances[TICKER] += quantity
            changed_buyer_data = 1
            if(changed_seller_data):
                return
        elif user.id == seller_id:
            user.balances["POINTS"] += price*quantity
            user.balances[TICKER] -= quantity
            changed_seller_data = 1
            if(changed_buyer_data):
                return

    print("***Trade could not execute***")
    return