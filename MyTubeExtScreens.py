from Components.Label import Label
from Components.MenuList import MenuList
from Components.config import configfile

from BaseScreen import BaseScreen
import os

last_index = 0
last_page = 1
last_time = 'all_time'
last_orderby = 'relevance'

class MyTubeExtSelcSearch(BaseScreen):
  filename = 'mytube_search.csv'
    
  skin = """
    <screen position="center,center" size="460,440" title="MyTubeExt - Search" >
      <widget name="myMenu" position="10,10" size="420,380" scrollbarMode="showOnDemand"/>
      <widget name="Statusbar" position="10,428" size="530,20" font="Regular;12"/>
      
            <widget name="red" position="10,394" size="120,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>
            <widget name="green" position="140,394" size="120,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>
            <widget name="yellow" position="270,394" size="120,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>
            <widget name="blue" position="400,394" size="120,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>
      

            <ePixmap name="pred" position="10,398" size="120,30" zPosition="0" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on"/>
            <ePixmap name="pgreen" position="140,398" size="120,30" zPosition="0" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on"/>
            <ePixmap name="pyellow" position="270,398" size="120,30" zPosition="0" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on"/>
            <ePixmap name="pblue" position="400,398" size="120,30" zPosition="0" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on"/>      
    </screen>
    """    
    
  def GetConfigDir(self, filename = None):
    if filename is None:
      return os.path.dirname(configfile.CONFIG_FILE) + '/'
    
    return os.path.dirname(configfile.CONFIG_FILE) + '/' + filename

  def getSearchFile(self):
    return self.GetConfigDir(self.filename)

  def build(self):
    
    self["myMenu"] = MenuList(self.buildlist())

    self["red"] = Label("today")
    self["green"] = Label("this_week")
    self["yellow"] = Label("this_month")
    self["blue"] = Label("all_time")    
    
    self.actions['red'] = lambda: self.set_time('today')
    self.actions['green'] = lambda: self.set_time('this_week')
    self.actions['yellow'] = lambda: self.set_time('this_month')
    self.actions['blue'] = lambda: self.set_time('all_time')
    
    self.actions['1'] = lambda: self.set_orderby('relevance')
    self.actions['2'] = lambda: self.set_orderby('viewCount')
    self.actions['3'] = lambda: self.set_orderby('published')
    self.actions['4'] = lambda: self.set_orderby('rating')
    self.actions['7'] = self.toggleFileVisibility
    
    self.actions['8'] = self.pageDown
    self.actions['9'] = self.pageUp
    
    self.actions['left'] = self.pageDown
    self.actions['right'] = self.pageUp
    
    self.context = ["ChannelSelectBaseActions","WizardActions", "DirectionActions","MenuActions","NumberActions","ColorActions"]    
    
  def pageUp(self):
    global last_page
    last_page = last_page + 1
    self.setStatus()

  def pageDown(self):
    global last_page
    last_page = last_page - 1
    if last_page < 1:
      last_page = 1
    self.setStatus()    
        
  def set_time(self, value):
    global last_time
    last_time = value
    self.setStatus()

  def toggleFileVisibility(self):
    path = str(self.GetConfigDir())

    if os.path.exists(path + self.filename):
      os.rename(path + self.filename, path + '.' + self.filename)
      self.SetMessage('hidden')
    else:
      if os.path.exists(path + '.' + self.filename):
        os.rename(path + '.' + self.filename, path + self.filename)
        self.SetMessage('show')    

    self.rebuild()

  def set_orderby(self, value):
    global last_orderby
    last_orderby = value
    self.setStatus()

  def setStatus(self):
    self.SetMessage(last_time + ' ' + last_orderby + ' ' + str(last_page))

  def readcsv(self):
    csv_file = self.GetConfigDir(self.filename)

    list = []
    if not os.path.exists(csv_file):
      self.SetMessage(_('File not found: %s' % csv_file))
      return list
      
    fp = open(csv_file)
    for i, line in enumerate(fp):
      row = str(line).split(',')
      row[0] = row[0].strip('"')
      row[1] = row[1].strip('"')
      row[2] = row[2].strip('"')
      if str(row[0]) == 'youtube':
        list.append((row[1], row[2]))
  
    return list

  def buildlist(self):
    return self.readcsv() 

  def reset(self):
    print 'reset'

  def layoutFinished(self):
    if last_index is 0 or len(self["myMenu"].list) is 0:
      return
    
    if(last_index > len(self["myMenu"].list)):
      return 
    
    self["myMenu"].moveToIndex(last_index)
    self.setStatus()

  def rebuild(self):
    self["myMenu"].setList(self.buildlist())

  def ok(self):
    selc = self["myMenu"].l.getCurrentSelection()
    
    # save last selection
    global last_index
    last_index = self["myMenu"].l.getCurrentSelectionIndex()
    
    back = {
            'time':last_time,
            'orderby':last_orderby,
            'page':last_page,
            }
    
    self.close(selc[-1], back)

          
 