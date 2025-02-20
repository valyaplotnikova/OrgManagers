from fastapi import HTTPException
from starlette import status

# Компания уже существует
CompanyAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Компания уже существует'
)

# Компания не найдена
CompanyNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Компания не найдена'
)

# Структура не найдена
StructureNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Структура не найдена'
)

# Участник структуры не найден
StructureMemberNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Участник структуры не найден'
)

# Новость не найдена
NewsNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Новость не найдена'
)
