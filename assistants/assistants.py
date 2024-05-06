from crud.userstg import userstg_crud


async def check_by_attr(attr_name, attr_value, session) -> bool:
    """Проверка id на наличие в ДБ."""

    if await userstg_crud.get_by_attr(
            attr_name,
            attr_value,
            session
            ) is None:
        return False
    return True
