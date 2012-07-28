# validator import
from Plugins.Extensions.MyTube.plugin import etpm, rootkey
from Plugins.Extensions.MyTube.MyTubeService import validate_cert
from enigma import eTPM
from Screens.MessageBox import MessageBox

import plugin
from Plugins.Extensions.MyTube.MyTubeService import myTubeService

from Plugins.Extensions.MyTube.plugin import config

# devel hack to remove receiver validatecheck on ubuntu pc
class MyTubeHack(object):

  def layoutFinished(self):
    self.currList = "status"
    current = self["config"].getCurrent()
    if current[1].help_window.instance is not None:
      current[1].help_window.instance.hide()

    self.statuslist = []
    self.statuslist.append(( _("Fetching feed entries"), _("Trying to download the Youtube feed entries. Please wait..." ) ))

    # auth user
    if not config.plugins.mytube.general.username.value is "" and not config.plugins.mytube.general.password.value is "":
      myTubeService.startService()
      try:
        myTubeService.auth_user(config.plugins.mytube.general.username.value, config.plugins.mytube.general.password.value)  
      except IOError as e:
        #@TODO: check startService is running twice!?
        pass      
      except Exception as e:
        print 'Login-Error: ' + str(e)        
    
    #    self.session.openWithCallback(self.SelectSearch, MyTubeExtScreens.MyTubeExtSelcSearch)
    self["feedlist"].style = "state"
    self['feedlist'].setList(self.statuslist)
    self.Timer.start(200)
    
  def setState(self,status = None):
      if status:
        if self.FirstRun == True:
          self.appendEntries = False
          myTubeService.startService()
          
        self.currList = "status"
        self["videoactions"].setEnabled(False)
        self["searchactions"].setEnabled(False)
        self["config_actions"].setEnabled(False)
        self["historyactions"].setEnabled(False)
        self["statusactions"].setEnabled(True)
        self["ButtonBlue"].hide()
        self["VKeyIcon"].hide()  
        self.statuslist = []
        self.hideSuggestions()
  
        print "Genuine Dreambox validation passed"
        if self.FirstRun == True:
          self.appendEntries = False
          myTubeService.startService()
        if self.HistoryWindow is not None:
          self.HistoryWindow.deactivate()
          self.HistoryWindow.instance.hide()
        if status == 'getFeed':
          self.statuslist.append(( _("Fetching feed entries"), _("Trying to download the Youtube feed entries. Please wait..." ) ))
        elif status == 'getSearchFeed':
          self.statuslist.append(( _("Fetching search entries"), _("Trying to download the Youtube search results. Please wait..." ) ))
        elif status == 'Error':
          self.statuslist.append(( _("An error occured."), _("There was an error getting the feed entries. Please try again." ) ))
        elif status == 'noVideos':
          self["key_green"].show()
          self.statuslist.append(( _("No videos to display"), _("Please select a standard feed or try searching for videos." ) ))
        elif status == 'byPass':
          self.statuslist.append(( _("Not fetching feed entries"), _("Please enter your search term." ) ))
          self["feedlist"].style = "state"
          self['feedlist'].setList(self.statuslist)
          self.switchToConfigList()
        self["feedlist"].style = "state"
        self['feedlist'].setList(self.statuslist)  
        
def main(session, **kwargs):
  l2 = False
  l2cert = etpm.getCert(eTPM.TPMD_DT_LEVEL2_CERT)
  if l2cert is None:
    print "l2cert not found!!"
    #return
    
  l2key = validate_cert(l2cert, rootkey)
  if l2key is None:
    print "l2cert invalid!!"
    #return
  l2 = True
  
  try:
    session.open(plugin.MyTubePlayerMainScreenExt, l2key)    
  except:
    print 'errr'  
      