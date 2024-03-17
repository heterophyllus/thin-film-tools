from enum import IntEnum
import wx
import wx.grid
from project import *

class COLUMN(IntEnum):
    # table column
    MATERIAL = 0
    REFRACTIVE_INDEX = 1
    EXTINCTION_COEFFICIENT = 2
    OPTICAL_THICKNESS = 3
    PHYSICAL_THICKNESS = 4

class LayerStackEditor(wx.grid.Grid):

    def __init__(self, parent=None, project=None):
        super().__init__(parent)

        self.thin_film_project = project

        column_labels = ['Material', 
                        'Refractive Index', 
                        'Extinction Coefficient', 
                        'Optical Thickness[FWOT]', 
                        'Physical Thickness[nm]']
        
        self.CreateGrid(1,len(column_labels))

        # columns
        for col,label in enumerate(column_labels):
            self.SetColLabelValue(col, label)
        
        self.AutoSizeColumns(True)
        self.set_row_property(0)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.update)

        # pop up menu
        menu_item_texts = ['Insert', 'Remove']
        self.popup_menu = wx.Menu()
        for text in menu_item_texts:
            item = self.popup_menu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.on_popup_item_selected, item)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.show_popup_menu)
    
    def on_popup_item_selected(self, event):
        item = self.popup_menu.FindItemById(event.GetId())
        text = item.GetItemLabelText()
        if text == 'Insert':
            self.insert_row(self.GetGridCursorRow())

    def show_popup_menu(self, event):
        pos = event.GetPosition()
        self.PopupMenu(self.popup_menu, pos)

    def insert_row(self, row:int):
        self.InsertRows(row)
        self.set_row_property(row)


    def set_row_property(self, row:int):
        material_name_list = self.thin_film_project.material_lib.get_material_name_list()
        choice_editor = wx.grid.GridCellChoiceEditor(material_name_list, False)
        self.SetCellEditor(row, COLUMN.MATERIAL, choice_editor)
        self.SetCellValue(row, COLUMN.MATERIAL, material_name_list[0])

        for col in range(COLUMN.REFRACTIVE_INDEX, COLUMN.PHYSICAL_THICKNESS+1):
            self.SetCellRenderer(row, col, wx.grid.GridCellFloatRenderer(precision=4))
            self.SetCellValue(row, col, str(0.0))

        self.SetReadOnly(row, COLUMN.EXTINCTION_COEFFICIENT, True)
        self.SetReadOnly(row, COLUMN.REFRACTIVE_INDEX, True)
        #self.SetReadOnly(row, COLUMN.OPTICAL_THICKNESS, True)

    
    def update(self, event):
        wavelength = self.thin_film_project.layer_stack_model.wavelength
        for row in range(self.GetNumberRows()):
            material_name = self.GetCellValue(row, COLUMN.MATERIAL)
            mate = self.thin_film_project.material_lib.find_material(material_name)
            # refractive index
            nk = mate.complex_refractive_index(wavelength)
            n = nk.real
            self.SetCellValue(row, COLUMN.REFRACTIVE_INDEX, str(n))

            # extinction coefficient
            k = nk.imag
            self.SetCellValue(row, COLUMN.EXTINCTION_COEFFICIENT, str(k))

            value = 5*float(self.GetCellValue(row, COLUMN.PHYSICAL_THICKNESS))
            self.SetCellValue(row, COLUMN.OPTICAL_THICKNESS, str(value))

        event.Skip()






