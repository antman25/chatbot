import difflib
import inspect
import logging
import re
import traceback
from datetime import datetime
from threading import RLock

from collections.abc import Mapping
from multiprocessing.pool import ThreadPool

#from errbot import CommandError
#from errbot.flow import FlowExecutor, FlowRoot
#from .backends.base import Backend, Room, Identifier, Message
from .storage import StoreMixin
#from .streaming import Tee
#from .templating import tenv
#from .utils import split_string_after

log = logging.getLogger(__name__)


# noinspection PyAbstractClass
class ChatBot(Backend, StoreMixin):
    """ ErrBot is the layer taking care of commands management and dispatching.
    """
    __errdoc__ = """ Commands related to the bot administration """
    MSG_ERROR_OCCURRED = 'Computer says nooo. See logs for details'
    MSG_UNKNOWN_COMMAND = 'Unknown command: "%(command)s". '
    startup_time = datetime.now()

    def __init__(self, bot_config):
        log.debug("ErrBot init.")
        super().__init__(bot_config)
        self.bot_config = bot_config
        self.prefix = bot_config.BOT_PREFIX
        if bot_config.BOT_ASYNC:
            self.thread_pool = ThreadPool(bot_config.BOT_ASYNC_POOLSIZE)
            log.debug('created a thread pool of size %d.', bot_config.BOT_ASYNC_POOLSIZE)
        self.commands = {}  # the dynamically populated list of commands available on the bot
        self.re_commands = {}  # the dynamically populated list of regex-based commands available on the bot
        self.command_filters = []  # the dynamically populated list of filters
        self.MSG_UNKNOWN_COMMAND = 'Unknown command: "%(command)s". ' \
                                   'Type "' + bot_config.BOT_PREFIX + 'help" for available commands.'
        if bot_config.BOT_ALT_PREFIX_CASEINSENSITIVE:
            self.bot_alt_prefixes = tuple(prefix.lower() for prefix in bot_config.BOT_ALT_PREFIXES)
        else:
            self.bot_alt_prefixes = bot_config.BOT_ALT_PREFIXES
        self.repo_manager = None
        self.plugin_manager = None
        self.storage_plugin = None
        self._plugin_errors_during_startup = None
        self.flow_executor = FlowExecutor(self)
        self._gbl = RLock()  # this protects internal structures of this class
