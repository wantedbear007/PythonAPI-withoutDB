from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

items = [
    {"name": "Shampoo", "price": 129}
]


def delete_fun(name):
    global items
    items = list(filter(lambda x: x['name'] == name, items))


class Items(Resource):
    def get(self):
        return items, 200


class Item(Resource):
    def get(self, name):
        # return {'fdf': name}
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item == None:
            return {'Error': 'Item not found'}
        return item, 200

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'Message': 'Item already exist.'}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 200

    def delete(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None) is None:
        #     return {"Message": f"Item doesn't exist {name}"}, 400
        # else:
        #     delete_fun(name)
        #     return {"Message": f"Successfully deleted.{name}"}, 200
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"Message": f"Successfully deleted {name}"}, 200

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help="This field cannot be left blank.")
        data = parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            it = {'name': name, 'price': data['price']}
            items.append(it)
        else:
            item.update(data)
        return item


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

if "__main__" == __name__:
    app.run(debug=True)
