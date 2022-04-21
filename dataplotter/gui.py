import tkinter as tk
from tkinter import filedialog
from tkinter.constants import ACTIVE
try:
    from dataplotter.utils import *
except:
    from utils import *

help_msg = '''
This is an application that assists in data plotting. To get started, click the "Browse Files" button below, navigate \
to the desired files, hold down the control key and select the files you would like to analyze. When finished selecting, \
click the "Open" button. The channels will then populate in the box below where it is says "Please choose the channel(s) \
you would like to plot". Begin typing a channel name where it says "Type channel here". The channels will automatically \
be filtered to what include only what has been typed. To select a channel, simply double click it. It will then populate \
in the box titled "Channels you chose". To select another channel, simply delete what you have typed and begin typing the \
name of the next channel and double click the channel. When all channels have been selected and you would like \
to plot, simply click the "Plot" button. Depending on how many files were selected, this may take anywhere from 30 seconds \
to 4 minutes, so please be patient. To generate a new plot with new channels, exit out of the generated plot, click the "Reset" button \
and begin choosing the new channels. The "Reset All" button will completely reset both the channels and files selected.

'''

class PlotterGUI(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title('Data Plotter GUI')
        self.chosen_channels = []

        self.top_label = tk.Label(self,text='Please choose the files you would like to view below',font=('Arial',15))
        self.top_label.grid(row=0,column=0)

        self.reset_all_btn = tk.Button(self,text='Reset All',command=self.reset_all)
        self.reset_all_btn.grid(row=0,column=1)

        self.help_btn = tk.Button(self,text='Help',command=self.help)
        self.help_btn.grid(row=0,column=2)

        self.tmp_label = tk.Label(self,text='')
        self.tmp_label.grid(row=1,columnspan=2)

        self.label_file_exp = tk.Label(self,text='Choose a file or files:')
        self.label_file_exp.grid(row=2,column=0)
        self.button1 = tk.Button(self,text='Browse Files',command=self.browse_files)
        self.button1.grid(row=2,column=1)

        self.display_files = tk.Text(self,height=5)
        self.display_files.grid(row=3,columnspan=2)

        self.bottom_label = tk.Label(self,text='Please choose the channel(s) you would like to plot',font=('Arial',15))
        self.bottom_label.grid(row=4,column=0)

        self.reset_btn = tk.Button(self,text='Reset',command=self.reset)
        self.reset_btn.grid(row=4,column=1)

        self.channel_entry = tk.Entry(self)
        self.channel_entry.grid(row=5,column=0)
        self.channel_entry.insert(0,'Type channel here')

        # create a binding on entry box to call autofill function every time character is typed
        self.channel_entry.bind('<KeyRelease>',self.autofill)

        self.channel_list = tk.Listbox(self,width=30)
        self.channel_list.grid(row=6,column=0)

        # bind any listbox selection to function fillout which adds the chosen channel to chosen_list listbox
        self.channel_list.bind('<Double-Button-1>', self.fillout) # <<ListboxSelect>> use this if want to bind to single mouse click

        self.chosen_label = tk.Label(self,text='Channels you chose:')
        self.chosen_label.grid(row=5,column=1)

        self.chosen_list = tk.Listbox(self,width=30)
        self.chosen_list.grid(row=6,column=1)

        self.plot_btn = tk.Button(self,text='Plot',font=('Arial',15),command=lambda: [popup(),plot(self.files,self.chosen_channels)])
        self.plot_btn.grid(row=7,columnspan=2)

    def browse_files(self):

        files = filedialog.askopenfilenames(initialdir=r'D:/',
                                            title='Select a file',
                                            filetypes=(('Dat file','*.dat*'),
                                                        ('All files','*.*'))
                                            )
        # print(file)
        self.files = files
        if len(files) > 0:
            self.label_file_exp.configure(text=f'{len(files)} file(s) chosen')
        self.display_files.insert("end",'\n'.join(files))
        self.display_files.insert("end",'\n')
        self.get_channels()


    def get_channels(self):

        channel_set= set()

        for file in self.files:

            f = open(file)
            for line in f:
                if line.startswith('1'):
                    break
            channels = next(f).strip().split('\t')[7:]
            channel_set.add(tuple(channels))
            # ddict[tuple(channels)].append(file)

            f.close()

        # find channels that show up in every file
        all_channel_set = [set(i) for i in channel_set]
        self.shared_channels = set.intersection(*all_channel_set) if len(channel_set) > 0 else []

        # add channels into listbox
        self.channel_list.insert('end',*self.shared_channels)

    def fillout(self,event): # need to pass event for this to work becuase with bindings need to pass the event to the function

        channel = self.channel_list.get(ACTIVE)    #(self.channel_list.curselection()) use this for single mouse click
        self.chosen_list.insert('end',channel)
        self.chosen_channels.append(channel)

    def autofill(self,event): # need to pass event since this is a binded function, this is the autofill function

        typed = self.channel_entry.get() # gets whatever was typed

        if typed == '':
            data = self.shared_channels
        else:
            data = []
            for c in sorted(self.shared_channels):
                if typed.lower() in c.lower():
                    data.append(c)
        # delete whatever is in listbox and update it with similar channels
        self.channel_list.delete(0,'end')
        self.channel_list.insert('end',*data)

    def help(self):

        msg = tk.Toplevel(self)
        msg.title('Help Message')
        txt = tk.Text(msg,wrap='word')
        txt.grid(row=0,column=0)
        txt.insert('end',help_msg)

    def reset(self):

        self.chosen_channels = []
        self.chosen_list.delete(0,'end')

    def reset_all(self):

        self.files = []
        self.shared_channels = []
        self.display_files.delete(1.0,'end')
        self.chosen_channels = []
        self.chosen_list.delete(0,'end')
        self.channel_list.delete(0,'end')
        self.channel_entry.delete(0,'end')
        self.channel_entry.insert(0,'Type channel here')


if __name__ == '__main__':

    app = PlotterGUI()
    app.mainloop()