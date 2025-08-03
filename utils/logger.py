import logging

def setup_logger(name="trading_bot", log_file="bot.log"):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    return logging.getLogger(name)
