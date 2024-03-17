#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import wx
import wx.grid


class TestGUI(wx.Frame):
    def __init__(self, parent, id=-1, title='TEST GUI'):
        wx.Frame.__init__(self, parent, id, title)
        self.SetTitle('TEST GUI')
        self.SetSize((300, 500))

        panel = wx.Panel(self)

        # ボタンの作成
        self.Btn = wx.Button(panel, label="push", pos=(120, 10), size=(60, 20))

        # ラベルの作成
        self.label = wx.StaticText(panel, -1, ' ', pos=(130, 50))

        # ボタンを割り当て
        self.Bind(wx.EVT_BUTTON, self.push, self.Btn)

        # コンボボックス
        self.cmb01 = wx.ComboBox(panel, wx.ID_ANY, 'select', choices=[], style=wx.CB_SIMPLE, pos=(60,80), size=(180,24))
        self.cmb01.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))

        self.cmb01.Append('FW', 1)
        self.cmb01.Append('MF', 2)
        self.cmb01.Append('DF', 3)

        # Grid
        self.grid = wx.grid.Grid(panel, pos=(30,120), size=(240,100))
        self.grid.CreateGrid(2, 2)
        self.grid.SetColLabelValue(0, "No")
        self.grid.SetColLabelValue(1, "Name")

        self.grid.SetCellValue(0,0,"7")
        self.grid.SetCellValue(0,1,"TEST")
        self.grid.SetCellValue(1,0,"10")
        self.grid.SetCellValue(1,1,"TET")

        # 行追加ボタンの作成
        self.BtnAdd = wx.Button(panel, label="ADD", pos=(120, 240), size=(60, 20))
        # ボタンを割り当て
        self.Bind(wx.EVT_BUTTON, self.rowadd, self.BtnAdd)

        # 行削除ボタンの作成
        self.BtnDel = wx.Button(panel, label="DEL", pos=(120, 280), size=(60, 20))
        # ボタンを割り当て
        self.Bind(wx.EVT_BUTTON, self.rowdel, self.BtnDel)

        self.Show(True)

        # コンボボックスイベント
        self.Bind(wx.EVT_COMBOBOX, self.cmb01select, self.cmb01)

    #-------------------------
    # イベント設定
    #-------------------------

    def push(self, event):
        self.label.SetLabel('OK')

    def cmb01select(self, event):
        print('Position:{}'.format(self.cmb01.GetValue()))
        self.label.SetLabel(self.cmb01.GetValue())

    # 行追加
    def rowadd(self, event):
        self.grid.AppendRows(1)
        rows = self.grid.NumberRows
        self.grid.SetCellValue(rows-1, 0, "8")
        self.grid.SetCellValue(rows-1, 1, "add")

    # 行削除
    def rowdel(self, event):
        if(self.grid.NumberRows != 0):
            rows = self.grid.GridCursorRow
            self.grid.DeleteRows(rows,1)


#-------------------------------------------------
## main ###
#-------------------------------------------------
if __name__=='__main__':

    app=wx.App()
    TestGUI(None, wx.ID_ANY, "Btn")
    app.MainLoop()
