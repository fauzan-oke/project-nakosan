from database.database import Base,engine
from models.models import User,RecipientList

print("Creating database ....")

Base.metadata.create_all(engine);