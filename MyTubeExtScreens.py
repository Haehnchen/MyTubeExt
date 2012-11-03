from Components.Label import Label
from Components.MenuList import MenuList
from Components.config import configfile
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap
from Components.config import getConfigListEntry, ConfigText
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Screen import Screen

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import SubElement, Element
from xml.dom import minidom
import re
import os

mytube_search_saved = {
  'index': 0,
  'page': 1,
  'time': 'all_time',
  'orderby': 'relevance',
}

class MyTubeExtSelcSearch(Screen):
  filename = 'mytube_search.xml'
  searches = None
    
  skin = """
    <screen position="center,center" size="550,440" title="MyTube - Search" >
            <widget name="myMenu" position="10,10" size="320,401" scrollbarMode="showOnDemand"/>
            
            <eLabel backgroundColor="#808080" position="340,0" size="1,422" />
            <eLabel backgroundColor="#808080" position="0,422" size="550,1" />
            <eLabel backgroundColor="#808080" position="340,310" size="210,1" />
                  
            <widget name="statusbar" position="10,428" size="530,20" font="Regular;12"/>
     
            <eLabel text="Filter" position="350,10" size="100,25" font="Regular;19" transparent="1" />
            
            <widget name="filter_alltime" position="390,30" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,27" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_blue.png" transparent="1" alphatest="on"/>            

            <widget name="filter_month" position="390,50" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,47" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_yellow.png" transparent="1" alphatest="on"/>

            <widget name="filter_week" position="390,70" size="140,20" font="Regular;17" transparent="1" />
            <ePixmap position="352,67" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_green.png" transparent="1" alphatest="on"/>

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

            <ePixmap position="350,317" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_menu.png" transparent="1" alphatest="on"/>
            <eLabel  position="390,320" size="200,25" text="Menu" font="Regular;19" transparent="1" />
            <ePixmap position="350,342" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_5.png" transparent="1" alphatest="on"/>
            <eLabel  position="390,345" size="200,25" text="Move up" font="Regular;19" transparent="1" />
            
            <ePixmap position="350,367" size="35,25" zPosition="0" pixmap="skin_default/buttons/key_6.png" transparent="1" alphatest="on"/>
            <eLabel  position="390,370" size="200,25" text="Move down" font="Regular;19" transparent="1" />
       
        </screen>
    """

  def __init__(self, session, args = 0):
      self.session = session
      self.args = args
      Screen.__init__(self, self.session)
      self.build()


  def getConfigDir(self, filename = None):
    if filename is None:
      return os.path.dirname(configfile.CONFIG_FILE) + '/'
    
    return os.path.dirname(configfile.CONFIG_FILE) + '/' + filename

  def getSearchFile(self):
    return self.getConfigDir(self.filename)

  def build(self):
   
    self["myMenu"] = MenuList(self.buildlist())

    # TODO: do we need to init labels?
    labels = ['last_page', 'filter_today', 'filter_week', 'filter_month' ,'filter_alltime', 'orderby_relevance', 'orderby_viewcount', 'orderby_published', 'orderby_rating', 'statusbar']
    for label in labels:
        self[label] = Label('')

    self["searchactions"] = ActionMap(["ChannelSelectBaseActions","WizardActions", "DirectionActions","MenuActions","NumberActions","ColorActions"], {
      "ok": self.ok,
      "cancel": self.cancel,
      "back": self.cancel,
      "red": lambda: self.set_time('today'),
      "green": lambda: self.set_time('this_week'),
      "yellow": lambda: self.set_time('this_month'),
      "blue": lambda: self.set_time('all_time'),
      "1": lambda: self.set_orderby('relevance'),
      "2": lambda: self.set_orderby('viewCount'),
      "3": lambda: self.set_orderby('published'),
      "4":lambda: self.set_orderby('rating'),
      "menu": self.handleMenu,
      "0": self.handleMenu,
      "5": self.MoveUp,
      "6" : self.MoveDown,
      "left": self.pageDown,
      "right": self.pageUp,
    }, -2)

    self.setStatus()

  def Save(self):
    self.searches.save()
    self.setMessage(_('Saved successfully'))

  def AddSearch(self):
    self.session.openWithCallback(self.AddSearchCallback, MyTubeExtRecordScreen)

  def AddSearchCallback(self, vals = None):

    if vals is None:
      return

    if self.is_selected() is True and self.Id() < self.searches.count():
        self.searches.add(vals, self.Id() + 1)
    else:
        self.searches.add(vals)

    self.setMessage(_('Item added'))
    self.rebuild()


  def MoveUp(self):
      if self.is_selected() is False: return

      if self.Id() is 0:
          return

      self.searches.move(self.Id(), -1)
      self.rebuild()
      self["myMenu"].moveToIndex(self.Id() - 1)


  def MoveDown(self):
      if self.is_selected() is False: return

      if self.Id() >= self.searches.count() - 1:
          return

      self.searches.move(self.Id(), self.Id() + 1)
      self.rebuild()
      self["myMenu"].moveToIndex(self.Id() + 1)


  def handleMenu(self):
      menulist = [(_("Add search"), "add_search")]
      if self.is_selected() is True:
          menulist.extend((
             (_("Edit search"), "edit_search"),
             (_("Delete search"), "delete_search"),
          ))

      menulist.extend((
          (_("Save changes"), "save_searches"),
      ))

      self.session.openWithCallback(self.openMenu, ChoiceBox, title=_("Select your Action."), list = menulist)

  def openMenu(self, answer):
      answer = answer and answer[1]
      if answer is None:
          return

      if answer is "add_search":
          self.AddSearch()
      if answer is "edit_search":
          self.EditSearch()
      if answer is "delete_search":
          self.DeleteSearch()
      if answer is "save_searches":
          self.Save()

  def EditSearch(self):
      if self.is_selected() is False: return
      vals = self.searches.getDict(self.Id())
      self.session.openWithCallback(self.EditSearchCallback, MyTubeExtRecordScreen, vals)

  def EditSearchCallback(self, vals = None):
      if vals is None: return
      if self.is_selected() is False: return

      self.searches.set(self.Id(), vals)
      self.setMessage('Item edited')
      self.rebuild()

  def DeleteSearch(self):
      if self.is_selected() is False: return
      self.session.openWithCallback(self.DeleteSearchCallback, MessageBox, _("Do you want delete this item?"), MessageBox.TYPE_YESNO)

  def DeleteSearchCallback(self, result):
      if result is False or self.Id() is None:
          return

      self.searches.remove(self.Id())
      self.setMessage('Item deleted')
      self.rebuild()

  def pageUp(self):
    self.setValue('page', self.getValue('page') + 1)        

  def pageDown(self):
    if self.getValue('page') - 1 is 0:
      return

    self.setValue('page', int(self.getValue('page')) - 1)        
        
  def set_time(self, value):
    self.setValue('time', value)

  def toggleFileVisibility(self):
    self._toggleFileVisibility(self.filename)

  def _toggleFileVisibility(self, filename):
    path = str(self.getConfigDir())

    if os.path.exists(path + filename):
      os.rename(path + filename, path + '.' + filename)
      self.setMessage('hidden')
    else:
      if os.path.exists(path + '.' + filename):
        os.rename(path + '.' + filename, path + filename)
        self.setMessage('show')

    self.searches = None
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


  def readxml(self):

      list = []

      xml_file = self.getConfigDir(self.filename)

      if self.searches is None:
          try:
              self.searches = MyTubeSearches(xml_file)
          except Exception, e:
              self.setMessage(_('Parse error on: %s' % xml_file))
              return list

      for i,line in enumerate(self.searches.getAll()):
          list.append((self.searches.getDict(i)['name']))

      return list

  def buildlist(self):
    return self.readxml()

  def reset(self):
    print 'reset'

  def Id(self):
    selc = self.CurrentSelection()
    if selc is None:
        return None

    return self["myMenu"].l.getCurrentSelectionIndex()

  def layoutFinished(self):
    global mytube_search_saved
    
    if self.getValue('index') is 0 or len(self["myMenu"].list) is 0:
      return
    
    if(self.getValue('index') > len(self["myMenu"].list)):
      return 
    
    self["myMenu"].moveToIndex(self.getValue('index'))
    self.setStatus()

  def rebuild(self):
    self["myMenu"].setList(self.buildlist())

  def ok(self):
    index = self["myMenu"].l.getCurrentSelectionIndex()

    # save last selection
    self.setValue('index', index)
    self.close(self.searches.getDict(index).get('query'), mytube_search_saved)

  def setMessage(self, msg):
    self["statusbar"].text = str(msg)

  def is_selected(self):
      if self.Id() is None:
          self.setMessage(_('Please select one item'))
          return False

      return True

  def CurrentSelection(self):
      return self["myMenu"].l.getCurrentSelection()

  def cancel(self):
      self.close()

