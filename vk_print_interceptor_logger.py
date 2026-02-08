import builtins
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
import os

_default_print = builtins.print
DISABLE_LOGS = False
LOG_AND_PRINT = True

#? Log Levels
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

class PrintLogger():
	def __init__(self, log_path='logs/vk_logger.log', formatter_string='%(asctime)s - %(levelname)s - %(message)s', default_level=logging.INFO):
		self._default_level = default_level
		self.logger = logging.getLogger('vk_logger')
		self.logger.setLevel(default_level)

		os.makedirs('/'.join(log_path.split('/')[:-1]), exist_ok=True)
		handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3)
		formatter = logging.Formatter(formatter_string)
		handler.setFormatter(formatter)

		self.logger.addHandler(handler)
		self.logger.propagate = False  # Prevent propagation to root logger

	def _print_interceptor(self, log_level):
		def inner_print(*args, sep=' ', end='\n', **kwargs):
			message = sep.join(str(arg) for arg in args) + end
			if LOG_AND_PRINT:
				_default_print(message.strip())
			self.logger.log(log_level, message.strip())
		return inner_print

	def log(self, disabled=False, log_level=None, _force=False):
		def decorator(func):
			@wraps(func)
			def wrapper(*args, **kwargs):
				if DISABLE_LOGS and not _force:
					return func(*args, **kwargs)
				level = log_level if log_level is not None else self._default_level
				if not disabled:
					builtins.print = self._print_interceptor(level)
				try:
					return func(*args, **kwargs)
				except Exception as e:
					self.logger.exception('Unhandled exception in %s: %s', func.__name__, e)
				finally:
					builtins.print = _default_print

			return wrapper
		return decorator

	def force_log(self, log_level=None):
		# Log even if DISABLED_LOGS is set to True
		return self.log(log_level=log_level, _force=True)

	def log_print(self, message, level=None):
		#! DISABLE LOG PRINTS WHEN LOG IS DISABLED
		level = level or self._default_level
		self.logger.log(level, message)

	# #? This makes the instance usable in "with" statements - Ex: "with log(...)"
	# def __call__(self, disabled=False, log_level=None):
	# 	level = log_level if log_level is not None else self._default_level
	# 	if disabled:
	# 		return self._noop_context()
	# 	return self._logging_context(level)

	# class _noop_context:
	# 	def __enter__(self): pass
	# 	def __exit__(self, exc_type, exc_val, exc_tb): pass

	# class _logging_context:
	# 	def __init__(self, level):
	# 		self.level = level

	# 	def __enter__(self):
	# 		self._previous = builtins.print
	# 		builtins.print = logger._print_interceptor(self.level)

	# 	def __exit__(self, exc_type, exc_val, exc_tb):
	# 		builtins.print = _default_print

# Create an instance and expose the log method

logger = PrintLogger()
log = logger.log  #* <- Shortcut to use as @log
force_log = logger.force_log  #* <- Shortcut to use as @force_log
log_print = logger.log_print #* <- Function to print with different log level
