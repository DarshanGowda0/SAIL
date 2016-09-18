from django.shortcuts import render
import json
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from suggest_faq.models import Tables, messages, Users, SuperUsers, tags, RightPredictions, WrongPredictions
from suggest_faq.serializers import UserSerializer, AddMessageSerializer, AddTagSerializer, getJSON, TableSerializer, AddCorrectTagSerializer
#, AddWrongTagSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from suggest_faq.imports.vectorizers import *
import pickle
import requests
#from suggest_faq.serializers import SnippetSerializer, SuggestionSerializer


'''
1.  Add | Remove | view : Users  & change password : Users

    model:  Users
    params: owner(SuperUsers), user_name, password, api_key
'''

class AddUser(APIView):
    """
    Add | Remove | view : Users  & change password : Users
    """
    def valudate(self,params):

        '''
        checking the validation details of the SuperUsers
        '''

        snippets = SuperUsers.objects.all().filter(user_name=params['user_name'])
        if snippets[0].password == params['password']:
            self.owner = snippets[0]
            return True
        else:
            return False

    def get(self, request,format=None):
        if(self.valudate(request.query_params)):
            '''
            GET a lit of all the users who are under the current SuperUser
            '''

            users = Users.objects.all().filter(owner=self.owner)
            serializer = UserSerializer(users,many=True, data=request.data)

            if serializer.is_valid():
                return Response(serializer.data)

            return Response(serializer.data)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        '''
        Add new user
        '''
        if(self.valudate(request.query_params)):
            serializer = UserSerializer(data=request.data)
            serializer.more(self.owner)
            if serializer.is_valid():
                if Users.objects.all().filter(user_name=serializer.validated_data['user_name']):
                    return Response({"error":"data exists"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)



            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,format=None):
        '''
        change password or api_key of the current user by the SuperUser
        '''
        if(self.valudate(request.query_params)):
            print request.data['user_name']
            snippet = Users.objects.all().filter(user_name=request.data['user_name'])
            try:
                serializer = UserSerializer(snippet[0], data=request.data)
            except Exception as e:
                return Response('invalid user_name',status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request,format=None):
        '''
        delete a user
        '''
        if(self.valudate(request.query_params)):
            # Every request contains a json object to obtain additional information
            j = json.loads(request.query_params['json'])
            snippets = Users.objects.all().filter(user_name=j['user_name'])
            for i in snippets:
                i.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

