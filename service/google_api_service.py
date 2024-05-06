from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from settings import Config

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    'type': Config.TYPE,
    'project_id': Config.PROJECT_ID,
    'private_key_id': Config.PRIVATE_KEY_ID,
    'private_key': Config.PRIVATE_KEY,
    'client_email': Config.CLIENT_EMAIL,
    'client_id': Config.CLIENT_ID,
    'auth_uri': Config.AUTH_URI,
    'token_uri': Config.TOKEN_URI,
    'auth_provider_x509_cert_url': Config.AUTH_PROVIDER_X509_CERT_URL,
    'client_x509_cert_url': Config.CLIENT_X509_CERT_URL
}

cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle


FORMAT = '%Y/%m/%d %H:%M:%S'
ROW_COUNT = 1000
COLUMN_COUNT = 11
SHEETS_VER = 'v4'
DRIVE_VER = 'v3'
TABLE_RANGE = 'A1:L999'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    spreadsheet_body = {
        'properties': {'title': f'Отчёт на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
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
                        'emailAddress': Config.email}
    service = await wrapper_services.discover('drive', DRIVE_VER)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        events: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    table_values = [
        ['ID', 'username', 'Имя', 'Аватар',
         'Дата подписки на канал', 'Дата отписки от канала',
         'utm метка ссылки по которой пришел пользователь',
         'Пол', 'Страна', 'Description', 'Активности']
    ]
    for event in events: 
        new_row = [
            event.user_id,
            event.username,
            event.name,
            event.avatar,
            event.date_in,
            event.date_out,
            event.utm,
            event.gender,
            event.country,
            event.description,
            event.action
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
