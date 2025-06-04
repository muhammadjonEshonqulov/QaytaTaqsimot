from sqlalchemy.orm import Session

from app.models.required_list import RequiredList


def seed_required_list(db: Session):
    """RequiredList jadvaliga default qiymatlarni qo‘shish."""
    default_entries = [
        "Kitobxonlik madaniyati",
        "\"5 muhim tashabbus\" doirasidagi ishtiroki",
        "Talabaning akademik ta’riflanishi",
        "Talaba xulq-atvori, ichki tartib qoidalari va odob-axloq kodeksiga rioya qilishi",
        "Xalqaro, respublika miqyosidagi olimpiadalar va sport musobaqalarida erishgan natijalari",
        "Talabaning darsga to‘liq va kechikmasdan kelishi",
        "Talabalarning \"Murabbiylar soati\"dagi faolligi",
        "Talabaning iqtidorli yoshlar toifasidagi faol ishtiroki",
        "Volontyorlik yarmarkasi ishtirokchisi",
        "Teatr va muzey, xiyobon, kino tomosha qilish, sport bilan shug‘ullanishi va sog‘lom turmush tarziga amal qilishi",
        "Ma’naviy-ma’rifiy sohaga oid boshqa yo‘nalishlardagi faolligi"
    ]

    for entry in default_entries:
        exists = db.query(RequiredList).filter_by(name=entry).first()
        if not exists:
            db.add(RequiredList(name=entry))

    db.commit()

def get_list(db: Session):
    return db.query(RequiredList).all()