'''
2.  Add | Remove | view : Models

    model: Tables
    params: table_name, owner(Users)
'''
class ManageTables(APIView):
    """
    Add | Remove | view : Models
    """
    def valudate(self,params):
        '''
        checking the validation details of the Users
        '''
        snippets = Users.objects.all().filter(user_name=params['user_name'])
        if snippets[0].password == params['password']:
            self.owner = snippets[0]
            return True
        else:
            return False

    def get(self, request,format=None):
        if(self.valudate(request.query_params)):
            '''
            GET a lit of all the tables who are under the current User
            '''

            users = Tables.objects.all().filter(owner=self.owner)
            serializer = TableSerializer(users,many=True, data=request.data)

            if serializer.is_valid():
                return Response(serializer.data)

            return Response(serializer.data)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        '''
        Add new table
        '''
        if(self.valudate(request.query_params)):
            serializer = TableSerializer(data=request.data)
            serializer.more(self.owner)
            if serializer.is_valid():
                if Tables.objects.all().filter(table_name=serializer.validated_data['table_name']).filter(owner=self.owner):
                    return Response({"error":"table already exists"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,format=None):
        '''
        delete a table
        '''
        if(self.valudate(request.query_params)):
            # Every request contains a json object to obtain additional information
            j = json.loads(request.query_params['json'])
            
            snippets = Tables.objects.all().filter(table_name=j['table_name'])
            for i in snippets:
                i.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

'''
3.  View | Add | delete messages

    model:  messages
    params: table, tag, message
'''

class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404
    # VALIDATING THE USERS
    def valudate(self,params):
        snippets = Users.objects.all().filter(user_name=params['user_name'])
        if snippets[0].password == params['password']:
            self.owner = snippets[0]
            return True
        else:
            return False
    def GetTableName(self, table_name):
        '''
        We then obtain a list of all the tables that have been created
        by the current user, to check if the data being queried is
        created by the same person
        '''

        table_object_list = Tables.objects.all().filter(owner=self.owner)

        '''
        We now need to convert this list of object of all the tables
        to a list of table names
        '''

        table_list = [i.table_name for i in table_object_list]

        '''
        Find the required table of exit with a bad request
        '''

        if table_name in table_list:
            self.table = table_object_list[table_list.index(table_name)]
            return self.table
        else:
            return Response('invalid table name',status=status.HTTP_400_BAD_REQUEST)

    # GETS ALL THE MESSAGES OF THE GIVEN MODEL:
    def get(self, request, format=None):

        # FIRST CHECKING IF YOUR AUTHERIZATION IS VALID
        if(self.valudate(request.query_params)):

            # Every request contains a json object to obtain additional information

            data = request.query_params['json']     # load the json and
                                                    # parse
            ser = getJSON(data=json.loads(data))    # Serialize the json
            if ser.is_valid():
                user_data = ser.data

            '''
            We then obtain a list of all the tables that have been created
            by the current user, to check if the data being queried is
            created by the same person
            '''

            table_object_list = Tables.objects.all().filter(owner=self.owner)

            '''
            We now need to convert this list of object of all the tables
            to a list of table names
            '''

            table_list = [i.table_name for i in table_object_list]

            '''
            Find the required table of exit with a bad request
            '''

            if user_data['table_name'] in table_list:
                self.table = table_object_list[table_list.index(user_data['table_name'])]
            else:
                return Response('invalid table name',status=status.HTTP_400_BAD_REQUEST)

            '''
            Now that we have all the parameters that we need,
            we can go ahead and print the data in the required table
            '''

            snippets = messages.objects.all().filter(table=self.table)
            serializer = AddMessageSerializer(snippets, many=True, data=request.data)

            if serializer.is_valid():
	            return Response(serializer.data)

        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)



    # INSERT THE MESSAGE INTO THE SPECIFIED MODEL:

    def post(self, request, format=None):
        if(self.valudate(request.query_params)):
            serializer = AddMessageSerializer(data=request.data)
            serializer2 = AddTagSerializer(data=request.data)
            if serializer2.is_valid():
                serializer2.more(self.owner)
                serializer2.save()
            else:
                self.GetTableName(request.data['table'])
                all_replies = tags.objects.all().filter(tag=request.data['tag']).filter(table=self.table)
                try:
                    useless_temp = all_replies[0]
                except Exception as e:
                    print e
                    return Response('Incorrect tag or tag does not exist', status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.more(self.owner)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

    # DELETES ALL MESSAGES IN THE CURRENT MODEL

    def delete(self, request, format=None):
        if(self.valudate(request.query_params)):
            # Every request contains a json object to obtain additional information

            data = request.query_params['json']     # load the json and
                                                    # parse
            ser = getJSON(data=json.loads(data))    # Serialize the json
            if ser.is_valid():
                user_data = ser.data

            '''
            We then obtain a list of all the tables that have been created
            by the current user, to check if the data being queried is
            created by the same person
            '''

            table_object_list = Tables.objects.all().filter(owner=self.owner)

            '''
            We now need to convert this list of object of all the tables
            to a list of table names
            '''

            table_list = [i.table_name for i in table_object_list]

            '''
            Find the required table of exit with a bad request
            '''

            if user_data['table_name'] in table_list:
                self.table = table_object_list[table_list.index(user_data['table_name'])]
            else:
                return Response('invalid table name',status=status.HTTP_400_BAD_REQUEST)

            '''
            Now that we have all the parameters that we need,
            we can go ahead and print the data in the required table
            '''

            snippets = messages.objects.all().filter(table=self.table)

            for i in snippets:
                i.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)


'''
4.  Predict and POST the result of the prediction

    model:  RightPredictions
    params: tag, message, table
'''

