from flask import Flask, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://172.105.45.40:9200")

@app.route("/")
def health_check():
    return "OK"

@app.route("/city", methods=["POST"])
def add_or_update_city():
    city = request.get_json("city")
    population = request.get_json("population")

    es.index(index="cities", id=city, body={"population": population})

    return "City added or updated"

@app.route("/city/<city_name>")
def get_city_population(city_name):
    result = es.get(index="cities", id=city_name)
    population = result["_source"]["population"]

    return str(population)

if __name__ == "__main__":
    app.run()
