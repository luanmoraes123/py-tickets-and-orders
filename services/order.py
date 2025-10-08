from db.models import Order, User, MovieSession, Ticket
from datetime import datetime
from django.db import transaction


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None) -> None:
    if not tickets:
        return None

    user = User.objects.get(username=username)

    if date:
        order = Order.objects.create(user=user, created_at=date)
    else:
        order = Order.objects.create(user=user)
    for ticket_data in tickets:
        ticket = Ticket(
            order=order,
            movie_session=(MovieSession.
                           objects.
                           get(id=ticket_data["movie_session"])),
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        ticket.full_clean()
        ticket.save()


def get_orders(username: str | None = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
