```python
from app import create_app, db
from config import Config
_app = create_app(Config)
app_context = _app.app_context()
app_context.push()
db.create_all()
```