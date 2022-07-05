import logging


def create_new_logger(logger_name, config_file):
    # Create a custom logger
    logger_path = config_file["Paths"]["abs_path"] + config_file["Paths"]["logger_folder"]
    logger_full_path = logger_path + logger_name + ".log"

    # Creating and Configuring Logger

    Log_Format = "%(levelname)s %(asctime)s - %(message)s"

    logging.basicConfig(filename=logger_full_path,
                        filemode="a",
                        format=Log_Format,
                        level=logging.INFO)

    logger = logging.getLogger()
    return logger
