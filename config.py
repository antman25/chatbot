import logging

STORAGE = 'Shelf'  # defaults to filestorage (python shelf).

BOT_DATA_DIR = '/home/antman/projects/chatbot/data'

BOT_LOG_FILE = BOT_DATA_DIR + '/chatbot.log'

BOT_LOG_LEVEL = logging.INFO

BACKEND = 'Mattermost'

BOT_ADMINS = ('@yourname') # Names need the @ in front!

BOT_ASYNC = True

# Size of the thread pool for the asynchronous mode.
BOT_ASYNC_POOLSIZE = 10

BOT_IDENTITY = {
        # Required
        'team': 'nameoftheteam',
        'server': 'mattermost.server.com',
        # For the login, either
        'login': 'bot@email.de',
        'password': 'botpassword',
        # Or, if you have a personal access token
        'token': 'YourPersonalAccessToken',
        # Optional
        'insecure': False, # Default = False. Set to true for self signed certificates
        'scheme': 'https', # Default = https
        'port': 8065, # Default = 8065
        'timeout': 30, # Default = 30. If the webserver disconnects idle connections later/earlier change this value
        'cards_hook': 'incomingWebhookId' # Needed for cards/attachments
}

ACCESS_CONTROLS = {}

TEXT_COLOR_THEME = 'light'
