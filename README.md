# HOW TO RUN THIS APPLICATION

  1. Clone the repo!

    git clone git@github.com:sheastyermines/ml_baseball.git
    cd ml_baseball

  2. Create a venv (both 'venvs' are necessary)

    sudo pip install virtualenv
    python3 -m venv venv

  3. Activate the virtual environment

    . venv/bin/activate

  4. Install the dependencies

    pip install -r requirements.txt

  5. Run the APPLICATION

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run

  6. Navigate to the web page

    localhost.com:5000/app/home
