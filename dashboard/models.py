from django.db import models

def generate_client_id():
    import string, random
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class BaseTimestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseTimestamp):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    auth_provider_id = models.CharField(max_length=255, null=True) # Third party auth provider id

    class Meta:
        db_table = 'user'
        

class Client(BaseTimestamp):
    id = models.CharField(max_length=255, primary_key=True, default=generate_client_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'client'

class Feedback(BaseTimestamp):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        db_table = 'feedback'


class WhiteList(BaseTimestamp):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)

    class Meta:
        db_table = 'whitelist'

class Wallet(BaseTimestamp):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    overdraft_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'wallet'


class WalletLedger(BaseTimestamp):
    class TransactionType(models.TextChoices):
        DEBIT = 'DEBIT'
        CREDIT = 'CREDIT'
    
    class Purpose(models.TextChoices):
        RECHARGE = 'RECHARGE'
        FEEDBACK_USAGE = 'FEEDBACK_USAGE'
    
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TransactionType.choices)
    purpose = models.CharField(max_length=255, choices=Purpose.choices)

    class Meta:
        db_table = 'wallet_ledger'
