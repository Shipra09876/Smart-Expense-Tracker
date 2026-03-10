from rest_framework import serializers
from .models import *


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','username','name','phone_no','password','password2','tc','dob','occupation','profile_picture','monthly_income','currency']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','user','category_name','is_default']
        read_only_fields = ['user']


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Expense
        fields = ['id', 'title', 'description', 'expense_amount',
                  'expense_date', 'is_recurring', 'recurring_type',
                  'payment_method', 'category_name']

    def create(self, validated_data):
        category_name = validated_data.pop("category_name", None)
        user = self.context["request"].user

        if category_name:
            category, created = Category.objects.get_or_create(
                category_name=category_name, user=user
            )
            validated_data["category"] = category

        return Expense.objects.create(**validated_data)

    def update(self, instance, validated_data):
        category_name = validated_data.pop("category_name", None)
        if category_name:
            category, created = Category.objects.get_or_create(
                category_name=category_name, user=self.context["request"].user
            )
            validated_data["category"] = category

        return super().update(instance, validated_data)



class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'user', 'amount', 'source', 'month', 'year', 'received_on']
        read_only_fields = ['user', 'received_on']
    
    def validate(self, data):
        user = self.context['request'].user
        source = data.get("source")
        month = data.get("month")
        year = data.get("year")

        if Income.objects.filter(user=user, source=source, month=month, year=year).exists():
            raise serializers.ValidationError("Income from this source already exists for this month")

        return data

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     validated_data['user'] = request.user
    #     return super().create(validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Budget
        fields=['id','user','category','budget_amount','month','year']
        read_only_fields = ['user']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wallet
        fields=['user','main_balance','saving_balance']
        read_only_fields=['main_balance','saving_balance']

class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=RecurringExpense
        fields=['user','name','emi_amount','start_date','end_date','active','next_due_date']

    def create(self, validated_data):
            # set next_due_date automatically from start_date if not provided
            if not validated_data.get("next_due_date"):
                validated_data["next_due_date"] = validated_data.get("start_date")
            return super().create(validated_data)

class FDSerializer(serializers.ModelSerializer):
    class Meta:
        model=FD
        fields=['user','name','target_amount','monthly_payment','current_balance','start_date','maturity_date','active']
    
    def create(self, validated_data):
        validated_data["maturity_date"]=validated_data.get("start_date")
        return super().create(validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(write_only=True,required=True)

    class Meta:
        model=Budget
        fields=['user','category','category_name','budget_amount','month','year']
        extra_kwargs = {
            'user': {'read_only': True},        
            'category': {'read_only': True},   
        }

    '''
    Sometimes the frontend (API request) may send category as an object ID (category=3).
    Sometimes it may only send category_name="Food". to resolve this problem 
    '''

    def resolve_category(self,user,category,category_name):
        if category:
            return Category.objects.get(id=category, user=user)
        
        if not category_name:
            return serializers.ValidationError("Provide category or category_ name")
        
        try:
            return Category.objects.get(category_name=category_name,user=user)
        except Category.DoesNotExist:
            return Category.objects.get(category_name=category_name,user__isnull=True)
    
    def create(self, validated_data):
        user=self.context["request"].user
        category=validated_data.pop('category',None)
        category_name=validated_data.pop("category_name",None)

        category=self.resolve_category(user,category,category_name)
        
        obj,created=Budget.objects.update_or_create(
            user=user,
            category=category,
            month=validated_data["month"],
            year=validated_data["year"],
            defaults={
                'budget_amount':validated_data["budget_amount"]
            }
        )
        return obj
    
    def update(self, instance, validated_data):
        user=self.context["request"].user
        category=validated_data.pop("category",None)
        category_name=validated_data.pop("category_name",None)

        if category or category_name:
            instance.category=self.resolve_category(user,category,category_name)

        for f in ("budget_amount","month","year"):
            if f in validated_data:
                setattr(instance,f,validated_data[f])

        instance.save()
        return instance
    

        