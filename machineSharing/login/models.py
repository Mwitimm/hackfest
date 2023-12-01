import uuid

from django.db import models


# Create your models here.


class Account(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=0)
    user_id = models.IntegerField()
    name = models.CharField(max_length=100, null=True)
    admin = models.BooleanField(default=0)


    def __str__(self):
        return self.name


class AddEquipment(models.Model):
    user_id = models.IntegerField(null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(null=True)
    img = models.ImageField(null=True,blank=True,upload_to="images/")
    Desc = models.TextField(null=True)
    type = models.TextField(default='tractor')
    condition = models.TextField()
    location = models.TextField()
    rental_rate = models.IntegerField(default=5)
    available = models.BooleanField(default=1)


class Apply(models.Model):
    member = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=1)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    date_applied = models.DateField(auto_now_add=True)
    date_approved = models.DateField(null=True, blank=True)
    date_due = models.DateField(null=True, blank=True)
    type = models.BooleanField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    ])

    def __str__(self):
        return f"Loan {self.id} - {self.member}"


class PayLoan(models.Model):
    member = models.CharField(max_length=50)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=1)
    payment_date = models.DateField(auto_now_add=True)


class Contribution(models.Model):
    member = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    contribution_month = models.IntegerField(default=0)  # Represents the month (1-12)
    contribution_year = models.IntegerField(default=2001)

    def __str__(self):
        return f"Contribution {self.id} - {self.member}"


class Loan(models.Model):
    loan_id = models.IntegerField(default=1)
    loan = models.IntegerField(default=6300)


class MonthlyActivity(models.Model):
    member = models.CharField(max_length=20)
    aggregate_balance = models.IntegerField(default=6300)
    total_contributions = models.IntegerField(default=10500)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.member.name


class Turn(models.Model):
    member = models.CharField(max_length=20)
    start_date = models.DateField(auto_now_add=True)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.member} - {self.start_date} to {self.end_date}"


class ActivityLog(models.Model):
    user = models.CharField(max_length=20)
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=[
        ('event', 'event'),
        ('info', 'info'),
        ('system', 'system'),
        ('team', 'team'),
    ])
    username = models.CharField(max_length=20)
    sender = models.CharField(max_length=20)
    message = models.CharField(max_length=1000)
    subject = models.CharField(max_length=250, default="Welcome Message")
    read = models.BooleanField(default=0)
