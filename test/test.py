import json

def decode_json_data(encoded_data):
    # Декодируем строку с экранированными символами Unicode
    decoded_str = bytes(encoded_data, 'utf-8').decode('unicode_escape')
    
    # Теперь можно безопасно распарсить JSON
    try:
        data = json.loads(decoded_str)
        return data
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        return None

# Пример строки с экранированными символами Unicode
encoded_data = r'{\"\u0424\u0430\u043c\u0438\u043b\u0438\u044f\": \"1\", \"\u0418\u043c\u044f\": \"1\", \"\u0412 \u043a\u0430\u043a\u043e\u043c \u0433\u043e\u0440\u043e\u0434\u0435 \u0442\u044b \u0436\u0438\u0432\u0435\u0448\u044c?\": \"\u041a\u043e\u0440\u0441\u0430\u043a\u043e\u0432\u043e-1, \u0425\u0430\u0431\u0430\u0440\u043e\u0432\u0441\u043a\u0438\u0439 \u043a\u0440\u0430\u0439\", \"\u0412 \u043a\u0430\u043a\u043e\u043c \u043a\u043b\u0430\u0441\u0441\u0435 \u0442\u044b \u0443\u0447\u0438\u0448\u044c\u0441\u044f?\": \"1\", \"\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0432\u043a/\u0442\u0433\": \"http://t.me/matveev_im\", \"\u041e\u0442\u043a\u0443\u0434\u0430 \u0443\u0437\u043d\u0430\u043b(-\u0430) \u043f\u0440\u043e \u0432\u0430\u043a\u0430\u043d\u0441\u0438\u044e?\": \"1\", \"\u0421\u043a\u043e\u043b\u044c\u043a\u043e \u0447\u0430\u0441\u043e\u0432 \u0432 \u043d\u0435\u0434\u0435\u043b\u044e \u0442\u044b \u0433\u043e\u0442\u043e\u0432(-\u0430) \u0440\u0430\u0431\u043e\u0442\u0430\u0442\u044c?\": \"\u0434\u043e 10\", \"\u0422\u044b \u0433\u043e\u0442\u043e\u0432(-\u0430) \u0437\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0434\u043e\u0433\u043e\u0432\u043e\u0440 \u043f\u043e\u0434\u0440\u044f\u0434\u0430 (\u0413\u041f\u0425)?\": \"\u0414\u0430\", \"\u041f\u0440\u0438\u043b\u043e\u0436\u0438 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u043d\u043e\u0435 \u0442\u0435\u0441\u0442\u043e\u0432\u043e\u0435 \u0437\u0430\u0434\u0430\u043d\u0438\u0435 \u0432 \u0432\u0438\u0434\u0435 \u0441\u0441\u044b\u043b\u043a\u0438 \u043d\u0430 \u0444\u0430\u0439\u043b\": \"http://t.me/matveev_im\", \"\u041f\u0440\u0438\u043b\u043e\u0436\u0438 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u043d\u043e\u0435 \u0442\u0435\u0441\u0442\u043e\u0432\u043e\u0435 \u0437\u0430\u0434\u0430\u043d\u0438\u0435 \u0432 \u0444\u043e\u0440\u043c\u0430\u0442\u0435 \u0444\u0430\u0439\u043b\u0430\": \"https://forms.yandex.ru/cloud/files?path=%2F4716238%2F67aef62649363998a3e7146b_powerliftingexercisesfinal.csv\", \"\u0414\u0430\u044e \u0441\u043e\u0433\u043b\u0430\u0441\u0438\u0435 \u043d\u0430 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0443 \u0438 \u043f\u0435\u0440\u0435\u0434\u0430\u0447\u0443 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445 \u0432 \u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0438\u0438 \u0441 \u041f\u043e\u043b\u0438\u0442\u0438\u043a\u043e\u0439 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445. \\n\u0421\u043e\u0433\u043b\u0430\u0441\u0438\u0435 \u0437\u0430\u043a\u043e\u043d\u043d\u043e\u0433\u043e \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u0438\u0442\u0435\u043b\u044f \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0430\u044e.\": \"\u0414\u0430\"}'

# Декодируем строку
decoded_data = decode_json_data(encoded_data)

# Проверяем результат
if decoded_data:
    print(json.dumps(decoded_data, ensure_ascii=False, indent=2))

#     import os
# import json
# import uuid
# from datetime import datetime
# import base64
# import pytz
# import re
# import logging
# import gspread
# from google.oauth2.service_account import Credentials
# from collections import OrderedDict

# # Настройка логирования
# logging.basicConfig(level=logging.DEBUG)

# # Декодирование строки с экранированными символами Unicode
# def decode_json_data(encoded_data):
#     try:
#         # Если данные уже являются словарем, то просто возвращаем их
#         if isinstance(encoded_data, dict):
#             return encoded_data
        
#         # Если encoded_data уже строка, то сразу декодируем её
#         if isinstance(encoded_data, str):
#             decoded_str = encoded_data.encode('utf-8').decode('unicode_escape')
#         else:
#             # Если данные не строка, пытаемся декодировать байтовые данные
#             decoded_str = encoded_data.decode('unicode_escape')
        
