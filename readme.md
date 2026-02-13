# Decorators

## Print Interceptor Logger
#### • vk_print_interceptor_logger.py

Captures all `print()` output from a function, saves it to a log file in the `log/` folder, and keeps normal terminal output untouched. Useful for lightweight logging without changing existing `print()` calls or adding explicit logger calls to the function.

## Runtime Type Validator
#### • vk_hintcheck.py

Validates function parameter types and return types at runtime based on type annotations. Raises errors when the actual values do not match the declared types.
