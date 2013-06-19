jenkins-github-branches-updater
===============================

This simple Python server receives GitHub's payload via the post-receive hook and subsequently updates the branch list for the repository specified in the payload. It coincides with the set up on the Jenkins side utilising the Extended Choice Parameter plugin to allow for the list of branches to be populated as a drop down in a Jenkins job (as documented here: https://www.sourceprojects.org/default/2012/12/22/1356192120000.html)

Steps to get it up and running:

1. Install `pip install PyGithub` (Python module used in this script)
2. Edit the configuration file with the path to save the branches to, your GitHub token, port to run on.
3. Start it with `python github-branches-updater.py`. Path to the config file can be specified as an argument.


