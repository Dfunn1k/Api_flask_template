import uuid

from flask import Flask, request, jsonify
from flask_smorest import abort

from db import stores, items

app = Flask(__name__)


# ----- Stores -----
@app.get('/stores')
def get_all_stores():
    return jsonify({"stores": list(stores.values())}), 200


@app.get('/store/<string:store_id>')
def get_store(store_id):
    if store_id not in stores:
        abort(404, message="Store not found")

    return jsonify(stores[store_id]), 200


@app.post('/store')
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
        abort(400,
              message="Ensure 'name' is included in JSON payload")

    print(stores.values())
    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, message="Store already exist!")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return jsonify(store), 201


@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    if store_id not in stores:
        abort(404, message="Store not found")

    del stores[store_id]
    return jsonify({"message": "Store deleted."}, 200)


@app.put('/store/<string:store_id>')
def update_store(store_id):
    if store_id not in stores:
        abort(404, message="Store not found")

    store_data = request.get_json()
    allowed_parameters = ["name"]

    if not all(param in store_data for param in allowed_parameters):
        abort(400,
              message="Ensure 'name' is included in JSON payload")

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="Store already exists")

    store = stores[store_id]
    store.update(**store_data)

    return jsonify(store), 200


# ----- Items -----
@app.get('/items')
def get_all_items():
    return {"items": list(items.values())}, 200


@app.get('/item/<string:item_id>')
def get_item(item_id):
    if item_id not in items:
        abort(404, message="Item not found")

    return items[item_id], 200


@app.post('/item')
def create_item():
    item_data = request.get_json()
    allowed_parameters = ["name", "price", "store_id"]

    # check if the parameters are included in the JSON
    if not all(param in item_data for param in allowed_parameters):
        abort(400,
              message="Ensure 'name', 'price', 'store_id' are included in the JSON payload")

    # validate if the item already exist
    for item in items.values():
        check_name = item["name"] == item_data["name"]
        check_store_id = item["store_id"] == item_data["store_id"]

        if check_name and check_store_id:
            abort(400, message="Item already exist!")

    # check if store_id is valid
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return jsonify(item), 201


@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    if item_id not in items:
        abort(404, message="Item not found")

    del items[item_id]
    return jsonify({"message": "Item deleted."}), 200


@app.put('/item/<string:item_id>')
def update_item(item_id):
    if item_id not in items:
        abort(404, message="Item not found.")

    item_data = request.get_json()
    allowed_parameters = ["name", "price"]

    if not all(param in item_data for param in allowed_parameters):
        abort(400,
              message="Ensure 'name', 'price' are included in JSON payload")

    for item in items.values():
        if item["name"] == item_data["name"]:
            abort(400,
                  message="Item already exist")

    item = items[item_id]
    item.update(**item_data)

    return jsonify(item), 200


if __name__ == '__main__':
    app.run()
