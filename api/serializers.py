from rest_framework import serializers
from .models import Person
from datetime import date


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'iin', 'age')

    def create(self, validated_data):
        person = Person.objects.create(iin=validated_data['iin'])

        def get_age(iin):
            dat = int("".join(map(str, iin[:2])))
            by = 2000 + dat if int(iin[6]) in (5, 6) else 1900 + dat
            bm = int("".join(map(str, iin[2:4])))
            bd = int("".join(map(str, iin[4:6])))
            today = date.today()
            return today.year - by - ((today.month, today.day) < (bm, bd))
        person.age = get_age(validated_data['iin'])
        person.save()
        return person


