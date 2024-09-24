from app import db
from app.models import User

admin_user = User(username='admin', email='admin@example.com')
admin_user.set_password('your_admin_password')
admin_user.is_admin = True
db.session.add(admin_user)
db.session.commit()

print("Admin user created successfully.")
