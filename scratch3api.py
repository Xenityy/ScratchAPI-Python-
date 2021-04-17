import os,json,requests,multiprocessing,scratchapi
from urllib.request import urlopen

class Get:
  def read(url):
    return json.loads(requests.get(url).text)
  class User:
    def __init__(self,user):
      self.user=user
      self.json=Get.read('https://api.scratch.mit.edu/users/'+user)
    def id(self):
      return self.json['id']
    def scratchteam(self):
      return self.json['scratchteam']
    def joindate(self):
      return self.json['history']['joined']
    def status(self):
      return self.json['profile']['status']
    def bio(self):
      return self.json['profile']['bio']
    def country(self):
      return self.json['profile']['country']
    def messages(self):
      return Get.read('https://api.scratch.mit.edu/users/'+self.user+'/messages/count')['count']
    def projects(self):
      Info=Get.read('https://api.scratch.mit.edu/users/'+self.user+'/projects')
      ids=[]
      for project in Info:
        ids.append(project['id'])
      return ids
    def comment(self):
      Info=urlopen('https://scratch.mit.edu/site-api/comments/user/'+self.user).read().decode("utf-8")
      Message=Info[Info.index('<div class="content">'):Info.index('<span class="time"')]
      Message=Message[Message.index('>')+1:Message.index('/')-1]
      Message=Message.strip()
      Author=Info[Info.index('<a href="/users/')+16:Info.index('" id')]
      return json.loads('{"Author":"'+Author+'","Message":"'+Message+'"}')
    def favorites(self):
      Info=Get.read('https://api.scratch.mit.edu/users/'+self.user+'/favorites')
      ids=[]
      for project in Info:
        ids.append(project['id'])
      return ids
    def following(self):
      Info=Get.read('https://api.scratch.mit.edu/users/'+self.user+'/following')
      Users=[]
      for User in Info:
        Users.append(Info[User]['username'])
      return Users
    def followers(self):
      Info=Get.read('https://api.scratch.mit.edu/users/'+self.user+'/followers')
      Users=[]
      for User in Info:
        Users.append(Info[User]['username'])
      return Users
    def main(self):
      return 'Link: https://scratch.mit.edu/users/'+self.user+', Name: '+self.user+', ID: '+str(self.id())+', Scratchteam?: '+str(self.scratchteam())+', Joindate: '+str(self.joindate())

  class Project:
    def __init__(self,ProjID):
      self.ProjID=ProjID
      self.json=Get.read('https://api.scratch.mit.edu/projects/'+str(ProjID))
    def title(self):
      return self.json['title']
    def description(self):
      return self.json['description']
    def instructions(self):
      return self.json['instructions']
    def author(self):
      return self.json['author']['username']
    def created(self):
      return self.json['history']['created']
    def modified(self):
      return self.json['history']['modified']
    def shared(self):
      return self.json['history']['shared']
    def views(self):
      return self.json['stats']['views']
    def loves(self):
      return self.json['stats']['loves']
    def favorites(self):
      return self.json['stats']['favorites']
    def remixes(self):
      return self.json['stats']['remixes']
    def cloud(self):
      self.Log = Get.read('https://clouddata.scratch.mit.edu/logs?projectid='+str(self.ProjID)+'&limit=1000&offset=0')
      self.vars = {}
      for x in range(len(self.Log)):
        y = self.Log[x]
        if not '☁ ' in str(y['value']) and not y['name'][2:]in self.vars:
          self.vars.update({y['name'][2:]: y['value']})
      return self.vars
    def comment(self):
      Info=urlopen('https://scratch.mit.edu/site-api/comments/project/'+str(self.ProjID)).read().decode("utf-8")
      Message=Info[Info.index('<div class="content">'):Info.index('<span class="time"')]
      Message=Message[Message.index('>')+1:Message.index('/')-1]
      Message=Message.strip()
      Author=Info[Info.index('<a href="/users/')+16:Info.index('" id')]
      return json.loads('{"Author":"'+Author+'","Message":"'+Message+'"}')
    def main(self):
      return 'Link: https://scratch.mit.edu/projects/'+str(self.ProjID)+', Author: '+self.author()+', Name: '+self.title()+', Views: '+str(self.views())+', Favorites: '+str(self.favorites())+', Loves: '+str(self.loves())
  
  class Studio:
    def __init__(self,StudioID):
      self.StudioID=StudioID
      self.json=Get.read('https://api.scratch.mit.edu/studios/'+str(StudioID))
    def title(self):
      return self.json['title']
    def owner(self):
      return self.json['owner']
    def created(self):
      return self.json['history']['created']
    def modified(self):
      return self.json['history']['modified']
    def main(self):
      return 'Link: https://scratch.mit.edu/studios/'+str(self.StudioID)+', Title: '+self.title()+', Owner: '+self.owner()+', Last modified: '+str(self.modified())

class Send:
  def __init__(self,username,password):
    self.username=username
    self.password=password
    self.scratch=scratchapi.ScratchUserSession(username,password)
  def SetVar(self,projId,name,value):
    Info=[str(projId),'"'+self.username+'"','"'+self.password+'"','"☁ '+name+'"',str(value)]
    with open('new.js','w') as file:
      file.write('''var fs = require('fs');
var scratch = require('scratch-api');
  function cloudVariable(projId, username, password, varName, varValue) {
    scratch.UserSession.create(username, password,  function (err, user) { 
      user.cloudSession(Number(projId),  function (err, cloud) {
        cloud.set(varName, varValue);
      });
    });
  };
  cloudVariable('''+', '.join(Info)+''')''')
    os.system('node new.js')
  def cloud(self,ProjID,VarName,VarValue):
    if not str(Get.Project(ProjID).cloud()[VarName])==str(VarValue):
      x=multiprocessing.Process(target=Send.SetVar,args=[self,ProjID,VarName,VarValue])
      x.start()
      while not str(Get.Project(ProjID).cloud()[VarName])==str(VarValue):
        pass
      x.terminate()
      os.remove('new.js')
  def follow(self,user):
    self.scratch.users.follow(user)
  def unfollow(self,user):
    self.scratch.users.unfollow(user)
  def invite(self,StudioID,user):
    self.scratch._studios_invite(StudioID,user)
  def Profile(self,user,comment):
    self.scratch.users.comment(user,comment)
  def Project(self,ProjID,comment):
    self.scratch.projects.comment(ProjID,comment)
  def Studio(self,StudioID,comment):
    self.scratch.studios.send(StudioID,comment)
