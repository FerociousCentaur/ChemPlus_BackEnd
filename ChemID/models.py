from django.db import models
import uuid
from django.utils import timezone
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
import datetime

from .choices import college, department, program, year, gender
# Create your models here.
def sid(id):
    return "CHPS21%04d" % id

# class EventManager(models.Manager):
#
#     def get_queryset(self):
#         return super().get_queryset().filter(
#             publishing_date__gte=timezone.now()-timezone.timedelta(minutes=5)
#         )

class Spectator(models.Model):
    id = models.AutoField(primary_key=True, editable=False)

    first_name = models.CharField(max_length=300,null=True,blank=True)
    last_name = models.CharField(max_length=300,null=True,blank=True)
    gender = models.CharField(max_length=6,null=True,blank=True)

    email = models.EmailField(null=True,blank=True,unique=True)
    mob_number = models.CharField(max_length=10,null=True,blank=True)
    alt_mob_number = models.CharField(max_length=10,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    zipcode = models.CharField(max_length=6,null=True,blank=True)


    state = models.CharField(max_length=30,null=True,blank=True)
    college = models.CharField(max_length=300, null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    program = models.CharField(max_length=10, null=True,blank=True)
    year = models.CharField(max_length=10, null=True,blank=True)
    chem_id = models.CharField(max_length=10, editable=False, unique=True)

    email_otp = models.PositiveIntegerField(null=True,blank=True)
    verified = models.BooleanField(default=False)

    publishing_date = models.DateTimeField(default=timezone.now, blank=True)

    is_all_events = models.BooleanField(default=False)
    is_python = models.BooleanField(default=False)
    is_ansys = models.BooleanField(default=False)
    is_scilab = models.BooleanField(default=False)
    is_matlab = models.BooleanField(default=False)
    is_aspen = models.BooleanField(default=False)
    is_dwsim = models.BooleanField(default=False)



    def __str__(self):
        return f'{self.first_name} [{self.chem_id}]'




@receiver(post_save, sender=Spectator)
def set_person_id(sender, instance, created, **kwargs):
     if created:
         instance.chem_id = "CHES21%04d" % instance.id
         instance.save()

class BroadCast_Email(models.Model):
    subject = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    message = models.TextField()

    def __unicode__(self):
        return self.subject

    class Meta:
        verbose_name = "BroadCast Email to all Member"
        verbose_name_plural = "BroadCast Email"

# added intance.verified to create chem_id

class Transaction(models.Model):
    owner = models.ForeignKey(Spectator, on_delete=models.DO_NOTHING, blank=False,null=True)
    order_id = models.CharField(max_length=30, blank=False, null=True)
    txn_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=30, blank=True, null=True)
    amount_initiated = models.FloatField(blank=True, null=True)
    was_success = models.BooleanField(default=False)
    status = models.CharField(max_length=30, blank=True, null=True)
    log = models.TextField(null=True, blank=True)
    registered_for = models.TextField(null=True, blank=True)
    txn_date = models.DateTimeField(default=timezone.now, blank=True)
    ru_date = models.DateTimeField(blank=True, null=True)
    s2s_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.owner.chem_id} [{self.order_id}]'

