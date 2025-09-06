import io
import csv
from typing import List
from datetime import datetime, date, timedelta, timezone
from app.schemas.analytics import ActivityItem, ActivityType
from app.services.bookings import bookings_db
from app.services.astra import transactions_db


async def get_activity_feed(user_id: str) -> List[ActivityItem]:
    """
    Constructs a user's activity feed from various sources.
    """
    activities = []

    # Process bookings from the in-memory db
    for booking_id, booking in bookings_db.items():
        if user_id in (booking.client_id, booking.freelancer_id):
            is_client = booking.client_id == user_id
            description = ""
            if is_client:
                description = f"Booking with {booking.freelancer_id}"
            else:
                description = f"Booking by {booking.client_id}"

            activities.append(ActivityItem(
                id=booking.id,
                type=ActivityType.BOOKING,
                timestamp=booking.start_time,
                description=description,
                amount=booking.price,
                status=booking.status.value,
            ))

    # Process transactions from the in-memory db
    for tx in transactions_db:
        details = tx['details']
        action = tx['action']
        activity_type = None
        description = ""
        user_is_involved = False

        if action == 'send_load':
            activity_type = ActivityType.LOAD
            if details.get('sender_id') == user_id:
                user_is_involved = True
                description = f"Sent load to {details.get('recipient_id')}"
            elif details.get('recipient_id') == user_id:
                user_is_involved = True
                description = f"Received load from {details.get('sender_id')}"

        elif action == 'request_load':
            activity_type = ActivityType.REQUEST
            if details.get('requester_id') == user_id:
                 user_is_involved = True
                 description = f"Requested load from {details.get('sender_id')}"
            elif details.get('sender_id') == user_id:
                 user_is_involved = True
                 description = f"Load requested by {details.get('requester_id')}"

        elif action == 'swap_funds':
            activity_type = ActivityType.SWAP
            if details.get('source_id') == user_id:
                user_is_involved = True
                description = f"Swapped funds to {details.get('destination_id')}"
            elif details.get('destination_id') == user_id:
                user_is_involved = True
                description = f"Received swapped funds from {details.get('source_id')}"

        if user_is_involved:
            activities.append(ActivityItem(
                id=details.get('transaction_id'),
                type=activity_type,
                timestamp=tx['timestamp'],
                description=description,
                amount=details.get('amount'),
                status=tx.get('status'),
            ))

    # Sort activities by timestamp in reverse chronological order
    activities.sort(key=lambda x: x.timestamp, reverse=True)

    return activities


async def get_revenue_projections(user_id: str):
    """
    Calculates projected revenue from confirmed future bookings.
    """
    projected_revenue = 0.0
    booking_count = 0
    now = datetime.now(timezone.utc)

    for booking_id, booking in bookings_db.items():
        # Projections are for freelancers receiving payment
        if booking.freelancer_id == user_id:
            # Convert booking start_time to offset-aware by assuming UTC
            if booking.status == "confirmed" and booking.start_time.replace(tzinfo=timezone.utc) > now:
                projected_revenue += booking.price
                booking_count += 1

    return {"projected_revenue": projected_revenue, "from_booking_count": booking_count}


async def get_income_trend(user_id: str, start_date: date, end_date: date):
    """
    Calculates income, expenses, and net income over a date range.
    """
    trend_data = {}

    # Initialize data points for the date range
    current_date = start_date
    while current_date <= end_date:
        trend_data[current_date] = {"income": 0.0, "expenses": 0.0}
        current_date += timedelta(days=1)

    # Process bookings
    for booking_id, booking in bookings_db.items():
        booking_date = booking.start_time.date()
        if start_date <= booking_date <= end_date and booking.status == "confirmed":
            if booking.freelancer_id == user_id:
                trend_data[booking_date]["income"] += booking.price
            elif booking.client_id == user_id:
                trend_data[booking_date]["expenses"] += booking.price

    # Process transactions
    for tx in transactions_db:
        tx_date = tx['timestamp'].date()
        if start_date <= tx_date <= end_date and tx['status'] == "completed":
            details = tx['details']
            action = tx['action']
            amount = details.get('amount', 0.0)

            if action == 'send_load' and details.get('sender_id') == user_id:
                trend_data[tx_date]["expenses"] += amount
            elif action == 'send_load' and details.get('recipient_id') == user_id:
                 trend_data[tx_date]["income"] += amount

            # For swaps, we assume the user's perspective
            elif action == 'swap_funds' and details.get('source_id') == user_id:
                trend_data[tx_date]["expenses"] += amount
            elif action == 'swap_funds' and details.get('destination_id') == user_id:
                trend_data[tx_date]["income"] += amount

    # Format for response
    response_trend = []
    for day, data in trend_data.items():
        net_income = data['income'] - data['expenses']
        response_trend.append({
            "date": day,
            "income": data['income'],
            "expenses": data['expenses'],
            "net_income": net_income
        })

    return sorted(response_trend, key=lambda x: x['date'])


