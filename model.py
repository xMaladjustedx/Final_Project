from google.appengine.ext import ndb


class Message(ndb.Model):
    song_name = ndb.StringProperty()
    artist = ndb.StringProperty(default="")
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)



