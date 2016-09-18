from firebase import firebase
import requests

fireBase = firebase.FirebaseApplication('https://sail-857f9.firebaseio.com/', None)
result = fireBase.get('', None)


class trains():
    def __init__(self, result):
        self.result = fireBase.get('', None)

    def makeUser(self, user_name, **kwargs):
        url = 'http://localhost:8080/add_user/'
        creds = '?user_name=trial&password=karikanda4&format=json'
        r = requests.post(url + creds, data={"api_key": "blah", "password": "blah", "user_name": kwargs['packageName']})
        print r
        print r.text

    def makeTable(self, user_name, **kwargs):
        """
        creates a table
        :param user_name:
        :param kwargs: table_name
        :return: Boolean
        """
        url = 'http://localhost:8080/ManageTables/'
        creds = '?password=blah&format=json&user_name=' + str(user_name) + '&json={"table_name":""}'
        r = requests.post(url + creds, data={"table_name": kwargs['table_name']})
        print r
        #print r.text

    def deleteTable(self, user_name, **kwargs):
        """
        Deletes the table
        :param user_name:
        :param kwargs: table_name
        :return:
        """

        url = 'http://localhost:8080/ManageTables/'
        creds = '?password=blah&format=json&user_name=' + str(user_name) + '&json={"table_name":"' + kwargs[
            'table_name'] + '"}'
        r = requests.delete(url + creds)
        print r
        print r.text

    def TrainOne(self, packageName):
        """

        trains the ai for the given application
        :param : name of package
        :return: bool

        """

        # Create user if there is no user
        self.makeUser(packageName, **{"packageName": packageName})

        # Traverse through the table to reach the data needed.
        self.bucket = self.result['packages'][packageName]['bucket']
        self.result = self.result['packages'][packageName]['activities']

        for i in self.result:
            # Delete entire table to prevent residencies.
            self.deleteTable(packageName, **{"table_name": i})

            # Create new table.
            self.makeTable(packageName, **{"table_name": i})

            # now we populate the table
            try:
                self.poulateTable(packageName,self.result[i]['views'], **{"table_name": i})
            except Exception as e:
                print e
                print 'no view'

        self.deleteTable(packageName, **{"table_name": "univ"})
        for i in self.bucket:
            self.makeTable(packageName,**{"table_name":"univ"})
            for j in self.bucket[i]:
                payload = {"tag":i,"message":self.bucket[i][j],"reply":"blah","table":"univ"}
                url = 'http://localhost:8080/snippets/'
                creds = '?password=blah&format=json&user_name=' + str(packageName) + '&json={"table_name":"univ"}'
                r = requests.post(url + creds, data=payload)
                print payload
                print r
            self.trainTable(packageName, **{"table_name": "univ"})
    def poulateTable(self, user_name, members, **kwargs):
        """
        method to add data into the table
            :param packageName:
        :param members:
        :param param:
        :return:
        """
        for i in members:
            for j in self.bucket[i]:
                print self.bucket
                payload =  {"tag":i,"message":self.bucket[i][j],"reply":members[i]['hint'],"table":kwargs['table_name']}
                url = 'http://localhost:8080/snippets/'
                print 'hi'
                creds = '?password=blah&format=json&user_name=' + str(user_name) + '&json={"table_name":"' + kwargs['table_name'] + '"}'
                r = requests.post(url + creds, data=payload)
                print payload
                print r
            self.trainTable(user_name,**{"table_name":kwargs['table_name']})

    def trainTable(self,user_name,**kwargs):
        """
        makes api call to train the table
        :param user_name:
        :param kwargs:
        :return:
        """
        url = 'http://localhost:8080/train/'
        creds = '?password=blah&format=json&user_name=' + str(user_name) + '&json={"table_name":"' + kwargs[
            'table_name'] + '"}'
        r = requests.get(url+creds)
        print r

