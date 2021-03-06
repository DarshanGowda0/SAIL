from rest_framework import serializers
from suggest_faq.models import Tables, Users, messages, RightPredictions, WrongPredictions
from suggest_faq.models import Tables, messages, Users, tags
# SERIALIZER FOR USER AUTH needed


# SE RIALIZER FOR MANIPULATION OF USERS XD

class UserSerializer(serializers.Serializer):
    # these are the stuff you pick up/ dump
    pk = serializers.IntegerField(read_only=True)
    api_key = serializers.CharField(required=True, allow_blank=True, max_length=100)
    user_name = serializers.CharField(required=True, allow_blank=True, max_length=100)
    password = serializers.CharField(style={'base_template': 'textarea.html'})

    def more(self,owner_name_from_views):
        self.owner = owner_name_from_views

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print validated_data
        validated_data['owner'] = self.owner

        return Users.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        print instance
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

#USED TO GET THEM JSON TO MEAN SOMETHING

class getJSON(serializers.Serializer):
    # these are the stuff you pick up/ dump
    pk = serializers.IntegerField(read_only=True)
    table_name = serializers.CharField(required=True, allow_blank=True, max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """

        return Users.objects.create(**validated_data)


    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.table_name = validated_data.get('user_name', instance.user_name)

        return instance

'''
Serialize Table data
'''
class TableSerializer(serializers.Serializer):
    # these are the stuff you pick up/ dump
    pk = serializers.IntegerField(read_only=True)
    table_name = serializers.CharField(required=True, allow_blank=True, max_length=100)

    def more(self,owner_name_from_views):
        self.owner = owner_name_from_views

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        validated_data['owner'] = self.owner
        return Tables.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        print instance
        instance.table_name = validated_data.get('table_name', instance.password)
        instance.save()
        return instance
# SERIALIZER FOR MESSAGES MANAGEMENT

class AddMessageSerializer(serializers.Serializer):
    def more(self,blah):
        self.owner = blah

    # these are the stuff you pick up/ dump
    pk = serializers.IntegerField(read_only=True)
    tag = serializers.CharField(required=True, allow_blank=True, max_length=100)
    message = serializers.CharField(style={'base_template': 'textarea.html'})
    table = serializers.CharField(required=True, allow_blank=True, max_length=100)

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
        else:
            return Response('invalid table name',status=status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        self.GetTableName(validated_data['table'])
        validated_data['table'] = self.table
        return messages.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.table = 5
        instance.message = 'her'
        instance.tag = validated_data.get('tag', instance.tag)
        instance.save()
        return instance

class AddTagSerializer(serializers.Serializer):
    def more(self,blah):
        self.owner = blah

    # these are the stuff you pick up/ dump
    pk = serializers.IntegerField(read_only=True)
    tag = serializers.CharField(required=True, allow_blank=True, max_length=100)
    reply = serializers.CharField(style={'base_template': 'textarea.html'})
    table = serializers.CharField(required=True, allow_blank=True, max_length=100)

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
        else:
            return Response('invalid table name',status=status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        self.GetTableName(validated_data['table'])
        validated_data['table'] = self.table
        return tags.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.table = 5
        instance.message = 'her'
        instance.tag = validated_data.get('tag', instance.tag)
        instance.save()
        return instance

# SERIALIZER FOR MESSAGES MANAGEMENT

class AddCorrectTagSerializer(serializers.Serializer):
    def more(self,blah):
        self.owner = blah

    # these are the stuff you pick up/ dump
    pk = serializers.IntegerField(read_only=True)
    tag = serializers.CharField(required=True, allow_blank=True, max_length=100)
    message = serializers.CharField(style={'base_template': 'textarea.html'})
    table = serializers.CharField(required=True, allow_blank=True, max_length=100)

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
        else:
            return Response('invalid table name',status=status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print "getting here"
        self.GetTableName(validated_data['table'])
        validated_data['table'] = self.table
        return RightPredictions.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.table = 5
        instance.message = 'her'
        instance.tag = validated_data.get('tag', instance.tag)
        instance.save()
        return instance


















class SuggestionSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

class SnippetSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)

    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
