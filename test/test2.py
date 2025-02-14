import os
import json
import uuid
import base64
import pytz
import re
import logging
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Загрузка маппинга из JSON файла
def load_mapping():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mapping_file = os.path.join(current_dir, 'mapping.json')
    logger.debug(f"Loading mapping from: {mapping_file}")
    
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                raise ValueError("Mapping file is empty")
            return json.loads(content)
    except Exception as e:
        logger.error(f"Error loading mapping: {str(e)}")
        raise

MAPPING = load_mapping()

# Декодирование строки с экранированными символами Unicode
def decode_json_data(encoded_data):
    try:
        if isinstance(encoded_data, dict):
            return encoded_data
        if isinstance(encoded_data, str):
            decoded_str = encoded_data.encode('utf-8').decode('unicode_escape')
        else:
            decoded_str = encoded_data.decode('unicode_escape')
        
        cleaned_str = re.sub(r'\\n', ' ', decoded_str)
        return json.loads(cleaned_str)
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при декодировании JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}", exc_info=True)
        return None

# Настройка подключения к Google Sheets
def authenticate_google_sheets():
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        logger.error(f"Ошибка аутентификации Google Sheets: {e}")
        raise

# Получение рабочего листа из Google Sheets
def get_worksheet(spreadsheet_url, sheet_name):
    try:
        client = authenticate_google_sheets()
        spreadsheet = client.open_by_url(spreadsheet_url)
        worksheet = spreadsheet.worksheet(sheet_name)
        return worksheet
    except Exception as e:
        logger.error(f"Ошибка доступа к Google Sheets: {e}")
        raise

# Вставка данных в Google Sheets
def insert_into_google_sheets(spreadsheet_url, sheet_name, data):
    try:
        worksheet = get_worksheet(spreadsheet_url, sheet_name)
        headers = worksheet.row_values(1)
        
        record_id = str(uuid.uuid4())
        moscow_tz = pytz.timezone("Europe/Moscow")
        timestamp = datetime.now(moscow_tz).strftime('%Y-%m-%d %H:%M:%S')
        
        row_data = {'id': record_id, 'timestamp': timestamp}
        
        for question, answer in data.items():
            column_name = MAPPING.get(question)
            if column_name:
                row_data[column_name] = answer
        
        row_values = [row_data.get(header, '') for header in headers]
        worksheet.append_row(row_values)
        
        logger.info(f"Данные успешно загружены в Google Sheets.")
        return record_id
    except Exception as e:
        logger.error(f"Ошибка при вставке данных в Google Sheets: {e}")
        raise

# Основной обработчик
def handler(event, context):
    try:
        logger.info("Запуск обработчика...")

        # Проверяем, что событие не пустое
        if event is None:
            logger.error("Received an empty event")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No event data provided"})
            }

        # Проверяем, есть ли в событии ключ 'body'
        body = event.get('body')
        if not body:
            logger.error("No body provided in the event")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No body provided in the event"})
            }

        # Декодируем строку данных с экранированными символами Unicode
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body).decode('utf-8')
        
        # Разбираем JSON
        data = json.loads(body)
        form_data = decode_json_data(data.get('params', "")) if 'params' in data else data
        
        if not form_data:
            logger.error("Form data is empty")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Form data is empty"})
            }

        # Логируем содержимое события, чтобы проверить
        logger.debug(f"Event data: {event}")
        
        # Получаем URL таблицы из переменных окружения или переданного события
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1DduGWf2nGWBTiiZnwa0qFy7pFI2uruIGnXGIVGjcwUs/edit"

        # Логируем полученное значение
        logger.debug(f"spreadsheet_url: {spreadsheet_url}")
        
        if not spreadsheet_url:
            logger.error("spreadsheet_url is not defined")
            return {
                'statusCode': 500,
                'body': json.dumps({"error": "spreadsheet_url is not defined"})
            }

        sheet_name = "Лист1"
        record_id = insert_into_google_sheets(spreadsheet_url, sheet_name, form_data)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "success", "id": record_id})
        }

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# Для локального тестирования
if __name__ == '__main__':
    with open('test_event.json', 'r', encoding='utf-8') as f:
        event = json.load(f)
    context = {}
    print(handler(event, context))
