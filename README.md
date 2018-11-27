<h1>Surf Lodger </h1>

<h3>Running Instructions</h3>

<p>This Project can be run using install.bat for the first time and surfLodger.bat thereafter. Some of the tests 
are dependent on installation of the project and input of the API key so make sure you've done this before running
test.bat</p>

<p>The installer creates a new virtual python environment in the repository, installs the package and it's dependencies
 including those required for testing, starts a web page and starts the application on localhost:5000. I've found that
 the web page has refreshed when the application becomes available but you may need to refresh the page if not.</p>

<p>It was run locally on a Windows machine using python 3 and flask.py's built in server. This project does not make use
of any databases. It makes use of a text file that will contain your API key however the web application will ask you
for this information, test it's functionality and generate the file for you when you first run the application.</p>

<p>If you make a mistake when entering the key, it will let you re-try if the key doesn't work and wont save it 
until it does. If you want to add a different key you can just delete the config file here:
 "instance/keys.txt"</p>

<p>If you want to change the search parameters, there is a settings menu at the top of the results list</p>

<p>All other information is described in a modal when the application is opened and can be accessed again 
at any time from the map key button at the top of the list of places</p>

<p> PHP version Currently hosted at <a href="https://surflodger.bennett-lloydtech.com/index.php">https://surflodger.bennett-lloydtech.com/index.php</a></p>
