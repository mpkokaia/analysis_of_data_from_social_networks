from urllib import urlopen
import json
from pymongo import Connection
import sys


class APIWorker(object):
    def __init__(self, usr_id, access_token, db):
        self.access_token = access_token
        self.users_get_url = "https://api.vk.com/method/users.get?v=5.5&user_ids="
        self.friends_get_url = "https://api.vk.com/method/friends.get?user_id="
        self.users_get_fields = "&fields=sex,education,universities,schools,personal,connections,interests"
        self.friends_get_fields = "&fields=nickname,education,universities"
        self.usr_id = str(usr_id)
        self.db = db
        self.create_record()

    def users_get(self):
        data = urlopen(self.users_get_url + self.usr_id + self.users_get_fields + self.access_token)
        obj = json.load(data)
        if obj['response'][0]['first_name'] == u'DELETED':
            return False
        return obj['response'][0]

    def friends_get(self):
        data = urlopen(self.friends_get_url + self.usr_id + self.friends_get_fields + self.access_token)
        obj = json.load(data)
        if u'error' in obj:
            return False
        return obj['response']

    def create_record(self):
        record = {}
        try:
            record['vkid'] = self.usr_id
            user = self.users_get()
            if user == False:
                return True
            record['users_get'] = user
            record['friends_get'] = self.friends_get()
        except IOError:
            sys.exit()
        self.db.students.save(record)
        return True


connection = Connection()
db = connection.urfu

access_token = "&access_token=bae62b9c62a99fe2cd04ca0bdf0d68c3f55192c93d7979e9cde1eea3bb6a45a3decbf52dd1f3d6881468d"
url = "https://api.vk.com/method/users.search?v=5.5&university=477"
foffset = "&offset="
university_year = "&university_year="
fsex = "&sex="
year = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
sex = [1, 2]
offset = 0
for s in sex:
    for y in year:
        offset = 0
        for i in range(0, 1000, 20):
            try:
                data = urlopen(url + university_year + str(y) + fsex +
                               str(s) + foffset + str(offset) + access_token)
            except IOError:
                sys.exit()
            obj = json.load(data)
            for item in obj['response']['items']:
                usr_id = item['id']
                APIWorker(usr_id, access_token, db)
            offset = i
