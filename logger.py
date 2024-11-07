import logging

# Custom logger creation
def setup_custom_logger(name):
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the log level
    
    # Check if handlers already exist to avoid duplication
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)  # Set the log level

        # Create handlers
        console_handler = logging.StreamHandler()  # Log to console
        file_handler = logging.FileHandler(f'logs/{name}.log')  # Log to a file

        # Set the log level for handlers
        console_handler.setLevel(logging.INFO)  # Only log INFO level and above to console
        file_handler.setLevel(logging.DEBUG)    # Log all DEBUG and above messages to file

        # Create formatters and assign them to handlers
        console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    # Disable propagation to avoid duplication
    logger.propagate = False

    return logger

# Remove handlers from a specific logger
def clear_logger_handlers(logger_name):
    logger = logging.getLogger(logger_name)
    # Remove all handlers from the logger
    for handler in logger.handlers[:]:  # Copy the list to avoid mutation during iteration
        logger.removeHandler(handler)
        handler.close()  # Close the handler to free resources