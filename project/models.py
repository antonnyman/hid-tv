import datetime
from project import db, UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String, nullable = False)
    email = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    locale = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    given_name = db.Column(db.String(255), nullable=False)
    family_name = db.Column(db.String(255), nullable=False)
    verified_email = db.Column(db.Boolean, default=False, nullable=False)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    admin = db.Column(db.Boolean, nullable = False, default = False)
    normal = db.Column(db.Boolean, default = True)
    vab = db.Column(db.Boolean, default = False)
    vacation = db.Column(db.Boolean, default = False)
    ooo = db.Column(db.Boolean, default = False) 
    projects = db.Column(db.Text)
    lifelog_token = db.Column(db.String(255))
    lifelog_refresh_token = db.Column(db.String(255))
    lifelog_token_expires_in = db.Column(db.DateTime)

    def to_json(self):
        return dict(
            google_id = self.google_id,
            email = self.email,
            name = self.name,
            picture = self.picture,
            gender = self.gender,
            locale = self.locale,
            link = self.link,
            given_name = self.given_name,
            family_name = self.family_name,
            verified_email = self.verified_email,
            tokens = self.tokens,
            created_at = self.created_at,
            admin = self.admin,
            normal = self.normal,
            vab = self.vab,
            vacation = self.vacation,
            ooo = self.ooo,
            projects = self.projects,
            lifelog_token = self.lifelog_token,
            lifelog_refresh_token = self.lifelog_refresh_token,
            lifelog_token_expires_in = self.lifelog_token_expires_in
        )

class Page(db.Model):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key = True)
    picture = db.Column(db.String(255), unique = True, nullable = False)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    created_by = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer)

    def to_json(self):
        return dict(
            picture = self.picture,
            name = self.name,
            created_at = self.created_at,
            created_by = self.created_by,
            position = self.position
        )
        

class Reload(db.Model):
    __tablename__ = "reload"
    
    id = db.Column(db.Integer, primary_key = True)
    reload = db.Column(db.DateTime, default = datetime.datetime.now())
    reloaded = db.Column(db.Boolean, default = False)