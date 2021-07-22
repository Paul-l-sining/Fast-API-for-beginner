from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel

# API stands for Application Program Interface
# Anything you retrieve from API is in JSON format

# To start our API, type, "uvicorn <file Name Without .py>:app --reload" in your terminal
# To view available content: "http://127.0.0.1:8000/docs", where you can try it out.


app = FastAPI()


class Item(BaseModel):
    type: str
    price: str
    brand: str
    year: str = ""  # set to optional


class UpdateItem(BaseModel):
    type: str = ""
    price: str = ""
    brand: str = ""
    year: str = ""


@app.get("/")
def home():  # no parameter taken.
    return {"Data": "Testing"}


@app.get("/about")
def about():
    return {"Data": "About"}


# we use inventory as an example, however, in real world, we use real database
inventory = {
    1: {
        "type": "Sedan",
        "price": "30k",
        "brand": "Mercedes",
        "year": "2017"
    },
    2: {
        "type": "Suv",
        "price": "26k",
        "brand": "Honda",
        "year": "2018"
    },
    3: {
        "type": "Coupe",
        "price": "40k",
        "brand": "BMW",
        "year": "2020"
    }
}


# Taking path / endpoint parameters
# "parameter: type" is a type hint in Python
@app.get("/get-item/{item_id}")
def get_item(
        item_id: int = Path(None, description="The Item ID you'd like to view")):  # Path(Default value, description)
    return inventory[item_id]


# Query parameters: '?'
# To call: "http://127.0.0.1:8000/get-by-name?type=XXX&test=XXX"
@app.get(f"/get-by-name")  # '/get-by-name' + '?' + 'PARAMETER=XXX' + '&' + '....'
def get_item(*, type: str = "", test: int):  # Set parameter a default value.
    for item_id in inventory:
        if inventory[item_id]["type"].lower() == type.lower():
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item name not found.") # raise 404 as error msg.


# Request Body Method
# To make user store info into your inventory, use "BaseModel" to create a class to store info
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists.")

    inventory[item_id] = item  # Fast API is smart enough to recognize and convert item into JSON format.
    return inventory[item_id]


# Post Method; in other words, update the current data
@app.put("/create-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")

    if item.type != "":
        inventory[item_id]["type"] = item.type

    if item.price != "":
        inventory[item_id]["price"] = item.price

    if item.brand != "":
        inventory[item_id]["brand"] = item.brand

    if item.year != "":
        inventory[item_id]["year"] = item.year

    return inventory[item_id]


# Delete Method
@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The Item ID to delete")):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")

    del inventory[item_id]  # delete that item
    return {"Success": "Item deleted successfully!"}
