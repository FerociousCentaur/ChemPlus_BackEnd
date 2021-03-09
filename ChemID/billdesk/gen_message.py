from django.conf import settings
from .checksum import Checksum
from datetime import datetime


class GetMessage():
    def message(self,uniqueID,amount, chem_id, mail, fname, mnumber):
        msg = f'{settings.MID}|{uniqueID}|NA|{amount:.2f}|NA|NA|NA|INR|NA|R|{settings.SEC_ID}|NA|NA|F|{fname}|{chem_id}|{mail}|{mnumber}|NA|NA|NA|{settings.REVERSE_URL}'
        checksum = Checksum().get_checksum(msg)
        return msg+'|'+checksum
    def schedule_msg(self,oid):
        msg = f'0122|{settings.MID}|{oid}|{self.date()}'
        checksum = Checksum().get_checksum(msg)
        return msg + '|' + checksum
    def date(self):
        date = datetime.now()
        return f"{date.year:04d}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}{date.second:02d}"