class Predict(APIView):
    """
    Predict and POST the result of the prediction
    """
    def valudate(self,params):

        '''
        checking the validation details of the SuperUsers
        '''

        snippets = Users.objects.all().filter(user_name=params['user_name'])
        if snippets[0].password == params['password']:
            self.owner = snippets[0]
            return True
        else:
            return False
    def GetTableName(self, table_name):
        '''
        We then obtain a list of all the tables that have been created
        by the current user, to check if the data being queried is
        created by the same person
        '''

        table_object_list = Tables.objects.all().filter(owner=self.owner)

        '''
        We now need to convert this list of object of all the tables
        to a list of table names
        '''

        table_list = [i.table_name for i in table_object_list]

        '''
        Find the required table of exit with a bad request
        '''

        if table_name in table_list:
            self.table = table_object_list[table_list.index(table_name)]
            return self.table
        else:
            return Response('invalid table name',status=status.HTTP_400_BAD_REQUEST)

    def get(self, request,format=None):
        short_code_to_data = {'computer': 'A computer technician will do the job.</br>may I suggest Mr. Ravi?</br>Here is his phone number: 8892878337', 'yoga': 'Sounds like you need a Yoga guru.</br>may I suggest Mr. Pathanjali?</br>Here is his phone number: 8892878337', 'paint': 'Would you like us to suggest a painter?</br>may I suggest Mr. Gunda?</br>Here is his phone number: 8892878337','hey':'Hello!</br> I am watawata.</br> Tell me what the problem is.','bye':'It was nice talking to you.</br>If you need me, you know where to find me.','confirm':'would you like me to confirm this order?','clean':'I will send someone to clean your house for you.</br>How about Mr. Ram?</br>Here is his phone number: 8892878337','price':'He charges Rs.300 for this job.','thankyou':'You don\'t have to thank me. It\'s all cool','house_app':'A House Appliance technician will fix it up for you.</br>may I suggest Mr. Nagesh?</br>Here is his phone number: 8892878337','plumb':'Would you like to book a Plumber?</br>may I suggest Mr. Rajesh?</br>Here is his phone number: 8892878337','electric':'You can hire an electrician to solve this.</br>may I suggest Mr. Tony?</br>Here is his phone number: 8892878337','carpy':'Does hiring a carpenter solve your problem?</br>may I suggest Mr. Manjunath?</br>Here is his phone number: 8892878337','cools':'Can we suggest someone who is an expert in refrigeration repairs?</br>may I suggest Mr. Divaker?</br>Here is his phone number: 8892878337'};
        if(self.valudate(request.query_params)):
            '''
            GET a prediction for the current request
            '''
            table = self.GetTableName(json.loads(request.query_params['json'])['table_name'])
            all_entries = tags.objects.all().filter(table=table)
            for i in all_entries:
                short_code_to_data[i.tag] = i.reply
            try:
                #predictors = request.session['predictors']
                #predictors.vectors = request.session['vectors']
                shortcode = predictors.predict(json.loads(request.query_params['json'])['message'])
            except Exception as e:
                predictors = pickle.load(open('./pickles/'+request.query_params['user_name']+'_'+json.loads(request.query_params['json'])['table_name'], "rb" ) )
                shortcode,accurecy,lists =  predictors.predict(json.loads(request.query_params['json'])['message'])
                x = {"shortcode":shortcode,"message":short_code_to_data[shortcode],"accurecy":str(accurecy),"lists":json.dumps(lists)}
            return Response(JSONRenderer().render(x), status=status.HTTP_201_CREATED)

        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        '''
        Add new user
        '''
        if(self.valudate(request.query_params)):
            serializer = AddCorrectTagSerializer(data=request.data)
            serializer.more(self.owner)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

'''
5.  BOT training and its version control(coming soon)

    model:  messages
    params: tag, message, table
'''

class Train(APIView):
    """
    BOT training and its version control(coming soon)
    """
    def valudate(self,params):
        '''
        checking the validation details of the SuperUsers
        '''
        snippets = Users.objects.all().filter(user_name=params['user_name'])
        if snippets[0].password == params['password']:
            self.owner = snippets[0]
            return True
        else:
            return False
    def GetTableName(self, table_name):
        '''
        We then obtain a list of all the tables that have been created
        by the current user, to check if the data being queried is
        created by the same person
        '''

        table_object_list = Tables.objects.all().filter(owner=self.owner)

        '''
        We now need to convert this list of object of all the tables
        to a list of table names
        '''

        table_list = [i.table_name for i in table_object_list]

        '''
        Find the required table of exit with a bad request
        '''

        if table_name in table_list:
            self.table = table_object_list[table_list.index(table_name)]
            return self.table
        else:
            return Response('invalid table name',status=status.HTTP_400_BAD_REQUEST)

    def get(self, request,format=None):
        if(self.valudate(request.query_params)):
            '''
            GET a prediction for the current request
            '''
            table = self.GetTableName(json.loads(request.query_params['json'])['table_name'])
            predictors= predictions()
            x = [[[[u'save', 0]], []]]
            all_entries = messages.objects.all().filter(table=table)
            X = []
            y = []
            for i in all_entries:
                X.append(i.message)
                y.append(i.tag)
            xy_list = {}
            xy_list['x'] = X
            xy_list['y'] = y
            predictors.learn_from_db(x,xy_list)
            pickle.dump(predictors, open('./pickles/'+request.query_params['user_name']+'_'+json.loads(request.query_params['json'])['table_name'], "wb" ) )
            #request.session['predictors'] = predictors
            #request.session['vectors'] = predictors.vectors
            return Response('success', status=status.HTTP_201_CREATED)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        '''
        Add new user
        '''
        if(self.valudate(request.query_params)):
            serializer = UserSerializer(data=request.data)
            serializer.more(self.owner)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('authentication failed',status=status.HTTP_400_BAD_REQUEST)
