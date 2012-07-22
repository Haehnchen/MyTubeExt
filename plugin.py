from Plugins.Plugin import PluginDescriptor
from Plugins.Extensions.MyTube.plugin import MyTubePlayerMainScreen
from Plugins.Extensions.MyTube.MyTubeService import myTubeService
from Components.Label import Label
import MyTubeExtScreens, MyTubeHack

class MyTubePlayerMainScreenExt(MyTubeHack.MyTubeHack, MyTubePlayerMainScreen):
  
  skin = """
    <screen name="MyTubePlayerMainScreenExt" position="0,0" size="720,576" title="MyTube - Browser111" >
      <ePixmap position="0,0" zPosition="-1" size="720,576" pixmap="~/mytubemain_bg.png" alphatest="on" transparent="1" backgroundColor="transparent"/>
      <widget name="config" zPosition="2" position="60,60" size="600,50" scrollbarMode="showNever" transparent="1" />
      <widget name="result" position="300,60" zPosition="3" size="350,50" font="Regular;21" transparent="1" backgroundColor="transparent" halign="right"/>
      <widget source="feedlist" render="Listbox" position="49,110" size="628,385" zPosition="1" scrollbarMode="showOnDemand" transparent="1" backgroundPixmap="~/list_bg.png" selectionPixmap="~/list_sel.png" >
        <convert type="TemplatedMultiContent">
        {"templates":
          {"default": (77,[
              MultiContentEntryPixmapAlphaTest(pos = (0, 0), size = (100, 75), png = 4), # index 4 is the thumbnail
              MultiContentEntryText(pos = (100, 1), size = (500, 22), font=0, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 1), # index 1 is the Title
              MultiContentEntryText(pos = (100, 24), size = (300, 18), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 5), # index 5 is the Published Date
              MultiContentEntryText(pos = (100, 43), size = (300, 18), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 6), # index 6 is the Views Count
              MultiContentEntryText(pos = (400, 24), size = (200, 18), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 7), # index 7 is the duration
              MultiContentEntryText(pos = (400, 43), size = (200, 18), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 8), # index 8 is the ratingcount
            ]),
          "state": (77,[
              MultiContentEntryText(pos = (10, 1), size = (560, 28), font=2, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 0), # index 0 is the name
              MultiContentEntryText(pos = (10, 22), size = (560, 46), font=3, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 1), # index 2 is the description
            ])
          },
          "fonts": [gFont("Regular", 22),gFont("Regular", 18),gFont("Regular", 26),gFont("Regular", 20)],
          "itemHeight": 77
        }
        </convert>
      </widget>

      <ePixmap pixmap="skin_default/buttons/key_info.png" position="50,500" zPosition="4" size="35,25" alphatest="on" transparent="1" />
      <ePixmap pixmap="skin_default/buttons/key_menu.png" position="50,520" zPosition="4" size="35,25" alphatest="on" transparent="1" />
      <ePixmap position="90,500" size="100,40" zPosition="4" pixmap="~/plugin.png" alphatest="on" transparent="1" />
      <ePixmap position="190,500" zPosition="4" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
      <ePixmap position="330,500" zPosition="4" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
      <ePixmap position="470,500" zPosition="4" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
      <widget name="key_red" position="190,500" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
      <widget name="key_green" position="330,500" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
      <widget name="key_yellow" position="470,500" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
      <widget name="ButtonBlue" pixmap="skin_default/buttons/button_blue.png" position="610,510" zPosition="10" size="15,16" transparent="1" alphatest="on" />
      <widget name="VKeyIcon" pixmap="skin_default/vkey_icon.png" position="620,495" zPosition="10" size="60,48" transparent="1" alphatest="on" />
      <widget name="thumbnail" position="0,0" size="100,75" alphatest="on"/> # fake entry for dynamic thumbnail resizing, currently there is no other way doing this.
      <widget name="HelpWindow" position="160,255" zPosition="1" size="1,1" transparent="1" alphatest="on" />
    </screen>"""    
  
  context = ["WizardActions"]
  
  def __init__(self, session, l2key):
    super(MyTubePlayerMainScreenExt, self ).__init__(session, l2key)
  
    self["result"] = Label("")

  #def keyOK(self):
  #  self.session.openWithCallback(self.SelectSearch, MyTubeExtScreens.MyTubeExtSelcSearch)

  def keyRight(self):
    self.session.openWithCallback(self.SelectSearch, MyTubeExtScreens.MyTubeExtSelcSearch)

  def handleHistory(self):
    self.session.openWithCallback(self.SelectSearch, MyTubeExtScreens.MyTubeExtSelcSearch)
  
  def SelectSearch(self, back = None, vals = {}):
    if back is None: return
    vals['startIndex'] = (int(vals.get('page', 1)) * 25) - 25
    
    #first page
    if vals['startIndex'] == 0:
      vals['startIndex'] = 1
      
    self.searchFeed(back, vals)

  def gotFeed(self, feed):
    super(MyTubePlayerMainScreenExt, self ).gotFeed(feed)
    total = myTubeService.getTotalResults()
    page = myTubeService.getCurrentPage()
    text = _("Results: %s - Page: %s " % (str(total), str(page)))
    self["result"].setText(text)

  #def keyOK(self):
  #  current = self["feedlist"].getCurrent()[0]
  #  self.getUserVideos(current)
  
def Plugins(path,**kwargs):
    global plugin_path
    plugin_path = path
    return [
        PluginDescriptor(name="ATube", description="Cloudy",where = PluginDescriptor.WHERE_PLUGINMENU, fnc=MyTubeHack.main),
        PluginDescriptor(name="ATube", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=MyTubeHack.main)
        ]
