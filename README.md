# HOW TO RUN THIS APPLICATION

## This project requires Python 3.6 to run

## All code used to train the models can be found in /training

  1. Clone the repo!

    git clone https://github.com/sheastyermines/ml_baseball.git
    cd ml_baseball

  2. Create a venv (pip3 if necessary)

    sudo pip install virtualenv
    python3 -m venv venv

  3. Activate the virtual environment

    . venv/bin/activate

  4. Install the dependencies (pip3 if necessary)

    pip install -r requirements.txt

  5. Run the APPLICATION

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run --without-threads

  6. Navigate to the web page

    localhost.com:5000/app/home

Any questions or troubleshooting help may be directed to sheastyer@mymail.mines.edu
