from sqlalchemy.orm import Session

from app.models.required_list import RequiredList


def seed_required_list(db: Session):
    """RequiredList jadvaliga default qiymatlarni qo‘shish."""
    default_entries = [
        "1. Kitobxonlik madaniyati (0-20)",
        "2. \"5 muhim tashabbus\" doirasidagi ishtiroki (0-20)",
        "3. Talabaning akademik ta’riflanishi (0-10)",
        "4. Talaba xulq-atvori, ichki tartib qoidalari va odob-axloq kodeksiga rioya qilishi (0-5)",
        "5. Xalqaro, respublika miqyosidagi olimpiadalar va sport musobaqalarida erishgan natijalari (0-10)",
        "6. Talabaning darsga to‘liq va kechikmasdan kelishi (0-5)",
        "7. Talabalarning \"Murabbiylar soati\"dagi faolligi (0-10)",
        "8. Talabaning iqtidorli yoshlar toifasidagi faol ishtiroki (0-5)",
        "9. Volontyorlik yarmarkasi ishtirokchisi (0-5)",
        "10. Teatr va muzey, xiyobon, kino tomosha qilish, sport bilan shug‘ullanishi va sog‘lom turmush tarziga amal qilishi (0-5)",
        "11. Ma’naviy-ma’rifiy sohaga oid boshqa yo‘nalishlardagi faolligi (0-5)",
    ]





    for entry in default_entries:
        exists = db.query(RequiredList).filter_by(name=entry).first()
        if not exists:
            db.add(RequiredList(name=entry))

    db.commit()

def get_list(db: Session):
    return db.query(RequiredList).all()