import os

js="var fs = require('fs'); \nvar scratch = require('scratch-api');\n  function cloudVariable(projId, username, password, varName, varValue) {\n    scratch.UserSession.create(username, password,  function (err, user) { \n     user.cloudSession(Number(projId),  function (err, cloud) {\n     cloud.set(varName, varValue);\n    });\n  });\n};\n\nfunction setVar() {\n  fs.readFile('communicate.txt', 'utf-8',  function(err, data) {\n    if (err) throw err;\n    let info = data.replace(/^\./gim, 'myString').split('/');\n    let projId = info[0];\n    let username = info[1];\n    let password = info[2];\n    let varName = info[3];\n    let varValue = info[4];\n    cloudVariable(projId, username, password, varName, varValue);\n  });\n};\nsetVar();"

md="# ScratchAPI-Python\n\nAn API interface for [Scratch](https://scratch.mit.edu), written in [Python](https://www.python.org/).\n## Getting Started\nTo use the api, you must log in to your scratch account:\n```python\nimport scratch3api\nscratch = scratch3api.Scratch('Username','Password')\n```\n## After Login\nThere are several things you can do after you are signed in.\n\n### Cloud\nTo get a dictionary of the cloud variables and their values:\n```python\nscratch.GetVars('Project ID')\n```\nTo get the value of an individual variable:\n```python\nscratch.GetVar('Project ID','Variable Name')\n```\nTo set a cloud variable:\n```python\nscratch.SetVar('Project ID','Variable Name','Variable Value')\n```\n\n### Following\n```python\nscratch.follow('user')\nscratch.unfollow('user')\n```\n\n### Commenting\n```python\nscratch.Comment.Profile('user','comment')\nscratch.Comment.Studio('Studio ID','comment')\nscratch.Comment.Project('Project ID','comment')\n```\n\n### Credits\nCredit to [Classfied3D](https://scratch.mit.edu/users/Classfied3D/) for helping with the cloud manipulation."

py="import os, json, requests, multiprocessing\nos.system('npm install scratch-api')\nimport scratchapi\n\ndef runJS():\n  os.system('node cloud.js')\n\nclass Scratch:\n  def __init__(self,username,password):\n    s=scratchapi.ScratchUserSession(username, password)\n    if not s.tools.verify_session():\n      raise Exception('Login Failed.')\n    self.username=username\n    self.password=password\n    self.Log={}\n  def GetVars(self, ProjID):\n    OldLog = self.Log\n    try:\n      self.Log = json.loads(requests.get('https://clouddata.scratch.mit.edu/logs?projectid='+str(ProjID)+'&limit=1000&offset=0').text)\n    except:\n      self.Log = OldLog\n    self.vars = {}\n    for x in range(len(self.Log)):\n      y = self.Log[x]\n      if not '☁ ' in str(y['value']) and not y['name'][2:]in self.vars:\n        self.vars.update({y['name'][2:]: y['value']})\n    return self.vars\n  def GetVar(self,ProjID,VarName):\n    info=self.GetVars(ProjID)\n    return info[VarName]\n  def GetMessages(self,user):\n    self.s.users.get_message_count(user)\n  def SetVar(self,ProjID,VarName,VarValue):\n    with open('communicate.txt', 'w') as file:\n      file.write(str(ProjID)+'/'+self.username+'/'+self.password+'/☁ '+VarName+'/'+str(VarValue))\n    process = multiprocessing.Process(target=runJS)\n    process.start()\n    while not str(self.GetVar(ProjID,VarName)) == str(VarValue):\n      pass\n    process.terminate()\n  def Follow(self,user):\n    self.s.users.follow(user)\n  def Unfollow(self,user):\n    self.s.users.unfollow(user)\n  class Comment:\n      def Profile(self,user,comment):\n        self.s.users.comment(user,comment)\n      def Studio(self,StudioID,comment):\n        self.s.studios.comment(StudioID,comment)\n      def Project(self,ProjID,comment):\n        self.s.projects.comment(ProjID,comment)"

def Install():
  os.system('npm install scratch-api')
  with open("cloud.js", "w") as file:
    file.write(js)
  with open("README.md","w") as file:
    file.write(md)
  with open("scratch3api.py","w") as file:
    file.write(py)
  os.remove("Installer.py")
