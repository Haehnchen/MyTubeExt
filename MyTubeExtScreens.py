from Components.Label import Label
from Components.MenuList import MenuList
from Components.config import configfile

from BaseScreen import BaseScreen
import os

mytube_search_saved = {
  'index': 0,
  'page': 1,
  'time': 'all_time',
  'orderby': 'relevance',
}

class MyTubeExtSelcSearch(BaseScreen):
  filename = 'mytube_search.csv'
    
  skin = """
    <screen position="center,center" size="550,440" title="MyTubeExt - Search" >
            <widget name="myMenu" position="0,0" size="340,421" scrollbarMode="showOnDemand"/>
            
            <eLabel backgroundColor="#808080" position="340,0" size="1,422" />
            <eLabel backgroundColor="#808080" position="0,422" size="550,1" />
                  
            <widget name="Statusbar" position="10,428" size="530,20" font="Regular;12"/>
     
            <eLabel text="Filter" position="350,10" size="100,25" font="Regular;19" transparent="1" />
            
            <widget name="filter_alltime" position="390,30" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,27" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_blue.png" transparent="1" alphatest="on"/>            
            
            <widget name="filter_week" position="390,50" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,47" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_green.png" transparent="1" alphatest="on"/>
                        
            <widget name="filter_month" position="390,70" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,67" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_yellow.png" transparent="1" alphatest="on"/>

            <widget name="filter_today" position="390,90" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,87" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_red.png" transparent="1" alphatest="on"/>  

            <eLabel text="Order by" position="350,120" size="140,25" font="Regular;19" transparent="1" />

            <widget name="orderby_relevance" position="390,140" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,137" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_1.png" transparent="1" alphatest="on"/>
            
            <widget name="orderby_viewcount"  position="390,160" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,157" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_2.png" transparent="1" alphatest="on"/>
            
            <widget name="orderby_published" position="390,180" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,177" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_3.png" transparent="1" alphatest="on"/>
            
            <widget name="orderby_rating" position="390,200" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,197" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_4.png" transparent="1" alphatest="on"/>

            <eLabel text="Start Page" position="350,230" size="140,25" font="Regular;19" transparent="1" />
            <ePixmap position="350,250" size="45,45" zPosition="0" pixmap="skin_default/vkey_left.png" transparent="1" alphatest="on"/>
            <widget name="last_page" position="390,250" size="50,45" valign="center" halign="center" font="Regular;23" transparent="1"/>
            <ePixmap position="440,250" size="45,45" zPosition="0" pixmap="skin_default/vkey_right.png" transparent="1" alphatest="on"/>
       
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
    
    self["last_page"] = Label('')    

    self["filter_today"] = Label('')
    self["filter_week"] = Label('')
    self["filter_month"] = Label('')
    self["filter_alltime"] = Label('')

    self["orderby_relevance"] = Label('')
    self["orderby_viewcount"] = Label('')
    self["orderby_published"] = Label('')
    self["orderby_rating"] = Label('')
    
    #test = Label("all_time")   
    
    #test.
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
    
    self.setStatus()
    
    self.context = ["ChannelSelectBaseActions","WizardActions", "DirectionActions","MenuActions","NumberActions","ColorActions"]    
    
  def pageUp(self):
    self.setValue('page', self.getValue('page') + 1)        

  def pageDown(self):
    if self.getValue('page') is 1:
      self.setValue('page', 2, False)
      
    self.setValue('page', int(self.getValue('page')) - 1)        
        
  def set_time(self, value):
    self.setValue('time', value)

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

  def getValue(self, name, default = None):
    global mytube_search_saved
    return mytube_search_saved.get(name, default)

  def setValue(self, name, value, update_status = True):
    global mytube_search_saved
    mytube_search_saved[name] = value
    
    if update_status is True:
      self.setStatus()        

  def set_orderby(self, value):
    self.setValue('orderby', value)

  def setStatus(self):
    self["last_page"].text = str(self.getValue('page'))
    
    self["filter_today"].text = ('(x) ' if self.getValue('time') is "today"  else '') + _('Today')
    self["filter_week"].text = ('(x) ' if self.getValue('time') is "this_week"  else '') + _('This week')
    self["filter_month"].text = ('(x) ' if self.getValue('time') is "this_month"  else '') + _('This month')
    self["filter_alltime"].text = ('(x) ' if self.getValue('time') is "all_time"  else '') + _('All time')
    
    self["orderby_relevance"].text = ('(x) ' if self.getValue('orderby') is "relevance"  else '') + _('Relevance')
    self["orderby_viewcount"].text = ('(x) ' if self.getValue('orderby') is "viewCount"  else '') + _('View count')
    self["orderby_published"].text = ('(x) ' if self.getValue('orderby') is "published"  else '') + _('Published')
    self["orderby_rating"].text = ('(x) ' if self.getValue('orderby') is "rating"  else '') + _('Rating')    

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
    global mytube_search_saved
    
    if mytube_search_saved['index'] is 0 or len(self["myMenu"].list) is 0:
      return
    
    if(mytube_search_saved['index'] > len(self["myMenu"].list)):
      return 
    
    self["myMenu"].moveToIndex(self.getValue('index'))
    self.setStatus()

  def rebuild(self):
    self["myMenu"].setList(self.buildlist())

  def ok(self):
    selc = self["myMenu"].l.getCurrentSelection()

    # save last selection
    self.setValue('index', self["myMenu"].l.getCurrentSelectionIndex())
    self.close(selc[-1], mytube_search_saved)
