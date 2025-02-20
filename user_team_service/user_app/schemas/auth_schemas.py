from typing import Self, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator, computed_field
from user_team_service.user_app.utils import get_password_hash


class EmailModel(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    model_config = ConfigDict(from_attributes=True)


class UserBase(EmailModel):
    first_name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    email: EmailStr = Field(description="Электронная почта")


class SUserRegister(UserBase):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    confirm_password: str = Field(min_length=5, max_length=50, description="Повторите пароль")

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
        self.password = get_password_hash(self.password)  # хешируем пароль до сохранения в базе данных
        return self


class SUserAddDB(UserBase):
    password: str = Field(min_length=5, description="Пароль в формате HASH-строки")


class SUserAuth(EmailModel):
    password: str = Field(min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class SUserStatus(BaseModel):
    status: str = Field(description="Статус пользователя")


class SUserCompany(BaseModel):
    company_id: Optional[int | None] = None


class SUserInfo(UserBase, SUserCompany):
    id: int = Field(description="Идентификатор пользователя")
    first_name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    status: str = Field(description="Статус пользователя")

    @computed_field
    def status_name(self) -> str:
        return self.status


class SUserSearch(BaseModel):
    id: int = Field(description="Идентификатор пользователя")


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class SUserAddDBTest(UserBase):
    password: str = Field(min_length=5, description="Пароль в формате HASH-строки")
    status: str
