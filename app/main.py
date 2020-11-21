from flask import Flask, request, Response
from dotenv import load_dotenv, find_dotenv
import pymongo
import os
import json

app = Flask(__name__)
load_dotenv(find_dotenv())


class Endpoint:
	TRUE = {"value": True}
	FALSE = {"value": False}
	
	def __init__(self):
		_KEY = os.getenv("KEY")
		_PASSWORD = os.getenv("PASSWORD")
		_HOST = os.getenv("HOST")
		client = pymongo.MongoClient(f"mongodb+srv://{_KEY}:{_PASSWORD}@{_HOST}/Portfolio?retryWrites=true&w=majority")
		self.db = client["Portfolio"]
		self.contact = self.db["contact"]


portfolio = Endpoint()


@app.route("/contact", methods=["POST"])
def contact_info():
	if request.method == "POST" and request.get_json() is not None:
		user_info = dict(json.loads(request.get_data()))
		if user_info and user_info["name"]:
			result = portfolio.contact.insert_one(user_info)
			if result is not None:
				return Response(status=200, response=json.dumps(portfolio.TRUE))
	return Response(status=406, response=json.dumps(portfolio.FALSE))


if __name__ == '__main__':
	app.run()
