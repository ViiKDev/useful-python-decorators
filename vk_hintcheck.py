import inspect
from functools import wraps
from typing import get_type_hints
import time

def validate_from_annotations():
	def decorator(func):
		type_hints = func.__annotations__.copy()

		check_return = 'return' in type_hints
		if check_return:
			raw_return_type = type_hints['return']
			# Convert None to NoneType if return is defined
			return_type = type(None) if raw_return_type is None else raw_return_type
		else:
			return_type = None # else set to None (don't validate)
		if not type_hints:
			return func

		sig = inspect.signature(func)
		arg_names = list(sig.parameters)

		# Precomputed positional checks
		arg_check_list = [
			(i, type_hints[name])
			for i, name in enumerate(arg_names)
			if name in type_hints
		]

		# Precomputed keyword checks
		kwarg_check_map = {
			name: type_hints[name]
			for name in arg_names
			if name in type_hints
		}

		@wraps(func)
		def wrapper(*args, **kwargs):
			for i, expected in arg_check_list:
				if i >= len(args):
					break
				if not isinstance(args[i], expected):
					raise TypeError(
						f"Argument '{arg_names[i]}' expected '{expected.__name__}', got '{type(args[i]).__name__}'"
					)

			if kwargs:
				for name, value in kwargs.items():
					expected = kwarg_check_map.get(name)
					if expected and not isinstance(value, expected):
						raise TypeError(
							f"Argument '{name}' expected '{expected.__name__}', got '{type(value).__name__}'"
						)

			result = func(*args, **kwargs)
			if not check_return:
				return result

			result_type = type(result)
			if result_type != return_type:
				raise TypeError(
					f"Expected return '{return_type.__name__}', got '{result_type.__name__}'"
				)
			return result
		return wrapper
	return decorator
