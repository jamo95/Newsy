import os

from flask import Flask
from flask_assets import Environment, Bundle


# Returns all .js files in root dir
def _get_js_files(root):
    files = []
    for f in os.listdir(root):
        if os.path.isfile(os.path.join(root, f)) and f.endswith('.js'):
            files.append(f)
    return files

# Returns all .scss files in root dir
def _get_css_files(root):
    files = []
    for f in os.listdir(root):
        if os.path.isfile(os.path.join(root, f)) and f.endswith('.scss'):
            files.append(f)
    return files


app = Flask(__name__)
app.config.from_object('config')

env = Environment(app)
env.load_path = [
    os.path.join(os.path.dirname(__file__), 'static', 'styles'),
    os.path.join(os.path.dirname(__file__), 'static', 'scripts'),
]

# Load JavaScript files
js_files = _get_js_files(
    os.path.join(os.path.dirname(__file__), 'static', 'scripts'))

js_bundle = Bundle(
    *js_files, filters='jsmin', output='build/scripts.min.js')
env.register('js', js_bundle)

# Load CSS files
css_files = _get_css_files(
    os.path.join(os.path.dirname(__file__), 'static', 'styles'))

css_bundle = Bundle(
    *css_files, filters='scss, cssmin', output='build/styles.css')
env.register('css', css_bundle)

# Build asset bundles.
css_bundle.build(force=True, disable_cache=True)
js_bundle.build(force=True, disable_cache=True)

from app import views   # NOQA
