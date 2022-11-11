from Application import app
from Application.constants import username, password
import pymongo


DB_URI = "mongodb+srv://{}:{}@customercareregistrydb.4ubajvz.mongodb.net/?retryWrites=true&w=majority".format(username, password)
client = pymongo.MongoClient(DB_URI)
db = client.users
