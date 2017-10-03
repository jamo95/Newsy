from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from . import article       # NOQA
from . import keyword       # NOQA
from . import review        # NOQA
from . import sentence      # NOQA
from . import word          # NOQA
