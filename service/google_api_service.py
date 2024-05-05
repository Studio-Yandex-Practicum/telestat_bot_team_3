from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

# времянка для тестов
load_dotenv('.env')
# from settings import Config

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    'type': os.environ['TYPE'],
    'project_id': os.environ['PROJECT_ID'],
    'private_key_id': os.environ['PRIVATE_KEY_ID'],
    # TODO Нужно расхардкодить, через os.environ работать не хочет
    'private_key': "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDp8UgYk7fN96wR\nV5WcK0tKitnHSk0McpYHYprD0E9Lfu4QWGge/XWpHsLail/l0up5WqvlUHWKYiYR\nes2r3QM0zQi1kjDDtH1lO0fdmtT5gMpGgHseCbGrpzqo9My4O+hSdYEJUsVzfJ7I\nvG6FSj2nVon+66GILxKnAGzbw3e31TpzKOd4+iWR9HNp7NAqHdmb8AGk9rtPwkkX\n69hItPEHtFAJZ5nCAj/kv8sr23OdE8OJyssirA6tF3JlRWMWLhc/54c6LPFyYXGh\nMj+OyaYggmPVLudhx1G5GivF4+P/mJbrXAumbPM3KOrT0h0HKvKrRUDUqNlR1rgu\nZa4E5z8lAgMBAAECggEAMnzl1hYFMECQJEL+cRB/5IPAWcv9gl71ZX0gkPtzLYQk\nfScTO4LwYnIW0+LSrO8ettd8axY488dYV2PlIL7nOv038LWu7AGXIWKQkTEh3wHu\nRZZjW7l0XGsQFBgW2XjmW+trkHdKUTD3NLPD92StFyDsUbWJLDKaiCulkq0l+Gh0\nwthGuWEigHI8saAtYTZwq9aKT+fiPp5pYNmQR/I1TF0JcbD3IGvb94vEj2LauMAZ\nO7YQy59eHguun1Iwge/6KSVmaFzScgXtlHNIFA3/wxGBBLkQC5wVozXTN5FS0q8N\nM9xpAP37OQ9ByLDLotW+2n5f6x0xzBZ4nV0yK4FBOQKBgQD/+qkWdfIVs1YgdZ3G\nLwFa+vvrUyrGGEc0C+QqTFsemyjLqGEmzFJjKTINaLWy0e2BykSJd/0DQiwVmCcz\nvyjO4Wu9RDB2ou2d+WHZo9iNItgoy8/OgHsUS9j7kmqtFS8IbsW8vSB/n8hNk2Hu\nuUfLI49gM8BFOE5cyU+Pszr+WQKBgQDp9ilVg30iU1Jzjf8+4TfazUITqOmP4CHt\nRbcfsYa1sZXcMgfQerCHiKOXJLiLrE5VspiBbd2B1BxCwo9e+yMOIWnbAZawhkbn\n01QiCYLU/1yNr3/oStlv423qFGCPWNLkDQR8Dd17XCVc1vpXHfl+y1dMVidtaSKy\nCGn6oaqlrQKBgQDXP6tRxMpVryD8WIrcbQhhve16m8u7Gg092cX6P4zbtrNeVe+j\n1WpuEeUR23v2q4phenmZczlhtRIm8nP8koE5PdsAI0fxat4O2faLMbjWLXfBDmln\nByj4DzOdkCh99PNAzw0dwZeDWhPwD7/pIwoY6oUU60+BpXBXm7x4ZMl1uQKBgB5u\n++94vDVT21zWssYuK8LVgmvmRAOIJ0GjGPARerF12UWcaHHRE9d9ibImf68DiekR\n406qyO6Tdd2lS1sSlfvHkup/KWfq/5w2XDJVRGSKlzKDCsNfwSsRzYFuhyT+a+ho\nXRX6A76BPQb3m/brGkJJFyEB7/0GeRHpkEee8gC9AoGAaAxsWHOj2g8CQbPnQU1I\noHxG3a8R0PFf0o/60IBTxC7+VcpaRRsEuVinuJVZG8aDWpXLz3D5DMrBvjZU7W6q\nGUAe0CET2X6PKQwXsZgA10yL1iU3ZJu5zlG6QnLvsjpa2GYorrFkkJOqUk3lDyKE\nF9bUJDKwaP8NdcShcdzv+lQ=\n-----END PRIVATE KEY-----\n",
    'client_email': os.environ['CLIENT_EMAIL'],
    'client_id': os.environ['CLIENT_ID'],
    'auth_uri': os.environ['AUTH_URI'],
    'token_uri': os.environ['TOKEN_URI'],
    'auth_provider_x509_cert_url': os.environ['AUTH_PROVIDER_X509_CERT_URL'],
    'client_x509_cert_url': os.environ['CLIENT_X509_CERT_URL']
}

cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


# async def get_service():
#     async with Aiogoogle(service_account_creds=cred) as aiogoogle:
#         yield aiogoogle


FORMAT = '%Y/%m/%d %H:%M:%S'
ROW_COUNT = 1000
COLUMN_COUNT = 11
SHEETS_VER = 'v4'
DRIVE_VER = 'v3'
TABLE_RANGE = 'A1:L999'

async def get_spreadsheets_id(wrapper_services: Aiogoogle, name: str):
    service = await wrapper_services.discover('drive', DRIVE_VER)
    spreadsheets = await wrapper_services.as_service_account(
        service.files.list(q=f"name = '{name}' and mimeType = 'application/vnd.google-apps.spreadsheet'")
    )
    if len(spreadsheets['files']) >= 1:
        if len(spreadsheets['files']) > 1:
            pass # Думаю нужно в логгер передавать ворнинг, что несколько файлов с одинаковым названием
        return spreadsheets['files'][0]['id']
    elif len(spreadsheets['files']) == 0:
        return None
    
async def delete_all_files_by_name(wrapper_services: Aiogoogle, name: str):
    """
    Служебная функция для удаления всех файлов имеющих определенное название. 
    Нужна чтоы удалять файлы, которые были созданы, но не видны у собственника аккаунта google
    """
    service = await wrapper_services.discover('drive', DRIVE_VER)
    spreadsheets = await wrapper_services.as_service_account(
        service.files.list(q=f"name = '{name}'")
    )
    for item in spreadsheets['files']:
        await wrapper_services.as_service_account(
        service.files.delete(fileId=item['id'])
    )
    print("Операция завершена")



async def spreadsheets_create(wrapper_services: Aiogoogle, name: str) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    spreadsheet_body = {
        'properties': {'title': f'{name}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': f'Отчёт на {now_date_time}',
                                   'gridProperties': {'rowCount': ROW_COUNT,
                                                      'columnCount': COLUMN_COUNT}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': os.environ['EMAIL']}
    service = await wrapper_services.discover('drive', DRIVE_VER)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        data: list[dict],
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    table_values = [
        ['ID', 'username', 'Имя', 'Аватар',
         'Дата подписки на канал', 'Дата отписки от канала',
         'utm метка ссылки по которой пришел пользователь',
         'Пол', 'Страна', 'Description', 'Активности']
    ]
    for item in data:
        actions = '\n'.join(item['action'])
        new_row = [
            item['user_id'],
            item['username'],
            item['name'],
            item['avatar'],
            item['date_in'],
            item['date_out'],
            item['utm'],
            item['gender'],
            item['country'],
            item['description'],
            actions
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=TABLE_RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def get_report(
    data: dict, # Пока путь словарь будет
):
    """Создание отчета в Google spreadsheets."""
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        for name, item in data.items():
            # await delete_all_files_by_name(aiogoogle, name) # Не забыть удалить
            spreadsheetid = await get_spreadsheets_id(aiogoogle, name)
            if spreadsheetid is None:
                spreadsheetid = await spreadsheets_create(aiogoogle, name)
            await set_user_permissions(spreadsheetid, aiogoogle)
            await spreadsheets_update_value(spreadsheetid,
                                            item,
                                            aiogoogle)

if __name__ == '__main__':
    # Тестовые данные:
    data = {
        'chanal_1': [
            {
                'user_id': 123456,
                'username': 'Ivan123',
                'name': 'Ivan',
                'avatar': 'image1.png',
                'date_in': '2024_01_01',
                'date_out': '2024_01_02',
                'utm': '',
                'gender': 'man',
                'country': 'Russia',
                'description': '',
                'action': ['1', '2']
            },
            {
                'user_id': 123457,
                'username': 'Ivan124',
                'name': 'Ivan',
                'avatar': 'image2.png',
                'date_in': '2024_01_01',
                'date_out': '2024_01_02',
                'utm': '',
                'gender': 'man',
                'country': 'Russia',
                'description': '',
                'action': ['1', '2']
            }
        ],
        'chanal_2': [
            {
                'user_id': 123456,
                'username': 'Ivan123',
                'name': 'Ivan',
                'avatar': 'image1.png',
                'date_in': '2024_01_01',
                'date_out': '2024_01_02',
                'utm': '',
                'gender': 'man',
                'country': 'Russia',
                'description': '',
                'action': ['3', '4']
            },
            {
                'user_id': 123457,
                'username': 'Ivan124',
                'name': 'Ivan',
                'avatar': 'image2.png',
                'date_in': '2024_01_01',
                'date_out': '2024_01_02',
                'utm': '',
                'gender': 'man',
                'country': 'Russia',
                'description': '',
                'action': ['3', '4']
            }
        ]
    }
    import asyncio
    asyncio.run(get_report(data))
    