from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Ticket
from app import db
from app.forms import BookTicketForm

user_bp = Blueprint('user', __name__)

# User dashboard
@user_bp.route('/user/dashboard')
@login_required
def user_dashboard():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('user/dashboard.html', tickets=tickets)

# View previous tickets
@user_bp.route('/user/view_tickets')
@login_required
def view_tickets():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('user/view_tickets.html', tickets=tickets)

# Book ticket (Chatbot integration)
@user_bp.route('/user/book_ticket', methods=['GET', 'POST'])
@login_required
def book_ticket():
    form = BookTicketForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Logic to book the ticket based on chatbot interaction
        ticket = Ticket(
            museum_name=form.museum_name.data,
            date=form.date.data,
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash(f'Ticket booked for {ticket.museum_name} on {ticket.date}', 'success')
        return redirect(url_for('user.view_tickets'))

    return render_template('user/book_ticket.html', form=form)
