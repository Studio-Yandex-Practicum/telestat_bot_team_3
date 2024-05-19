from datetime import datetime

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from core.db import async_session, engine
from crud.report import report_crud
from settings import Config, configure_logging

logger = configure_logging()

FORMAT = '%Y/%m/%d-%H:%M:%S'
ROW_COUNT = 1000
COLUMN_COUNT = 12
SHEETS_VER = 'v4'
DRIVE_VER = 'v3'
TABLE_RANGE = 'A1:L999'

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


async def get_spreadsheets_id(wrapper_services: Aiogoogle, name: str):
    service = await wrapper_services.discover('drive', DRIVE_VER)
    spreadsheets = await wrapper_services.as_service_account(
        service.files.list(
            q=f"name = '{name}' and mimeType = 'application/vnd.google-apps.spreadsheet'"
        )
    )
    if len(spreadsheets['files']) >= 1:
        if len(spreadsheets['files']) > 1:
            logger.warning(
                f'Обнаружено несколько файлов с именем {name}'
            )
        return spreadsheets['files'][0]['id']
    elif len(spreadsheets['files']) == 0:
        return None


# TODO: Данная функция требется только на стадии разработки, по завершению ее можно удалить
async def delete_all_files_by_name(
        wrapper_services: Aiogoogle,
        chanal_name: str
):
    """
    Служебная функция для удаления всех файлов имеющих определенное название. 
    Нужна чтоы удалять файлы, которые были созданы, 
    но не видны у собственника аккаунта google
    """
    service = await wrapper_services.discover('drive', DRIVE_VER)
    spreadsheets = await wrapper_services.as_service_account(
        service.files.list(q=f"name = '{chanal_name}'")
    )
    for item in spreadsheets['files']:
        await wrapper_services.as_service_account(
            service.files.delete(fileId=item['id'])
        )
    print(f"All files with name {chanal_name} delete.")


async def spreadsheets_create(wrapper_services: Aiogoogle, chanal_name: str) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    sheet_title = f'report_{now_date_time}'
    spreadsheet_body = {
        'properties': {'title': f'{chanal_name}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': sheet_title,
                                   'gridProperties': {
                                        'rowCount': ROW_COUNT,
                                        'columnCount': COLUMN_COUNT
                                    }}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid, sheet_title


async def spreadsheets_create_new_list(
        wrapper_services: Aiogoogle,
        spreadsheetid: str
):
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    sheet_title = f'report_{now_date_time}'
    spreadsheet_body = {
        'requests': [
            {
                'addSheet': {
                    'properties': {
                        'title': sheet_title,
                        'gridProperties': {
                            'rowCount': ROW_COUNT,
                            'columnCount': COLUMN_COUNT
                        }
                    }
                }
            }
        ]
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.batchUpdate(
            spreadsheetId=spreadsheetid,
            json=spreadsheet_body
        )
    )

    return sheet_title


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    #На релизе поменять обратно.
    # permissions_body = {'type': 'user',
    #                     'role': 'writer',
    #                     'emailAddress': Config.EMAIL}
    permissions_body = {'type': 'anyone',
                        'role': 'reader'}
    service = await wrapper_services.discover('drive', DRIVE_VER)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        sheet_title: str,
        data: dict,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', SHEETS_VER)
    table_values = []
    # Запись информации об активности
    logger.debug('Подготовка информации об активности для записи в таблицу')
    table_values.append(['Активность', 'Среднее количество'])
    for activity, amount in data['Активности'].items():
        new_row = [
            activity, amount
        ]
        table_values.append(new_row)
    logger.debug(
        'Подготовка информации об активности для записи в таблицу завершена'
    )
    table_values.append([])  # Пустая строка

    # Запись информации подписчиках
    logger.debug('Подготовка информации о подписчиках для записи в таблицу')
    table_values.append(
        ['ID', 'Username', 'Имя', 'Язык пользователя',
         'Дата подписки на канал', 'Статус подписчика', 'Это бот?', 'Фото'])

    for follower in data['Подписчики']:
        new_row = [
            follower['ID'],
            follower['Username'],
            follower['Имя'],
            follower['Язык пользователя'],
            follower['Дата вступления'],
            follower['Статус подписчика'],
            follower['Это бот ?'],
            follower['Фото']
        ]
        table_values.append(new_row)
    logger.debug(
        'Подготовка информации о подписчиках для записи в таблицу завершена'
    )

    update_body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {
                "range": f'{sheet_title}!{TABLE_RANGE}',
                "majorDimension": "ROWS",
                "values": table_values
            }
        ]
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.batchUpdate(
            spreadsheetId=spreadsheetid,
            json=update_body
        )
    )


async def get_report(
    data: dict
):
    """Создание отчета в Google spreadsheets."""
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        reports_url = []
        for chanal_name, data in data.items():
            # await delete_all_files_by_name(aiogoogle, chanal_name) # TODO Не забыть удалить перед релизом
            spreadsheetid = await get_spreadsheets_id(aiogoogle, chanal_name)
            if spreadsheetid is None:
                spreadsheetid, sheet_title = await spreadsheets_create(
                    aiogoogle, chanal_name
                )
                logger.info(
                    f'Создана таблица {chanal_name} с листом {sheet_title}'
                )
                await set_user_permissions(spreadsheetid, aiogoogle)
                logger.info(
                    f'Таблице {chanal_name} установлены разрешения'
                )
            else:
                sheet_title = await spreadsheets_create_new_list(
                    aiogoogle, spreadsheetid
                )
                logger.info(
                    f'В таблицу {chanal_name} добавлен лист {sheet_title}'
                )
            await spreadsheets_update_value(spreadsheetid,
                                            sheet_title,
                                            data,
                                            aiogoogle)
            url = f'https://docs.google.com/spreadsheets/d/{spreadsheetid}'
            logger.info(
                f'Отчет по каналу {chanal_name} сформирован: URL {url}'
            )
            async with async_session() as session:
                async with engine.connect():
                    report_crud.create(
                        {
                            'link': url,
                            'group': chanal_name
                        },
                        session=session
                    )
            reports_url.append(
                f'Отчет по каналу {chanal_name} сформирован: {url}'
            )
        return reports_url
