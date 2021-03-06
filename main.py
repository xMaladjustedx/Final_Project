#!/usr/bin/env python
import os
import jinja2
import webapp2
import model



template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class ResultHandler(BaseHandler):
    def post(self):
        song_name = self.request.get("song_name")
        artist = self.request.get("some_artist")

        msg = model.Message(song_name=song_name, artist=artist)
        msg.put()

        return self.redirect_to("message_list")

class MessageListHandler(BaseHandler):
    def get(self):
        messages = sorted(model.Message.query(model.Message.deleted == False).fetch(), key=lambda m: m.created)
        params = {"messages": messages}
        return self.render_template("message_list.html", params=params)

class MessageDetailsHandler(BaseHandler):
    def get(self, message_id):
        message = model.Message.get_by_id(int(message_id))
        params = {"message": message}
        return self.render_template("message_details.html", params=params)

class ErrorSiteHandler(BaseHandler):
    def get(self,):
        return self.render_template("error_site.html")

class PollHandler(BaseHandler):
    def post(self):
        band = self.request.get("band")
        ip_address = self.request.remote_addr

        polls = model.Poll.query(model.Poll.ip_address == ip_address).fetch()

        if polls:
            return self.redirect_to("error_site")

        else:
            msg = model.Poll(band=band, ip_address=ip_address)
            msg.put()

            polls = model.Poll.query().fetch()
            params = {"polls": polls}
            return self.render_template("poll_result.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
    webapp2.Route('/poll-result', PollHandler, name="poll_result"),
    webapp2.Route('/error-site', ErrorSiteHandler, name="error_site"),
    webapp2.Route('/message-list', MessageListHandler, name="message_list"),
    webapp2.Route('/message-list', MessageListHandler, name="msg-list"),
], debug=True)
