CALL venv\Scripts\activate
echo "running tests, this requires chrome"
coverage run -m pytest
echo "produce html report of test results and coverage"
coverage html