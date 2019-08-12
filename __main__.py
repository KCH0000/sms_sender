from sender import load_data_from_csv, send_sms
from log.logger import response_logger
from time import sleep

MESSAGE = '17 августа 13.00 состоится ' \
          'собрание собственников, членов СНТ "Астра"'

source_files = [
    {'name': 'astra_phones_1.csv', 'encoding': 'UTF-8'},
    {'name': 'astra_phones_2.csv', 'encoding': 'UTF-8'},
    {'name': 'astra_phones_4.csv', 'encoding': 'UTF-8'},
    {'name': 'astra_phones_5.csv', 'encoding': 'UTF-8'}
]

blacklist_file = 'blacklist.csv'

sender_list = []

for file in source_files:
    sender_list += load_data_from_csv(file['name'], file['encoding'])
    response_logger.info(f'Загружены данные из {file["name"]}, всего {len(sender_list)} номеров')

blacklist = load_data_from_csv(blacklist_file)
response_logger.info(f'Вчерноем списке {len(blacklist)} номеров')

sender_list = set(sender_list) - set(blacklist)
response_logger.info(f'Всего уникальных {len(sender_list)} номеров')

if len(MESSAGE) > 70:
    response_logger.error(f'Длина сообщения {len(MESSAGE)} символов')
    assert len(MESSAGE) < 70

response_logger.info(f'Длина сообщения {len(MESSAGE)} символов')

# for sender in sender_list:
#     sleep(1)
#     send_sms(sender, MESSAGE)
# send_sms('79266023332', MESSAGE, 'SMSC.RU')