class MyTubeExtRecordScreen(ConfigListScreen, Screen):
    args = None

    skin = """
    <screen name="ConfigListScreen" position="center,center" size="560,400" title="Youtube search">
      <ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
      <ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
      <widget source="key_red" render="Label" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
      <widget source="key_green" render="Label" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
      <widget name="config" position="5,50" size="550,360" scrollbarMode="showOnDemand" zPosition="1"/>
    </screen>"""

    def __init__(self, session, args=None):
        Screen.__init__(self, session)
        ConfigListScreen.__init__(self, [])
        self.args = args

        self["key_red"] = StaticText(_("Cancel"))
        self["key_green"] = StaticText(_("OK"))

        self["key_yellow"] = StaticText("")

        self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
                {
                "red": self.cancel,
                "green": self.__SaveValues,
                "save": self.__SaveValues,
                "cancel": self.cancel,
                "ok": self.__SaveValues,
                }, -2)

        self["config"].list = self.buildlist()

    def buildlist(self):

        vals = self.args

        name = ''
        query = ''

        if not vals is None:
            name = str(vals.get('name'))
            query = str(vals.get('query'))

        fields = [
                {'name': 'name', 'field': ConfigText(fixed_size = False) , 'text': 'Name', 'value': name},
                {'name': 'query', 'field': ConfigText(fixed_size = False) , 'text': 'Search query', 'value': query},
        ]

        list = []
        for field in fields:
            field['field'].setValue(field['value'])
            list.append(getConfigListEntry(_(field['text']), field['field'], field['name']))

        return list

    def __SaveValues(self):
        values = {}
        for x in self["config"].list:
            values[x[2]] = x[1].getValue()

        self.close(values)

    def cancel(self):
        self.close()



