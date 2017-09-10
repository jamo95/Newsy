import os

from flask import Flask
from flask_assets import Environment, Bundle


def _get_js_files(root):
    files = []
    for f in os.listdir(root):
        if os.path.isfile(os.path.join(root, f)) and f.endswith('.js'):
            files.append(f)
    return files


app = Flask(__name__)
app.config.from_object('config')

env = Environment(app)
env.load_path = [
    os.path.join(os.path.dirname(__file__), 'static', 'styles'),
    os.path.join(os.path.dirname(__file__), 'static', 'scripts'),
]

js_files = _get_js_files(
    os.path.join(os.path.dirname(__file__), 'static', 'scripts'))

# Setup scripts bundle
js_bundle = Bundle(
    *js_files, filters='jsmin', output='build/scripts.min.js')
env.register('js', js_bundle)

# Setup styling bundle.
css_bundle = Bundle(
    'main.scss', filters='scss, cssmin', output='build/styles.css')
env.register('css', css_bundle)

# Build asset bundles.
css_bundle.build(force=True, disable_cache=True)
js_bundle.build(force=True, disable_cache=True)

from app import views   # NOQA
