import os
import csv
import re
import requests
import json
from collections import namedtuple

from requests.auth import HTTPBasicAuth

from account import SMSC_RU, SMSAERO_RU
from log.logger import logged, response_logger

DATA_DIR = 'data'

User = namedtuple('User', ['name', 'u_num', 'phone'])


def format_phone(phone):
    phone = str(phone)
    phone = ''.join(re.findall(r'\d', phone))
    if len(phone) < 11:
        return False
    if phone[0] in '87':
        phone = '7' + phone[1:]
        return phone
    else:
        return False


def load_data_from_csv(file_name, encoding=''):
    res =[]
    encoding = {'encoding': encoding} if encoding else {}
    file_path = os.path.join(os.path.dirname(__file__), DATA_DIR, file_name)
    with open(file_path, 'r', **encoding) as file:
        data = csv.DictReader(file, delimiter='\t')
        for row in data:
            phone_formatted = format_phone(row['phone'])
            if phone_formatted:
                res.append(phone_formatted)
    return res


@logged
def send_sms_smsc_ru(phone, message, sender=''):
    url = f'https://smsc.ru/sys/send.php' \
          f'?login={SMSC_RU["username"]}' \
          f'&psw={SMSC_RU["password"]}' \
          f'&phones={phone}' \
          f'&mes={message}' \
          f'&fmt=3'
    if sender:
        url += f'&sender={sender}'
    response = json.loads(requests.get(url).text)
    if response.get('error'):
        response_logger.error(f"{phone} - {response.get('error')}")
    else:
        response_logger.info(f"{phone} - sms отправлено")
    return response


@logged
def send_sms_smsaero_ru(phone, message, sender):
    auth = HTTPBasicAuth(SMSAERO_RU['email'], SMSAERO_RU['key'])
    headers = {'application': 'json'}
    url = f'https://gate.smsaero.ru/v2/sms/send' \
          f'?number={phone}' \
          f'&text={message}' \
          f'&channel=DIRECT' \
          f'&sign={sender}'

    response = json.loads(requests.get(url, auth=auth, headers=headers).text)
    if response.get('success'):
        if response['success']:
            response_logger.info(f"{phone} - sms отправлено")
        else:
            response_logger.error(f"{phone} - {response.get('error')}")
    return response
