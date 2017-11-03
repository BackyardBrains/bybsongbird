import MySQLdb
import MySQLdb.cursors
import config

def connect_to_database():
  options = {
    'host': config.env['host'],
    'user': config.env['user'],
    'passwd': config.env['password'],
    'db': config.env['db'],
    'cursorclass' : MySQLdb.cursors.DictCursor
  }
  db = MySQLdb.connect(**options)
  db.autocommit(True)
  return db

def isStrLengthLessThanN(str, length):
  if len(str) <= length:
      return True
  else: 
      return False

def get_name_mat():
  name_list = []
  with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
      json_decode = json.load(inputFile)
      for item in json_decode:
          name_list.append(item.get('name'))

  name_vectorizer = TfidfVectorizer(min_df=1)
  name_mat = name_vectorizer.fit_transform(name_list).toarray()
  return name_mat

def get_address_mat():
  address_list = []
  with open('business_LV.json', 'r') as inputFile:
      json_decode = json.load(inputFile)
      for item in json_decode:
          address_list.append(item.get('address'))

  address_vectorizer = TfidfVectorizer(min_df=1)
  address_mat = address_vectorizer.fit_transform(address_list).toarray()
  return address_mat