#         # Очищаем данные от возможных лишних символов, например, \n
#         cleaned_str = re.sub(r'\\n', ' ', decoded_str)  # Заменяем \n на пробелы
        
#         # Теперь можно безопасно распарсить JSON
#         return json.loads(cleaned_str)
#     except json.JSONDecodeError as e:
#         logging.error(f"Ошибка при декодировании JSON: {e}")
#         return None
#     except Exception as e:
#         logging.error(f"Произошла ошибка: {str(e)}", exc_info=True)
#         return None


# # Загрузка словаря
# def load_mapping():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     mapping_file = os.path.join(current_dir, 'mapping.json')
#     logging.debug(f"Loading mapping from: {mapping_file}")

#     if not os.path.exists(mapping_file):
#         logging.error(f"Mapping file not found at {mapping_file}")
#         raise FileNotFoundError(f"Mapping file not found at {mapping_file}")

#     try:
#         with open(mapping_file, 'r', encoding='utf-8-sig') as f:
#             content = f.read()
#             logging.debug(f"Mapping file content: {content}")  # Логируем содержимое
#             if not content.strip():  # Проверка на пустое содержимое
#                 logging.error("Mapping file is empty")
#                 raise ValueError("Mapping file is empty")
            
#             logging.debug("Successfully loaded mapping content.")
#             return json.loads(content)
#     except json.JSONDecodeError as e:
#         logging.error(f"Error decoding JSON from mapping file: {e}")
#         raise
#     except Exception as e:
#         logging.error(f"Error loading mapping: {str(e)}")
#         raise


# MAPPING = load_mapping()

# # Настройка подключения к Google Sheets
# SCOPE = ["https://spreadsheets.google.com/feeds", 
#              "https://www.googleapis.com/auth/spreadsheets", 
#              "https://www.googleapis.com/auth/drive.file", 
#              "https://www.googleapis.com/auth/drive"
# ]

# CREDENTIALS = Credentials.from_service_account_file(
#     "credentials.json",
#     scopes=SCOPE
# )
# client = gspread.authorize(CREDENTIALS)

# # Конфигурация таблицы
# SPREADSHEET_URL = os.getenv('SPREADSHEET_URL')
# SHEET_NAME = os.getenv('SHEET_NAME')

# def get_worksheet():
#     try:
#         spreadsheet = client.open_by_url(SPREADSHEET_URL)
#         worksheet = spreadsheet.worksheet(SHEET_NAME)
#         return worksheet
#     except Exception as e:
#         logging.error(f"Ошибка доступа к Google Sheets: {e}")
#         raise

# # Функция для извлечения числа из строки
# def extract_number(answer):
#     if isinstance(answer, str):
#         match = re.search(r'":\s*(\d+)', answer)
#         if match:
#             return match.group(1)
#         try:
#             json_str = '{' + answer + '}'
#             data = json.loads(json_str)
#             return str(list(data.values())[0])
#         except json.JSONDecodeError:
#             pass
#     return answer

# # Функция для вставки данных в Google Sheets
# def insert_into_google_sheets(data):
#     worksheet = get_worksheet()
#     headers = worksheet.row_values(1)
    
#     record_id = str(uuid.uuid4())
#     moscow_tz = pytz.timezone("Europe/Moscow")
#     moscow_time = datetime.now(moscow_tz)
#     timestamp = moscow_time.strftime('%Y-%m-%d %H:%M:%S')
    
#     row_data = {'id': record_id, 'timestamp': timestamp}
    
#     for question, answer in data.items():
#         column_name = MAPPING.get(question)
#         if column_name:
#             if isinstance(answer, str) and re.match(r'".*":\s*\d+', answer):
#                 answer = extract_number(answer)
#             row_data[column_name] = answer
    
#     row_values = [row_data.get(header, '') for header in headers]
#     worksheet.append_row(row_values)
    
#     return record_id

# # Основной обработчик
# def handler(event, context):
#     try:
#         # Проверяем, что событие не пустое
#         if event is None:
#             logging.error("Received an empty event")
#             return {
#                 "statusCode": 400,
#                 "body": json.dumps({"error": "No event data provided"})
#             }

#         # Проверяем, есть ли в событии ключ 'body'
#         body = event.get('body')
#         if not body:
#             return {
#                 "statusCode": 400,
#                 "body": json.dumps({"error": "No body provided in the event"})
#             }

#         # Декодируем строку данных с экранированными символами Unicode
#         if event.get('isBase64Encoded', False):
#             body = base64.b64decode(body).decode('utf-8')
        
#         # Разбираем JSON
#         data = json.loads(body)
#         form_data = decode_json_data(data.get('params', "")) if 'params' in data else data
        
#         if not form_data:
#             return {
#                 "statusCode": 400,
#                 "body": json.dumps({"error": "Form data is empty"})
#             }

#         record_id = insert_into_google_sheets(form_data)
#         return {
#             "statusCode": 200,
#             "body": json.dumps({"status": "success", "id": record_id})
#         }

#     except Exception as e:
#         logging.error(f"Error: {str(e)}", exc_info=True)
#         return {
#             "statusCode": 500,
#             "body": json.dumps({"error": str(e)})
#         }


