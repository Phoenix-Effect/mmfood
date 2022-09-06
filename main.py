import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])    

import_or_install('flask')
import_or_install('Frozen-Flask')
import_or_install('Flask-FlatPages')

import json
from flask import Flask, render_template
from flask_frozen import Freezer
from flask_flatpages import FlatPages
import sys

# In this case, we will load templates off the filesystem.
# This means we must construct a FileSystemLoader object.
#
# The search path can be used to make finding templates by
#   relative paths much easier.  In this case, we are using
#   absolute paths and thus set it to the filesystem root.
# templateLoader = jinja2.FileSystemLoader( searchpath= os.path.join(os.getcwd(), "templates/" ))

# # An environment provides the data necessary to read and
# #   parse our templates.  We pass in the loader object here.
# templateEnv = jinja2.Environment( loader=templateLoader )

# # This constant string specifies the template file we will use.
# TEMPLATE_FILE = "home.jinja"

# # Read the template file using the environment object.
# # This also constructs our Template object.
# template = templateEnv.get_template( TEMPLATE_FILE )

# # Specify any input variables to the template as a dictionary.
# templateVars = { "title" : "Test Example",
#                  "description" : "A simple inquiry of function." }

# # Finally, process the template to produce our final text.
# outputText = template.render( templateVars )

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

data = json.load(open('static/data.json', 'r'))

@app.route("/")
def home():
    context = {
        "title": "Hello Title",
        "description": "No you",
        "reviewers": data['reviewers']
    }
    return render_template( "home.jinja", **context )

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.debug = True
        app.run()
