from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


# approach 1: Serializers
class SnippetSerializer2(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, 
                                  allow_blank=True, 
                                  max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, 
                                       default='python')    
    style = serializers.ChoiceField(choices=STYLE_CHOICES, 
                                    default='friendly')
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        ''' Create and return a new `Snippet` instance, given the validated data. '''
        return Snippet.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        ''' Update and return an existing `Snippet` instance, given the validated data.'''
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


# approach 2: ModelSerializers (減少重複的資料)
# Ref: https://www.django-rest-framework.org/tutorial/1-serialization/#creating-a-serializer-class
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner']
