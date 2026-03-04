from expense_management.models import *
from decimal import Decimal

# get wallet
def get_wallet(user):
    wallet,created=Wallet.objects.get_or_create(user=user)
    return wallet


def SpilitIncome(user,amount):
    # get wallet amount 
    wallet=get_wallet(user)
    # convert into decimal feild to multiply amount to bcz float only 8 bit and decimal is 16 bit
    amount=Decimal(str(amount))
    saving_part=amount*Decimal("0.3")
    main_part=amount-saving_part

    wallet.main_balance+=main_part
    wallet.saving_balance+=saving_part

    wallet.save()
    return wallet

def DeductFromWallet(user,amount):
    # deduct from wallet -> first deduct from main wallet-> saving wallet
    wallet=get_wallet(user)
    amount=Decimal(str(amount))

    if wallet.main_balance>amount:
        wallet.main_balance-=amount
    else:
        remaining_amount=amount-wallet.main_balance
        wallet.main_balance=Decimal("0")
        wallet.saving_balance-=remaining_amount
    
    wallet.save()
    return wallet




        


