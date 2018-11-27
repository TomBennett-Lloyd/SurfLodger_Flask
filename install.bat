python -m venv venv
echo "activating the new virtual environment"
CALL venv\Scripts\activate
echo "installing the flask web application"
pip install -e \
echo "running tests, this requires chrome"
coverage run -m pytest
echo "produce html report of test results and coverage"
coverage html
echo "launch application on localhost:5000"
SurfLodger