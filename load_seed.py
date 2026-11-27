"""Repeatable seed loader.  Usage: python load_seed.py"""
import bcrypt
from sqlalchemy import text

import seed_data
from db import Base, SessionLocal, engine
from models import Booking, Ledger, Route, Trip, User

TABLES = ["users", "routes", "trips", "bookings", "ledger"]


def load():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = seed_data.build()

    # Hash once; every seeded user shares the demo password. The plain text is never stored.
    password_hash = bcrypt.hashpw(data["demo_password"].encode(), bcrypt.gensalt()).decode()

    with SessionLocal() as db:
        db.add_all(User(password_hash=password_hash, **u) for u in data["users"])
        db.flush()
        db.add_all(Route(**r) for r in data["routes"])
        db.flush()
        db.add_all(Trip(**t) for t in data["trips"])
        db.flush()
        db.add_all(Booking(**b) for b in data["bookings"])
        db.flush()
        db.add_all(Ledger(id=i, **e) for i, e in enumerate(data["ledger"], start=1))
        db.commit()

        if engine.dialect.name == "postgresql":
            # Explicit ids do not advance PostgreSQL sequences; move them past the seeded rows.
            for table in TABLES:
                db.execute(text(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                                f"(SELECT MAX(id) FROM {table}))"))
            db.commit()

        counts = {name: db.execute(text(f"SELECT COUNT(*) FROM {name}")).scalar_one()
                  for name in TABLES}

    print("loaded: " + " ".join(f"{k}={v}" for k, v in counts.items()))


if __name__ == "__main__":
    load()