class XmlCrud(object):

    _root = None
    _filename = None

    _node_tag = 'item'
    _node_root = 'items'
    _encoding = 'utf-8'

    def __init__(self, filename):
        self._filename = filename

        if not os.path.exists(self._filename):
            self._root = Element(self._node_root)
            return

        self._root = ET.parse(filename).getroot()

    def get(self, index):
        return self._root[index]

    def getAll(self):
        return self._root

    def getDict(self, index):
        ar = {}
        for element in self._root[index]:
            ar[element.tag] = element.text

        return ar

    def set(self, index, values):
        for key, value in values.items():
            item = self._root[index].find(key)
            if item is None:
                item = SubElement(self._root[index], key)

            item.text = value

    def add(self, values, at_index = None):
        parent = SubElement(self._root, self._node_tag)
        for key, value in values.items():
            item = SubElement(parent, key)
            item.text = value

        if not at_index is None:
            self.move(self.count() -1, at_index)

    def save(self):
        f = open( self._filename, 'w')
        f.write(self._remove_whitespace(self._prettify(self._root)))
        f.close()

    def remove(self, index):
        del self._root[index]

    def count(self):
        return len(self._root)

    def move(self, old, new):
        if new < 0:
            new = old + new

        node = self.get(old)
        self.remove(old)
        self._root.insert(new, node)

    def isInRange(self, index):
        return index <= self.count() -1

    def _prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, self._encoding)
        reparsed = minidom.parseString(rough_string)

        uglyXml = reparsed.toprettyxml(encoding = self._encoding)

        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
        return text_re.sub('>\g<1></', uglyXml)

    def _remove_whitespace(self, txt):
        return '\n'.join([x for x in txt.split("\n") if x.strip()!=''])

class MyTubeSearches(XmlCrud):

    _root = None
    _filename = None

    _node_root = 'searches'
    _node_tag = 'search'

    _default_item = {
        'name': '',
        'query': '',
        'type': 'search',
        }

    def add(self, values, at_index = None):
        super(MyTubeSearches, self).add(dict(self._default_item, **values), at_index)

    def set(self, index, values):
        super(MyTubeSearches, self).set(index, dict(self._default_item, **values))

    def getDict(self, index):
        return dict(self._default_item, **super(MyTubeSearches, self).getDict(index))