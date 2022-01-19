#!/home/students/mismap/a/ad432952/public_html/api/bin/python3

from wsgiref.handlers import CGIHandler

from main import app

CGIHandler().run(app)
