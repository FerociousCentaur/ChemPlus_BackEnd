from django.conf import settings
from .checksum import Checksum


class GetMessage():
    def message(self,uniqueID,amount):
        msg = f'{settings.MID}|{uniqueID}|NA|{amount}|NA|NA|NA|INR|NA|R|{settings.SEC_ID}|NA|NA|F|NA|NA|NA|NA|NA|NA|NA|{settings.REVERSE_URL}'
        checksum = Checksum.get_checksum(msg)
        return msg+'|'+checksum