from .base import db


# ==================================================================
# Database table definitions
# ==================================================================

class Kfi(db.Model):
    __tablename__ = "Kfi"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000), nullable=True)
    calculation = db.Column(db.String(2000), nullable=False)
    intrinsic_threshold = db.Column(db.String(2000),nullable=False)

    
    def __repr__(self):
        return '<id %r>' % self.id

# ==================================================================
# App object definition
# ==================================================================

class Kfi_:
    def __init__(self, some_params):
        # set a bunch of class properties
        # self.thing = some_params you pass in 
        return None

def some_method(some_param):
    # call the class you made
    # ref_to_Kfi_class = Kfi()
    # Stuff
    return None