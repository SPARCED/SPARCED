#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

try:
    # Import the tqdm module
    from tqdm import tqdm

    # Initialize the progress bar
    bar = tqdm(total=100, desc="Progress")  # Adjust the total as needed

    # Save the original print function
    original_print = print
except ImportError:
    print("tqdm is not installed. Progress bar will not be shown.")
    # bypass the progress bar if tqdm is not installed
    bar = None


# Define a custom print function
def custom_print(*args, **kwargs):
    # Update the progress bar
    bar.update(1)
    # Call the original print function
    original_print(*args, **kwargs)


# Override the built-in print function
sys.modules["builtins"].print = custom_print
