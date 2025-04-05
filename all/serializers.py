from rest_framework import serializers
from .models import Object, Apartment, User, ExpenseType, Supplier, Expense, Payment, Document, UserPayment, SupplierPayment

class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'

class ApartmentSerializer(serializers.ModelSerializer):
    object_name = serializers.CharField(source='object.name', read_only=True)

    class Meta:
        model = Apartment
        fields = [
            'id', 'object', 'object_name', 'room_number', 'rooms', 'area', 'floor',
            'price', 'status', 'description', 'secret_code', 'reserved_until', 'reservation_amount', 'total_payments'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'fio', 'address', 'phone_number', 'object_id', 'apartment_id',
            'user_type', 'telegram_chat_id', 'balance', 'kafil_fio', 'kafil_address',
            'kafil_phone_number', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    balance_details = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ['id', 'company_name', 'contact_person_name', 'phone_number', 'address', 'description', 'balance', 'balance_details']

    def get_balance_details(self, obj):
        return obj.get_balance_details()

class ExpenseSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)
    expense_type_name = serializers.CharField(source='expense_type.name', read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'date', 'supplier', 'supplier_name', 'comment', 'expense_type',
            'expense_type_name', 'object', 'status'
        ]

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'payment', 'document_type', 'docx_file', 'pdf_file', 'image', 'created_at']

class PaymentSerializer(serializers.ModelSerializer):
    user_fio = serializers.CharField(source='user.fio', read_only=True)
    apartment_info = serializers.CharField(source='apartment.__str__', read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_fio', 'apartment', 'apartment_info', 'payment_type', 'total_amount',
            'initial_payment', 'interest_rate', 'duration_months', 'monthly_payment', 'due_date',
            'paid_amount', 'status', 'additional_info', 'created_at', 'documents', 'reservation_deadline'
        ]

class UserPaymentSerializer(serializers.ModelSerializer):
    user_fio = serializers.CharField(source='user.fio', read_only=True)

    class Meta:
        model = UserPayment
        fields = ['id', 'user', 'user_fio', 'amount', 'payment_type', 'date', 'description']

class SupplierPaymentSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.company_name', read_only=True)

    class Meta:
        model = SupplierPayment
        fields = ['id', 'supplier', 'supplier_name', 'amount', 'payment_type', 'date', 'description']