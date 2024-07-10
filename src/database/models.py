from tortoise import fields
from tortoise.models import Model

from enum import Enum


class Language(str, Enum):
    RUSSIAN = "ru"
    ENGLISH = "en"
    UKRAINIAN = "uk"

    def get_language_name(self):
        """Возвращает название языка, соответствующее перечислению"""
        if not isinstance(self, Language):
            raise TypeError("Объект должен быть экземпляром класса")
        language_names = {
            self.RUSSIAN: "Русский",
            self.ENGLISH: "English",
            self.UKRAINIAN: "Українська"
        }
        return language_names.get(self, None)

    @classmethod
    def get_language_code(cls, language_name):
        """Возвращает объект enum по названию языка"""
        language_codes = {
            "Русский": cls.RUSSIAN,
            "English": cls.ENGLISH,
            "Українська": cls.UKRAINIAN
        }
        return language_codes.get(language_name, None)


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=180)
    language = fields.CharEnumField(Language)


class DayStatistic(Model):
    date = fields.DateField(pk=True)
    new_users = fields.IntField(default=0)
    downloads = fields.IntField(default=0)
    errors = fields.IntField(default=0)


class Advert(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.IntField()
    message_id = fields.IntField()
    current_number = fields.IntField(default=0)
    total_number = fields.IntField(default=10)
