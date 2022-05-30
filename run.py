from api import create_app
from api.models.models import User, Order

app = create_app('development')


if __name__ == '__main__':
    app.run()
