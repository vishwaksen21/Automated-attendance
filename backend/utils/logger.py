"""
Logging utilities for the attendance system.
Provides structured logging with both file and console output.
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str,
    log_dir: Path = Path("logs"),
    log_level: str = "INFO"
) -> logging.Logger:
    """
    Set up logger with both file and console handlers.

    Args:
        name (str): Logger name (usually __name__)
        log_dir (Path): Directory to store logs
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        logging.Logger: Configured logger instance

    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Application started")
    """
    log_dir.mkdir(exist_ok=True, parents=True)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))

    # Only add handlers if logger doesn't already have them
    if not logger.handlers:
        # ==================== File Handler ====================
        # Use rotating file handler to manage log file size
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / f"{name}.log",
            maxBytes=10485760,  # 10MB
            backupCount=5,  # Keep 5 backup files
        )
        file_handler.setLevel(logging.DEBUG)

        # ==================== Console Handler ====================
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level))

        # ==================== Formatter ====================
        # Detailed format for file logging
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Simpler format for console
        console_formatter = logging.Formatter(
            "%(levelname)s - %(name)s - %(message)s"
        )

        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


class PerformanceLogger:
    """Log function execution time"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_execution_time(self, func_name: str, start_time: float, end_time: float):
        """
        Log the execution time of a function.

        Args:
            func_name (str): Name of the function
            start_time (float): Start time (from time.time())
            end_time (float): End time (from time.time())
        """
        duration = end_time - start_time
        self.logger.info(f"Function '{func_name}' executed in {duration:.2f} seconds")

        if duration > 5:
            self.logger.warning(
                f"Function '{func_name}' took longer than expected: {duration:.2f}s"
            )


# Example usage
if __name__ == "__main__":
    # Create logger
    logger = setup_logger(__name__, log_level="INFO")

    # Test logging
    logger.info("Application started")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.debug("This is a debug message")

    # Test performance logging
    import time

    perf_logger = PerformanceLogger(logger)
    start = time.time()
    time.sleep(0.5)
    end = time.time()
    perf_logger.log_execution_time("sample_function", start, end)
