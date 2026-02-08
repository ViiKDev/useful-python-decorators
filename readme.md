### Print Interceptor Logger - vk_print_interceptor_logger.py

A decorator that captures all `print()` output from a function, saves it to a log file in the `log/` folder, and keeps normal terminal output untouched. Useful for lightweight logging without changing existing `print()` calls or adding explicit logger calls to the function.
