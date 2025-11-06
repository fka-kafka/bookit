from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname', 'role',
                  'password', 'password_confirm', 'date_created']
        read_only_fields = ['id', 'date_created']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def validate_role(self, value):
        """Ensure role is either 'organizer' or 'attendee'"""
        if value not in ['organizer', 'attendee']:
            raise serializers.ValidationError(
                "Invalid role. Choose 'organizer' or 'attendee'.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        username = validated_data.get('email')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            role=validated_data.get('role', 'attendee')
        )

        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname',
                  'role', 'full_name', 'date_created']
        read_only_fields = ['id', 'date_created']