async def get_revenue_report(user_id: str, breakdown_by: str):
    """
    Generates a revenue report, broken down by client or service.
    """
    revenue_data = {}
    now = datetime.now(timezone.utc)

    # Only freelancers receive revenue from bookings
    if breakdown_by == 'service':
        for booking_id, booking in bookings_db.items():
            if booking.freelancer_id == user_id and booking.status == "confirmed" and booking.start_time.replace(tzinfo=timezone.utc) < now:
                service = booking.service
                if service not in revenue_data:
                    revenue_data[service] = {"total_revenue": 0.0, "transaction_count": 0}
                revenue_data[service]["total_revenue"] += booking.price
                revenue_data[service]["transaction_count"] += 1

    elif breakdown_by == 'client':
        for booking_id, booking in bookings_db.items():
            if booking.freelancer_id == user_id and booking.status == "confirmed" and booking.start_time.replace(tzinfo=timezone.utc) < now:
                client = booking.client_id
                if client not in revenue_data:
                    revenue_data[client] = {"total_revenue": 0.0, "transaction_count": 0}
                revenue_data[client]["total_revenue"] += booking.price
                revenue_data[client]["transaction_count"] += 1

    # Format for response
    response_report = []
    for category, data in revenue_data.items():
        response_report.append({
            "category": category,
            "total_revenue": data['total_revenue'],
            "transaction_count": data['transaction_count']
        })

    return response_report


async def generate_financial_report_csv(user_id: str):
    """
    Generates a CSV financial report for a user.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['Date', 'Description', 'Income', 'Expense', 'Category'])

    # Process bookings
    for booking_id, booking in bookings_db.items():
        if booking.status == "confirmed":
            row = None
            if booking.freelancer_id == user_id:
                row = [
                    booking.start_time.strftime('%Y-%m-%d'),
                    f"Payment for '{booking.service}' from {booking.client_id}",
                    booking.price,
                    "",
                    "Booking Revenue"
                ]
            elif booking.client_id == user_id:
                row = [
                    booking.start_time.strftime('%Y-%m-%d'),
                    f"Payment for '{booking.service}' to {booking.freelancer_id}",
                    "",
                    booking.price,
                    "Service Expense"
                ]
            if row:
                writer.writerow(row)

    # Process transactions
    for tx in transactions_db:
        if tx['status'] == "completed":
            details = tx['details']
            action = tx['action']
            amount = details.get('amount', 0.0)
            row = None

            if action == 'send_load':
                if details.get('sender_id') == user_id:
                    row = [
                        tx['timestamp'].strftime('%Y-%m-%d'),
                        f"Load sent to {details.get('recipient_id')}",
                        "",
                        amount,
                        "Funds Transfer Out"
                    ]
                elif details.get('recipient_id') == user_id:
                    row = [
                        tx['timestamp'].strftime('%Y-%m-%d'),
                        f"Load received from {details.get('sender_id')}",
                        amount,
                        "",
                        "Funds Transfer In"
                    ]

            elif action == 'swap_funds':
                 if details.get('source_id') == user_id:
                    row = [
                        tx['timestamp'].strftime('%Y-%m-%d'),
                        f"Funds swapped to {details.get('destination_id')}",
                        "",
                        amount,
                        "Swap Out"
                    ]
                 elif details.get('destination_id') == user_id:
                    row = [
                        tx['timestamp'].strftime('%Y-%m-%d'),
                        f"Funds swapped from {details.get('source_id')}",
                        amount,
                        "",
                        "Swap In"
                    ]

            if row:
                writer.writerow(row)

    output.seek(0)
    return output
