"""SQLAlchemy models for the SeatDesk seat-inventory database."""
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="passenger")


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    origin: Mapped[str] = mapped_column(String(50), nullable=False)
    destination: Mapped[str] = mapped_column(String(50), nullable=False)
    distance_km: Mapped[int] = mapped_column(Integer, nullable=False)


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    route_id: Mapped[int] = mapped_column(Integer, ForeignKey("routes.id"), nullable=False)
    operator: Mapped[str] = mapped_column(String(50), nullable=False)
    departure_at: Mapped[str] = mapped_column(String(19), nullable=False)
    bus_type: Mapped[str] = mapped_column(String(20), nullable=False)
    fare_inr: Mapped[int] = mapped_column(Integer, nullable=False)
    total_seats: Mapped[int] = mapped_column(Integer, nullable=False)

    route: Mapped["Route"] = relationship()


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trip_id: Mapped[int] = mapped_column(Integer, ForeignKey("trips.id"), nullable=False)
    passenger_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    amount_inr: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="held")
    created_at: Mapped[str] = mapped_column(String(19), nullable=False)

    trip: Mapped["Trip"] = relationship()


class Ledger(Base):
    __tablename__ = "ledger"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[int] = mapped_column(Integer, ForeignKey("bookings.id"), nullable=False)
    entry_type: Mapped[str] = mapped_column(String(10), nullable=False)
    amount_inr: Mapped[int] = mapped_column(Integer, nullable=False)
