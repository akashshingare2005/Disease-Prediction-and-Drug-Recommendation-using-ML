from pymongo import MongoClient

client = MongoClient("mongodb+srv://akkki_217:Akash217@cluster0.6rovofz.mongodb.net/BookShelfDB?retryWrites=true&w=majority&appName=Cluster0")

db = client["disease_prediction"]

drug_collection = db["drugs"]
history_collection = db["history"]
