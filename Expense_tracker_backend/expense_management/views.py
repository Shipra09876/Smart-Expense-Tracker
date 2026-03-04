from django.shortcuts import render
from .models import *
from user_management.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from expense_management.serializers import *
import logging
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
import uuid
from expense_management.Utils.wallet_utils import *
from decimal import Decimal
from .filters import ExpenseFilter, BudgetFilter
from datetime import date,datetime
from expense_management.Utils.budget_utils import *

#---------- Income --------------------------------------

class AddIncome(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]
    def post(self,request):
        data=request.data.copy()
        data['user'] = request.user.id
        serializer=IncomeSerializer(data=request.data.copy())
        if serializer.is_valid():
            income=serializer.save(user=request.user)
            
            # update wallet
            SpilitIncome(request.user,income.amount)

            return Response({
            "msg":"Income added successfully and wallet updated successfully"
            },status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class EditIncome(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]
    def put(self,request,pk):
        try:
            income_obj = get_object_or_404(Income, pk=pk, user=request.user)
        except Income.DoesNotExist:
            return Response({"error": "Income not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer=IncomeSerializer(instance=income_obj, data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg":"Information edit successfully"
            },status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
class ViewIncome(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request):
        incomes=Income.objects.filter(user=request.user)
        serializer=IncomeSerializer(incomes,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class ViewIncomeById(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request,pk):
        try:
            income=Income.objects.get(pk=pk,user=request.user)
            serializer=IncomeSerializer(income)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Income.DoesNotExist:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


# ----------Wallet View------------------------------
class GetWalletBalance(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request):
        wallet=get_wallet(request.user)
        return Response({
            "Main Wallet":wallet.main_balance,
            "Saving Wallet":wallet.saving_balance
        },status=status.HTTP_200_OK)

class TransferMoneyToSaving(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def post(self,request):
        amount=Decimal(str(request.data.get("amount",0)))
        wallet=get_wallet(request.user)

        if wallet.main_balance>=amount:
            wallet.main_balance-=amount
            wallet.saving_balance+=amount
            wallet.save()
        
            return Response({
                "Msg":f"{amount} Transfer Money To Saving Wallet Successfully"
            },status=status.HTTP_200_OK)
    
        return Response({
            "Msg":"Money not transferred"
        },status=status.HTTP_404_NOT_FOUND)

class WithdrawSaving(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def post(self,request):
        amount=Decimal(str(request.data.get("amount",0)))
        wallet=get_wallet(request.user)

        if wallet.saving_balance>amount:
            wallet.saving_balance-=amount
            wallet.main_balance+=amount
            wallet.save()
        
            return Response({
                "msg":f"{amount} Transferred Money To Main Wallet Successfully"
            },status=status.HTTP_200_OK)
        
        return Response({
            "msg":f"Money Transferrer unsuccesfull"
        },status=status.HTTP_404_NOT_FOUND)
    


#----------------------Categories---------------------------------

class CategoryListCreate(APIView):
    permissions_classes=[IsAuthenticated]
    render_classes=[JSONRenderer]

    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,is_default=False)
            return Response({
                "Msg":"Category create successfully"
            },status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request):
        category = Category.objects.filter(models.Q(user=request.user) | models.Q(user__isnull=True))
        print(category)

        serializer=CategorySerializer(category,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
# ----------------- Expenses -------------------------------------

class AddExpense(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def post(self, request):
        # 1. Parse request data
        title = request.data.get("title")
        expense_amount = request.data.get("expense_amount")
        category = request.data.get("category")        # can be id
        category_name = request.data.get("category_name")  # can be name
        expense_date_str = request.data.get("expense_date")

        if not expense_date_str:
            return Response({"error": "expense_date is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            expense_date = datetime.strptime(expense_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid expense_date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        year = expense_date.year
        month = expense_date.month

        # 2. Use BudgetSerializer.resolve_category to resolve category
        budget_serializer = BudgetSerializer(context={"request": request})
        try:
            category_obj = budget_serializer.resolve_category(request.user, category, category_name)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Check budget before adding
        check = check_budget_before_adding(request.user, category_obj, year, month, Decimal(expense_amount))

        # ⚠️ Yahan pe reject mat karo, sirf alert ke liye store karo
        alert_info = None
        if check.get("reason") == "Over Budget":
            alert_info = {"level": "danger", "message": "You have exceeded your budget for this category!"}
        elif check.get("reason") == "Near limit":
            alert_info = {"level": "warning", "message": "You are nearing your budget limit!"}


        # 4. Deduct from wallet
        wallet = DeductFromWallet(request.user, float(expense_amount))

        # 5. Save expense via serializer
        serializer = ExpenseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            expense = serializer.save(user=request.user, category=category_obj)

            # 6. Get updated budget info
            budget_info = remaining_budget(request.user, category_obj, year, month)

            return Response({
                "msg": "Expense added",
                "expense": serializer.data,
                "wallet": {
                    "main": str(wallet.main_balance),
                    "saving": str(wallet.saving_balance)
                },
                "budget": budget_info,
                "alert": alert_info 
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditExpense(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def put(self, request, uid):
        try:
            expense_obj = Expense.objects.get(id=uid, user=request.user)
        except Expense.DoesNotExist:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExpenseSerializer(
            instance=expense_obj,
            data=request.data,
            context={'request': request}, 
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Edit Expense successfully"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetExpense(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]
    def get(self,request):
        querySet = Expense.objects.filter(user=request.user)
        filterSet=ExpenseFilter(request.GET,queryset=querySet)
        
        if not filterSet.is_valid():
            return Response(filterSet.errors, status=400)

        expenses = filterSet.qs
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class DeleteExpense(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]
    def delete(self,request,uid):
        try:
            expense = get_object_or_404(Expense, id=uid, user=request.user)
            expense.delete()
            return Response({"msg": "Deleted Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# --------------- EMI -------------------------
class AddRecurringExpense(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def post(self,request):
        serializer=RecurringExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "msg":"Add Recurring expense successfully",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# return all expenses of logged-in-user
class GetRecurringExpense(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request):
        expense=RecurringExpense.objects.filter(user=request.user)
        serializer=RecurringExpenseSerializer(expense,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class RecurringExpenseById(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

# return only 1 expenses of logged-in-user by id
    def get(self,request,pk):
        expense=RecurringExpense.objects.get(user=request.user,pk=pk)
        if not expense:
            return Response({
                "Error":"Not Found"
            },status=status.HTTP_404_NOT_FOUND)

        serializer=RecurringExpenseSerializer(expense)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        try:
            expense=RecurringExpense.objects.get(pk=pk,user=request.user)
        except RecurringExpense.DoesNotExist:
            return Response({
                "Msg":"expense does not exist"
            },status=status.HTTP_404_NOT_FOUND)
        
        serializer=RecurringExpenseSerializer(instance=expense,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        expense=RecurringExpense.objects.filter(pk=pk,user=request.user)
        if not expense:
            return Response({
                "msg":"Expense not found"
            },status=status.HTTP_404_NOT_FOUND)

        expense.delete()
        return Response({
            "msg":"expense deleted successfully"
        },status=status.HTTP_204_NO_CONTENT)

# -------FD's API-----------------------------------
class AddGoal(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def post(self,request):
        serializer=FDSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class GetGaol(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request):
        goal=FD.objects.filter(user=request.user)
        serializer=FDSerializer(goal,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class GetGoalByID(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request,pk):
        goal=FD.objects.get(user=request.user,pk=pk)
        if not goal:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=FDSerializer(goal)
        return Response(serializer.data,status=status.HTTP_200_OK)
     

    def put(self, request, pk):
        goal = FD.objects.get(user=request.user,pk=pk)
        if not goal:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FDSerializer(instance=goal, data=request.data, partial=True)
        if serializer.is_valid():
            goal = serializer.save(user=request.user)
            # Check completion
            if goal.current_balance >= goal.target_amount:
                goal.active = False
                goal.save()
            return Response(FDSerializer(goal).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request,pk):
        goal=FD.objects.filter(user=request.user,pk=pk)
        if not goal:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        goal.delete()
        return Response({
            "msg":"Goal deleted successfully"
        },status=status.HTTP_204_NO_CONTENT)

#------Budget setup-------------------------------------

class BudgetUpsert(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def post(self,request,format=None):
        serializer=BudgetSerializer(data=request.data,context={"request":request})

        if serializer.is_valid():
            budget=serializer.save()
            return Response(
                {"Msg":"Budget Saved Successfully",
                 "budget":BudgetSerializer(budget).data},
                 status=status.HTTP_200_OK
                )
        
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
    
class BudgetList(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request,format=None):
        querySet=Budget.objects.filter(user=request.user)
        filterSet=BudgetFilter(request.GET,queryset=querySet)

        if not filterSet.is_valid():
            return Response(filterSet.errors,status=400)
        
        budget=filterSet.qs
        serializer=BudgetSerializer(budget,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class BudgetDetails(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request,pk):
        budget=Budget.objects.get(user=request.user,pk=pk)
        if not budget:
            return Response({
                "Msg":"Budget not found"
            },status=status.HTTP_404_NOT_FOUND)
        
        serializer=BudgetSerializer(budget)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        try:
            budget=Budget.objects.get(pk=pk,user=request.user)
        except Budget.DoesNotExist:
            return Response({
                "Msg":"Not Found"
            },status=status.HTTP_404_NOT_FOUND)
        
        serializer = BudgetSerializer(
            instance=budget,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg":"Updated successfully",
                 "data":serializer.data},

                status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        budget=Budget.objects.get(pk=pk,user=request.user)
        budget.delete()
        return Response({
            "Msg":"Deleted Successfully"
        },status=status.HTTP_204_NO_CONTENT)
    
class BudgetSummary(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request):
        today=date.today()
        month=int(request.query_params.get("month",today.month))
        year=int(request.query_params.get("year",today.year))

        summary=budgets_summary_for_month(request.user,year,month)

        return Response({
            "month":month,
            "year":year,
            "summary":summary
        },status=status.HTTP_200_OK)
    
