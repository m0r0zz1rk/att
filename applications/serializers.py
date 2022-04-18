from rest_framework import fields, serializers
from .models import *


class TypeOoSerializer(serializers.ModelSerializer):
    class Meta:
        model = type_oo
        fields = ('name',)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('name_pos', 'type_pos')


class MunobrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Munobr
        fields = ('name_mo', 'type_mo')


class AttformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attform
        fields = ('name',)


class AttcategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('type_cat', )


class OoSerializer(serializers.ModelSerializer):
    mo = serializers.SlugRelatedField(slug_field='name_mo', read_only=True)
    type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Oo
        fields = '__all__'