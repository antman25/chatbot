import logging

STORAGE = 'Shelf'  # defaults to filestorage (python shelf).

BOT_DATA_DIR = '/home/antman/projects/chatbot/data'

BOT_LOG_FILE = BOT_DATA_DIR + '/chatbot.log'

BOT_LOG_LEVEL = logging.DEBUG

BOT_EXTRA_PLUGIN_DIR = None

BACKEND = 'Mattermost'

BOT_ADMINS = ('@antman') # Names need the @ in front!

BOT_ASYNC = True

# Size of the thread pool for the asynchronous mode.
BOT_ASYNC_POOLSIZE = 10

BOT_IDENTITY = {
        # Required
        'team': 'testteam',
        'server': '10.0.0.111',
        # For the login, either
        'login': 'antbot',
        #'password': 'botpassword',
        # Or, if you have a personal access token
        'token': 'p4afay9hgfbr5xpt6qg7tydm5w',
        # Optional
        'insecure': True, # Default = False. Set to true for self signed certificates
        'scheme': 'https', # Default = https
        'port': 8065, # Default = 8065
        'timeout': 30, # Default = 30. If the webserver disconnects idle connections later/earlier change this value
        'cards_hook': 'incomingWebhookId' # Needed for cards/attachments
}

ACCESS_CONTROLS = {}

CORE_PLUGINS = None

TEXT_COLOR_THEME = 'light'
