from rest_framework import serializers
class LockerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    key = serializers.CharField(max_length=100)
    status = serializers.BooleanField()
    user = serializers.CharField()

    def create(self, validated_data):
        return Locker.objects.create(**validated_data)
    
    # def __str__(self):
    #     return self.name