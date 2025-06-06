from logger.core.libraries import *

class LoggerEntry():

    def __init__(self):
        self.gui = ctk.CTk()
        self.gui._set_appearance_mode('dark')
        self.gui.geometry('800x600')
        self.gui.wm_title('Color Explorer [Logger v.1.2.1]')

        self.logs = []

        self.loglist = CTkListbox.CTkListbox(self.gui, 600, 800)
        self.loglist.pack()

        self.gui.wm_protocol('WM_DELETE_WINDOW', self.close)

    def run(self):
        self.gui.mainloop()
        if (len(self.logs)>0):
            for log in self.logs:
                self.loglist.insert('END', f'[{log.time}] {log.data}')
    
    def close(self):
        self.loglist.destroy()
        self.gui.destroy()
    
    def add_log(self, log: LogData) -> None:
        self.logs.append(log)
        try:
            self.loglist.insert('END', f'[{log.time}] {log.data}')
        except:
            pass
    
    def update(self) -> None:
        self.loglist.option_clear()
        for log in self.logs:
            self.loglist.insert('END', f'[{log.time}] {log.data}')
