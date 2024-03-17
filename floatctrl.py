import string
import wx


class FloatCtrl(wx.TextCtrl):
    '''
    https://gist.githubusercontent.com/needle-wang/1547620e681887f61c23c4e4cf8606a6/raw/6dab71015d2750055818cf3fc96970a6bdb31932/FloatCtrl.py
    https://stackoverflow.com/questions/1369086/is-it-possible-to-limit-textctrl-to-accept-numbers-only-in-wxpython
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Bind(wx.EVT_CHAR, self.onChar)

    def onChar(self, event):
        keycode = event.GetKeyCode()
        obj = event.GetEventObject()
        val = super().GetValue()
        # filter unicode characters
        if keycode == wx.WXK_NONE:
            pass
        # allow digits
        elif chr(keycode) in string.digits:
            event.Skip()
        # allow special, non-printable keycodes
        elif chr(keycode) not in string.printable:
            event.Skip()  # allow all other special keycode
        # allow '-' for negative numbers
        elif chr(keycode) == '-':
        # 负号只能是开头
            if '-' not in val:
                obj.SetValue('-' + val)  # 如果是首次输入"-", 则放在开头
                obj.SetInsertionPointEnd()
            else:
                obj.SetValue(val[1:])    # 如果已存在"-", 则去掉
                obj.SetInsertionPointEnd()
        # allow '.' for float numbers
        elif chr(keycode) == '.' and '.' not in val:
            event.Skip()
        return

    def GetValue(self):
        try:
            return float(super().GetValue())
        except ValueError as e:
            return 0.0
        