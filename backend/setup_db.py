from app import app
from extensions import db
from app import User

with app.app_context():
    db.create_all()
    
def create_user(username, email, password_hash):
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user is None:
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} created successfully.")
    else:
        print(f"User with this username ({username}) or email ({email}) already exists.")

def remove_user(username):
    user_to_remove = User.query.filter_by(username=username).first()
    if user_to_remove:
        db.session.delete(user_to_remove)
        db.session.commit()
        print(f"User {username} removed successfully.")
    else:
        print(f"User {username} does not exist.")

# Create the database and the database table
with app.app_context():
    db.create_all()

    # Remove the test user if it exists
    remove_user('testuser')

    # Example of creating a new user
    create_user('newuser', 'newuser@example.com', 'hashedpassword')
