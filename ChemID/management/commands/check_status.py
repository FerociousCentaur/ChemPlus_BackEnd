from ChemID.models import Transaction, Spectator
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
            pipeind15 = findNthOccur(response, '|', 15)
            pipeind16 = findNthOccur(response, '|', 16)
            pipeind27 = findNthOccur(response, '|', 27)
            pipeind28 = findNthOccur(response, '|', 28)
            pipeind29 = findNthOccur(response, '|', 29)
            pipeind31 = findNthOccur(response, '|', 31)
            pipeind32 = findNthOccur(response, '|', 32)
            mid = response[pipeind1+1:pipeind2]
            oid = response[pipeind2 + 1:pipeind3]
            status = response[pipeind31 + 1:pipeind32]
            authstat = response[pipeind15 + 1:pipeind16]
            refundtstat = response[pipeind28 + 1:pipeind29]
            amnt = response[pipeind27 + 1:pipeind28]
            if valid_payment:
                if mid == settings.MID and authstat == '0300' and wait.amount_initiated==float(amnt):
                    if refundtstat == '0699':
                        wait.status = 'Refunded'
                    elif refundtstat == '0799':
                        wait.status = 'Refund initiated'
                    elif refundtstat == 'NA':
                        wait.status = 'Late SUCCESS'
                        chem_id = wait.owner.chem_id
                        reg_for = eval(wait.registered_for)
                        usr_details = Spectator.objects.filter(chem_id=chem_id)[0]
                        for i in reg_for:
                            if i == 'All events pass':
                                usr_details.is_all_events = True
                            elif i == 'Ansys':
                                usr_details.is_ansys = True
                            elif i == 'Python':
                                usr_details.is_python = True
                            elif i == 'SciLab':
                                usr_details.is_scilab = True
                            elif i == 'Matlab':
                                usr_details.is_matlab = True
                        usr_details.save()
                        wait.was_success = True
                    elif refundtstat == '0899':
                        wait.status = 'Refunded thro Chargeback'
                    wait.log += str([response])
                    wait.save()