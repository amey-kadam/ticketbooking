from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import AddMuseumForm

admin_bp = Blueprint('admin', __name__)

# Admin dashboard
@admin_bp.route('/admin_panel')
@login_required
def admin_dashboard():
    from app import db  # Import db here to avoid circular import issues
    from app.models import Museum

    if not current_user.is_admin:
        flash('Access restricted to admin only!', 'danger')
        return redirect(url_for('main.dashboard'))  # Ensure this is the correct blueprint name

    museums = Museum.query.all()
    return render_template('admin/admin_panel.html', museums=museums)


@admin_bp.route('/add_museum', methods=['GET', 'POST'])
@login_required
def add_museum():
    from app import db  # Import db here to avoid circular import issues
    from app.models import Museum

    form = AddMuseumForm()

    if form.validate_on_submit():
        # Create a new museum entry
        new_museum = Museum(
            name=form.name.data,
            state=form.state.data,
            district=form.district.data,
            city=form.city.data
        )

        # Save to the database
        db.session.add(new_museum)
        db.session.commit()

        # Flash success message
        flash('Museum added successfully!', 'success')
        return redirect(url_for('admin.add_museum'))

    return render_template('admin/add_museum.html', form=form)


# Delete museum
@admin_bp.route('/delete_museum/<int:museum_id>')
@login_required
def delete_museum(museum_id):
    from app import db  # Import db here to avoid circular import issues
    from app.models import Museum

    if not current_user.is_admin:
        flash('Access restricted to admin only!', 'danger')
        return redirect(url_for('main.dashboard'))  # Ensure this is the correct blueprint name

    museum = Museum.query.get_or_404(museum_id)
    db.session.delete(museum)
    db.session.commit()
    flash(f'Museum {museum.name} deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))
