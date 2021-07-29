import re
import string
from pathlib import Path

from tinydb import TinyDB, where
from validate_email import validate_email


class Adhesion:
    DB = TinyDB(Path(__file__).resolve().parent / "db.json", indent=4, encoding="utf-8")

    def __init__(self, first_name: str, last_name: str, phone_number: str, mail: str, address: str = ""):
        self.last_name = last_name
        self.first_name = first_name
        self.phone_number = phone_number
        self.mail = mail
        self.address = address

    def __str__(self) -> str:
        return f"{self.full_name}\n{self.mail}\n{self.phone_number}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def db_instance(self):
        return Adhesion.DB.get((where("first_name") == self.first_name) & (where("last_name") == self.last_name))

    def _checks(self):
        self._check_name()
        self._check_phone()
        self._check_mail()

    def _check_name(self):
        if not (self.first_name and self.last_name):
            raise ValueError("Le prénom et le nom de famille ne peuvent pas être vide.")

        special_char = string.digits + string.punctuation.replace("-", "")
        for character in self.last_name + self.first_name:
            if character in special_char:
                raise ValueError(f"Nom {self.full_name} invalide")

    def _check_mail(self):
        if not validate_email(self.mail):
            raise ValueError(f"mail {self.mail} invalide")

    def _check_phone(self):
        phone_digit = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_digit) < 10 or not phone_digit.isdigit:
            raise ValueError(f"numéro de téléphone {phone_digit} invalide.")

    def exists(self):
        return bool(self.db_instance)

    def delete(self) -> list[int]:
        if self.exists():
            return Adhesion.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []

    def save(self) -> int:
        self._checks()
        if not self.exists():
            return Adhesion.DB.insert(self.__dict__)
        return 0

def get_all_users():
    return [Adhesion(**membre) for membre in Adhesion.DB.all()]


if __name__ == "__main__":
    toto = Adhesion("Issa", "Ballo", "0102030405", "989899@gmail.com", "1 rue du chemin vert, 78700 Pantin")

    toto.save()
