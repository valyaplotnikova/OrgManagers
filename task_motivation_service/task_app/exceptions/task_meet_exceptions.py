from fastapi import HTTPException
from starlette import status

# Задача уже существует
TaskAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Задача уже существует'
)

# Задача не найдена
TaskNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Задача не найдена'
)

# Мотивация не найдена
MotivationNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Мотивация не найдена'
)

# Мотивация для этой задачи уже существует
MotivationAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Мотивация для этой задачи уже существует.")

# Встреча не найдена
MeetingNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Встреча не найдена'
)

# Участник встречи не найден
ParticipantNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Участник встречи не найден'
)

# Недостаточно прав
ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Недостаточно прав')

# Токен истек
TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истек'
)

# Некорректный формат токена
InvalidTokenFormatException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Некорректный формат токена'
)


# Токен отсутствует в заголовке
TokenNoFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Токен отсутствует в заголовке'
)

# Невалидный JWT токен
NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен не валидный'
)


# Неверный формат токена. Ожидается 'Bearer <токен>'
TokenInvalidFormatException = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат токена. Ожидается 'Bearer <токен>'"
)