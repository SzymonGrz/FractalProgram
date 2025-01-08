import tkinter as tk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

from frames.IFSFrame import IFSFrame
from frames.RectFrame import RectFrame
from frames.ChaosGameFrame import ChaosGameFrame
from frames.MandelJuliaFrame import MandelJuliaFrame
from frames.StartFrame import StartFrame
from frames.LSystemFrame import LSystemFrame
from frames.TutorialFrame import TutorialFrame

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.state('zoomed')
        self._frame = None

        self.frames = {
            "start" : StartFrame,
            "fractals" : ChaosGameFrame,
            "affine" : IFSFrame,
            "mandel" : MandelJuliaFrame,
            "rect" : RectFrame,
            "lsys" : LSystemFrame,
            "tutor" : TutorialFrame
        }
        NavigationToolbar2Tk.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),)

        self.switch_frame("start")


    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        cls = self.frames[frame_class]
        new_frame = cls(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame
        self._frame.pack(anchor = tk.NW)


if __name__ == "__main__":
    app = App()
    app.title("Fraktale")
    app.mainloop()
    

