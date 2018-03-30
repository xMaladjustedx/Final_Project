from google.appengine.ext import ndb


class Message(ndb.Model):
    message_text = ndb.StringProperty()
    author = ndb.StringProperty(default="")
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)



