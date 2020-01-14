from os import path, makedirs
import importlib
import logging
import sys

from core import ChatBot
from storage.base import StoragePluginBase
from logs import format_logs
from backend_plugin_manager import BackendPluginManager
from plugin_manager import BotPluginManager




log = logging.getLogger(__name__)

HERE = path.dirname(path.abspath(__file__))
CORE_STORAGE = path.join(HERE, 'storage')

def bot_config_defaults(config):
    if not hasattr(config, 'ACCESS_CONTROLS_DEFAULT'):
        config.ACCESS_CONTROLS_DEFAULT = {}
    if not hasattr(config, 'ACCESS_CONTROLS'):
        config.ACCESS_CONTROLS = {}
    if not hasattr(config, 'BOT_PREFIX'):
        config.BOT_PREFIX = '!'
    if not hasattr(config, 'TEXT_COLOR_THEME'):
        config.TEXT_COLOR_THEME = 'light'
'''
    if not hasattr(config, 'ACCESS_CONTROLS_DEFAULT'):
        config.ACCESS_CONTROLS_DEFAULT = {}
    if not hasattr(config, 'ACCESS_CONTROLS'):
        config.ACCESS_CONTROLS = {}
    if not hasattr(config, 'HIDE_RESTRICTED_COMMANDS'):
        config.HIDE_RESTRICTED_COMMANDS = False
    if not hasattr(config, 'HIDE_RESTRICTED_ACCESS'):
        config.HIDE_RESTRICTED_ACCESS = False
    if not hasattr(config, 'BOT_PREFIX_OPTIONAL_ON_CHAT'):
        config.BOT_PREFIX_OPTIONAL_ON_CHAT = False
    if not hasattr(config, 'BOT_PREFIX'):
        config.BOT_PREFIX = '!'
    if not hasattr(config, 'BOT_ALT_PREFIXES'):
        config.BOT_ALT_PREFIXES = ()
    if not hasattr(config, 'BOT_ALT_PREFIX_SEPARATORS'):
        config.BOT_ALT_PREFIX_SEPARATORS = ()
    if not hasattr(config, 'BOT_ALT_PREFIX_CASEINSENSITIVE'):
        config.BOT_ALT_PREFIX_CASEINSENSITIVE = False
    if not hasattr(config, 'DIVERT_TO_PRIVATE'):
        config.DIVERT_TO_PRIVATE = ()
    if not hasattr(config, 'DIVERT_TO_THREAD'):
        config.DIVERT_TO_THREAD = ()
    if not hasattr(config, 'MESSAGE_SIZE_LIMIT'):
        config.MESSAGE_SIZE_LIMIT = 10000  # Corresponds with what HipChat accepts
    if not hasattr(config, 'GROUPCHAT_NICK_PREFIXED'):
        config.GROUPCHAT_NICK_PREFIXED = False
    if not hasattr(config, 'AUTOINSTALL_DEPS'):
        config.AUTOINSTALL_DEPS = True
    if not hasattr(config, 'SUPPRESS_CMD_NOT_FOUND'):
        config.SUPPRESS_CMD_NOT_FOUND = False
    if not hasattr(config, 'BOT_ASYNC'):
        config.BOT_ASYNC = True
    if not hasattr(config, 'BOT_ASYNC_POOLSIZE'):
        config.BOT_ASYNC_POOLSIZE = 10
    if not hasattr(config, 'CHATROOM_PRESENCE'):
        config.CHATROOM_PRESENCE = ()
    if not hasattr(config, 'CHATROOM_RELAY'):
        config.CHATROOM_RELAY = ()
    if not hasattr(config, 'REVERSE_CHATROOM_RELAY'):
        config.REVERSE_CHATROOM_RELAY = ()
    if not hasattr(config, 'CHATROOM_FN'):
        config.CHATROOM_FN = 'Errbot'
    if not hasattr(config, 'TEXT_DEMO_MODE'):
        config.TEXT_DEMO_MODE = True
    if not hasattr(config, 'BOT_ADMINS'):
        raise ValueError('BOT_ADMINS missing from config.py.')
    if not hasattr(config, 'TEXT_COLOR_THEME'):
        config.TEXT_COLOR_THEME = 'light'
    if not hasattr(config, 'BOT_ADMINS_NOTIFICATIONS'):
        config.BOT_ADMINS_NOTIFICATIONS = config.BOT_ADMINS
'''


def setup_bot(backend_name: str, logger, config, restore=None) -> ChatBot:
    # from here the environment is supposed to be set (daemon / non daemon,
    # config.py in the python path )

    bot_config_defaults(config)

    if hasattr(config, 'BOT_LOG_FORMATTER'):
        format_logs(formatter=config.BOT_LOG_FORMATTER)
    else:
        format_logs(theme_color=config.TEXT_COLOR_THEME)

        if config.BOT_LOG_FILE:
            hdlr = logging.FileHandler(config.BOT_LOG_FILE)
            hdlr.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)-25s %(message)s"))
            logger.addHandler(hdlr)

    logger.setLevel(config.BOT_LOG_LEVEL)

    storage_plugin = get_storage_plugin(config)

    # init the botplugin manager
    botplugins_dir = path.join(config.BOT_DATA_DIR, PLUGINS_SUBDIR)
    if not path.exists(botplugins_dir):
        makedirs(botplugins_dir, mode=0o755)

def bootstrap(bot_class, logger, config, restore=None):
    """
    Main starting point of Errbot.

    :param bot_class: The backend class inheriting from Errbot you want to start.
    :param logger: The logger you want to use.
    :param config: The config.py module.
    :param restore: Start Errbot in restore mode (from a backup).
    """
    bot = setup_bot(bot_class, logger, config, restore)

    log.debug(f'Start serving commands from the {bot.mode} backend.')
    bot.serve_forever()

def get_storage_plugin(config):
    """
    Find and load the storage plugin
    :param config: the bot configuration.
    :return: the storage plugin
    """
    storage_name = getattr(config, 'STORAGE', 'Shelf')
    spm = BackendPluginManager(config, 'errbot.storage', storage_name, StoragePluginBase, CORE_STORAGE)
    log.info('Found Storage plugin: %s.' % spm.plugin_info.name)
    return spm.load_plugin()
