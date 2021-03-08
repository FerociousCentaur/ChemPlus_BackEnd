from ChemID.models import Transaction
from ChemID.billdesk.gen_message import GetMessage
from ChemID.billdesk.checksum import Checksum
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Django admin command to check the pending status of transactions'

    def handle(self, *args, **kwargs):
        scheduled_check()

def findNthOccur(string, ch, N):
    occur = 0

    # Loop to find the Nth
    # occurence of the character
    for i in range(len(string)):
        if (string[i] == ch):
            occur += 1

        if (occur == N):
            return i

    return -1

def scheduled_check():
    waiting = Transaction.objects.filter(status = 'WAITING')
    if waiting:
        for wait in waiting:
            msg = GetMessage().schedule_msg(wait.order_id)
            response = requests.post(settings.CONF_BILL_URL, data={'msg': msg})
            response = response.text
            valid_payment = Checksum().verify_checksum(response)
            pipeind1 = findNthOccur(response, '|', 1)
            pipeind2 = findNthOccur(response, '|', 2)
            pipeind3 = findNthOccur(response, '|', 3)
            pipeind31 = findNthOccur(response, '|', 31)
            pipeind32 = findNthOccur(response, '|', 32)
            mid = response[pipeind1+1:pipeind2]
            oid = response[pipeind2 + 1:pipeind3]
            status = response[pipeind31 + 1:pipeind32]
            if valid_payment:
                if mid == settings.MID and status == 'Y':
                    wait.status = 'Late SUCCESS'
                    wait.save()