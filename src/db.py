from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    User model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=False)

    # One user can upload many found items
    found_items = db.relationship("FoundItem", back_populates="user", cascade="delete")


    def __init__(self, **kwargs):
        """
        Initialize user object
        """
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.phone = kwargs.get("phone")


    def serialize(self):
        """
        Serializing user object to be returned
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone
        }
    
class FoundItem(db.Model):
    """
    Item model
    """
    __tablename__ = "found_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    date_found = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String, nullable=True)


    #linking object to the user who uploaded it
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="found_items")

    def __init__(self, **kwargs):
        """
        Initialize found_items
        """
        self.description = kwargs.get("description")
        self.location = kwargs.get("location")
        self.date_found = kwargs.get("date_found")
        self.image_url = kwargs.get("image_url")
        self.user_id = kwargs.get("user_id")


    def serialize(self):
        """
        Serializing FoundItem object to be returned
        """
        return {
            "id": self.id,
            "description": self.description,
            "location": self.location,
            "date_found": self.date_found.isoformat(),
            "image_url": self.image_url,
            "user": self.user.serialize()  
        }
