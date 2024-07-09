# view_database.py

from models import session, User, File, Image

def view_users():
    users = session.query(User).all()
    for user in users:
        print(f"User ID: {user.id}, Username: {user.username}")

def view_files():
    files = session.query(File).all()
    for file in files:
        print(f"File ID: {file.id}, Filename: {file.filename}, User ID: {file.user_id}")

def view_images():
    images = session.query(Image).all()
    for image in images:
        print(f"Image ID: {image.id}, Filename: {image.filename}, User ID: {image.user_id}")

if __name__ == "__main__":
    print("Users:")
    view_users()
    print("\nFiles:")
    view_files()
    print("\nImages:")
    view_images()
