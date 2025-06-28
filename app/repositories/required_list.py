from sqlalchemy.orm import Session

from app.models.required_list import RequiredList


def seed_required_list(db: Session):
    """RequiredList jadvaliga default qiymatlarni qo‘shish."""
    default_entries = [
        "1. Kitobxonlik madaniyati (0-20)",
        "2. \"5 muhim tashabbus\" doirasidagi ishtiroki (0-20)",
        "3. Talabaning akademik o'zlashtirishi (0-10)",
        "4. Talabaning oliy ta'lim tashkilotining ichki tartib qoidalari va Odob-axloq kodeksiga rioya etishi (0-5)",
        "5. Xalqaro, respublika, viloyat miqyosidagi ko'rik-tanlov, fan olimpiadalari va sport musobaqalarida erishgan natijalari (0-10)",
        "6. Talabaning darslarga to‘liq va kechikmasdan kelishi (0-5)",
        "7. Talabalarning \"Ma'rifat darslari\"dagi faol ishtiroki (0-10)",
        "8. Volontyorlik va jamoat ishlaridagi faolligi (0-5)",
        "9. Teatr va muzey, xiyobon, kino, tarixiy qadamjolarga tashriflar (0-5)",
        "10. Talabalarning sport bilan shug‘ullanishi va sog'lom turmush tarziga amal qilishi (0-5)",
        "11. Ma’naviy-ma’rifiy sohaga oid boshqa yo‘nalishlardagi faolligi (0-5)",
    ]





    for entry in default_entries:
        exists = db.query(RequiredList).filter_by(name=entry).first()
        if not exists:
            db.add(RequiredList(name=entry))

    db.commit()

def get_list(db: Session):
    return db.query(RequiredList).all()