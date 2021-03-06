import os
from uuid import uuid4

from sugar_odm import MongoDB

from server import server

from models.user import User


@server.listener('before_server_start')
async def before_server_start(app, loop):
    user = await User.find_one({ 'username': 'administrator' })

    if not user:
        user = await User.add({
            'username': os.getenv('SUGAR_ADMIN_USERNAME', 'administrator'),
            'password': os.getenv('SUGAR_ADMIN_PASSWORD', 'password'),
            'email': os.getenv('SUGAR_ADMIN_EMAIL', 'paul@sugarush.io'),
            'secret': str(uuid4()),
            'groups': [ 'administrator' ]
        })
        await user.send_confirmation_email()
