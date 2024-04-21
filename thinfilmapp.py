import sys
from matplotlib.figure import Figure
import wx
import wx.grid
from editor import *
from project import *
from floatctrl import *

class Window(wx.Frame):
    def __init__(self, parent=None, id = -1, title = None):
        wx.Frame.__init__(self, parent, id, title)

        self.thin_film_project = ThinfilmProject()
        
        self.init_menu()
        self.init_panel()
        self.Update()
        self.Show(True)
    
    def init_panel(self):
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.Fit()
        self.sizer = wx.GridBagSizer(0,0)
 
        # note
        text_note = wx.StaticText(self.panel, label = "Notes:") 
        self.sizer.Add(text_note, pos = (0, 0), flag = wx.ALL, border = 5) 
        self.textctrl_note = wx.TextCtrl(self.panel,style = wx.TE_MULTILINE) 
        self.sizer.Add(self.textctrl_note, pos = (0,1), span = (1, 2), flag = wx.EXPAND|wx.ALL, border = 5) 
        
        # reference wavelength
        text_ref_wave = wx.StaticText(self.panel, label = "Reference Wavelength:") 
        self.sizer.Add(text_ref_wave, pos = (1, 0), flag = wx.ALL, border = 5) 
        self.textctrl_wave = FloatCtrl(self.panel)
        self.textctrl_wave.Bind(wx.EVT_TEXT, self.on_wavelength_changed)
        self.sizer.Add(self.textctrl_wave,pos=(1,1), border = 5)

        # table
        self.layer_editor = LayerStackEditor(self.panel,self.thin_film_project)
        self.sizer.Add(self.layer_editor, pos=(2,0), span = (1, 2), flag = wx.EXPAND|wx.ALL, border = 20)

        # substrate
        text_substrate = wx.StaticText(self.panel, label = "Substrate:") 
        self.sizer.Add(text_substrate, pos = (3, 0), flag = wx.ALL, border = 5) 
        self.choice_substrate = wx.Choice(self.panel, -1, choices= self.thin_film_project.glass_lib.glass_name_list())
        self.choice_substrate.SetSelection(0)
        self.sizer.Add(self.choice_substrate, pos=(3,1), border = 5)

        self.panel.SetSizerAndFit(self.sizer)
        self.Fit()
    
    def update_ui(self):
        self.panel.SetSizerAndFit(self.sizer)
        self.Fit()

    def init_menu(self):
        menu_bar = wx.MenuBar()

        file = wx.Menu()
        file.Append(1, "New")
        file.Append(2, "Quit")

        edit = wx.Menu()
        edit.Append(3, "Insert")
        edit.Append(4, "Insert Formula")

        tool = wx.Menu()
        tool.Append(5, "Plot Reflection vs Wavelength")
 
        menu_bar.Append(file, 'File')
        menu_bar.Append(edit, 'Edit')
        menu_bar.Append(tool, 'Tool')
 
        self.SetMenuBar(menu_bar)
 
        self.Bind(wx.EVT_MENU, self.click_menu)

    def click_menu(self, event):
        event_id = event.GetId()
        msg = ""
        if (event_id == 1):
            msg = "New"
        elif (event_id == 2):
            msg = "Quit"
            self.Close(True)
        elif (event_id == 3):
            msg = "Redu"
        elif (event_id == 4):
            msg = "Undo"
        elif (event_id == 5):
            self.plot_reflection_vs_wavelength()
 
        #wx.MessageBox(msg, 'Clicked')
    
    def on_wavelength_changed(self):
        wvl = float(self.textctrl_wave.GetValue())
        self.thin_film_project.layer_stack_model.wavelength = wvl
        self.layer_editor.update()

    def plot_reflection_vs_wavelength(self):
        pass
 
if __name__ == "__main__":
    app = wx.App()
    Window(None, wx.ID_ANY, "Thin Film")
    app.MainLoop()
    