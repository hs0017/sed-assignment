# Application: SurreyLM
# Application Purpose: SurreyLM is a web application that allows users to manage software licenses.
# Application Author: Holly Sherlock
# Purpose of this file: This file runs the application and creates the error log.

# Importing the required modules.
from surreylm import create_app


app = create_app()  # Creating the flask app.


if __name__ == '__main__':
    app.run()  # Running the application.
