#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from github import Github
import json, sys, cgi, ConfigParser

CONFIG_SECTION = "config"
CONFIG_PORT = "port"
CONFIG_BRANCHES_FILE_PATH = "branches_file_path"
CONFIG_GITHUB_TOKEN = "github_token"

class myHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    if self.path == "/status":
      mimetype = 'text/html'
      self.send_response(200)
      self.send_header('Content-type', mimetype)
      self.end_headers()
      self.wfile.write("Ok")

  def do_POST(self):
    if self.path == "/update-branches":
      # load and parse Github JSON payload
      form = cgi.FieldStorage(
        fp = self.rfile, 
        headers = self.headers,
        environ = { 'REQUEST_METHOD':'POST', })

      payload = form["payload"].value
      data = json.loads(payload)
      ownerName = data["repository"]["owner"]["name"]
      repoName = data["repository"]["name"]

      # get branch list via Github API
      g = Github(GITHUB_TOKEN)
      branches = g.get_repo(ownerName + "/" + repoName).get_branches()

      # update relevant branch list file
      branchesFile = open(BRANCHES_FILE_PATH + "/" + repoName + ".branches", "w")
      branchesFile.write("BRANCHES=")
      for branch in branches:
        branchesFile.write(branch.name + ",")

      branchesFile.close()

      self.send_response(200)
      self.end_headers()
      self.wfile.write("{\"status\":\"success\"}")
      
# parse config files and then start the server
config_file = "github-branches-updater.cfg"
if len(sys.argv) == 2:
  config_file = sys.argv[1]

config = ConfigParser.SafeConfigParser()
config.read(config_file)

if config.has_option(CONFIG_SECTION, CONFIG_PORT) and config.has_option(CONFIG_SECTION, CONFIG_BRANCHES_FILE_PATH) and config.has_option(CONFIG_SECTION, CONFIG_GITHUB_TOKEN):
  try:
    PORT_NUMBER = config.getint(CONFIG_SECTION, CONFIG_PORT)
    BRANCHES_FILE_PATH = config.get(CONFIG_SECTION, CONFIG_BRANCHES_FILE_PATH)
    GITHUB_TOKEN = config.get(CONFIG_SECTION, CONFIG_GITHUB_TOKEN)
  except:
    print "Error in parsing the configuration file!"
    sys.exit(1)
else:
  print "Missing properties in configuration file!"
  sys.exit(1)

try:
  server = HTTPServer(('', PORT_NUMBER), myHandler)
  print 'Started HTTP server on port', PORT_NUMBER
  
  server.serve_forever()

except KeyboardInterrupt:
  print '^C received, shutting down the HTTP server'
  server.socket.close()
