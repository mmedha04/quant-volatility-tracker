#create structured logging so that every time script runs, key events and signals get saved in a logs/app.log file
import logging #built in python logging library
import os #creates folders and manages paths

def setup_logger(log_file = "../logs/app.log"): #sets up and returns logger object
    #check that folder exists, creates if doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok = True) #exist_ok means wont crash if alr exists

    #configure logger
    logging.basicConfig(
        filename = log_file,
        level = logging.INFO, #sets the minimum severity of logs to capturev
        format = "%(asctime)s - %(levelname)s- %(message)s" #format specifier of outputs
    )

    return logging.getLogger(__name__)
