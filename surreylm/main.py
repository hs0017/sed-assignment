# Application: SurreyLM
# Application Purpose: SurreyLM is a web application that allows users to manage software licenses.
# Application Author: Holly Sherlock
# Purpose of this file: This file runs the application and creates the error log.

# Importing the required modules.
from surreylm import create_app
import logging
from logging import FileHandler, WARNING

app = create_app()  # Creating the flask app.

# Creating the error log.
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run()   # Running the application.
