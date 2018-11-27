from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from JIRA_ListComparer_Python3 import jiraListComparer

firstFile = ""
secondFile = ""

class jiraComparerApplication(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.createWidgets()

    def onFileButtonClicked(self, button):
        filename = filedialog.askopenfilename(initialdir="C://", title="Open File",
                                              filetypes=(("XML Files", "*.xml"), ("All Files", "*,*")))
        if filename == "":
            messagebox.showinfo("Error", "No file selected - please select a file.")
        else:
            if button == self.firstFileButton:
                firstFile = filename
                self.firstFileResultLabel.config(text=filename)
            else:
                secondFile = filename
                self.secondFileResultLabel.config(text=filename)

    def onGenerateListButtonClicked(self):
        """ generated the list with items not found in both lists """
        if self.firstFileResultLabel.cget("text") != "(None)" and self.secondFileResultLabel.cget("text") != "(None)":
            listComparer = jiraListComparer(firstFile, secondFile)
            """
            generatedList = listComparer.showListDifference(self.firstFileResultLabel.cget("text"),
                                                            self.secondFileResultLabel.cget("text"))
            """
            generatedList = listComparer.showListAllUniqueItems(self.firstFileResultLabel.cget("text"),
                                                                self.secondFileResultLabel.cget("text"))

            if generatedList is not None:
                listString = self.listToStringProcessing(generatedList)
                self.listResults.delete(0, END)
                self.listResults.insert(0, listString)
            else:
                messagebox.showinfo("Error", "No list generated")
        else:
             messagebox.showinfo("Error", "Two files have not been selected - please select two XML files.")

    def listToStringProcessing(self, genList):
        jiraListString = ""
        itemCount = len(genList)
        for item in genList:
            if itemCount != 1:
                jiraListString += item + ", "
                itemCount -= 1
            else:
                jiraListString += item
        return jiraListString

    def createWidgets(self):
        self.winfo_toplevel().title("JIRA List Comparer")

        self.firstFileLabel = ttk.Label(self, text="File 1:")
        self.firstFileLabel.grid(column=0, row=0, sticky=W)

        """ First filename... """
        self.firstFileResultLabel = ttk.Label(self, text="(None)")
        self.firstFileResultLabel.grid(column=1, row=0)

        self.firstFileButton = ttk.Button(self, text="Select")
        self.firstFileButton.config(command=lambda button=self.firstFileButton: self.onFileButtonClicked(button))
        self.firstFileButton.grid(column=2, row=0, sticky=E)

        self.secondFileLabel = ttk.Label(self, text="File 2:")
        self.secondFileLabel.grid(column=0, row=1, sticky=W)

        """ Second filename... """
        self.secondFileResultLabel = ttk.Label(self, text="(None)")
        self.secondFileResultLabel.grid(column=1, row=1)

        self.secondFileButton = ttk.Button(self, text="Select")
        self.secondFileButton.config(command=lambda button=self.secondFileButton: self.onFileButtonClicked(button))
        self.secondFileButton.grid(column=2, row=1, sticky=E)

        self.generateListButton = ttk.Button(self, text="Generate List", command=self.onGenerateListButtonClicked)
        self.generateListButton.grid(column=0, row=2, sticky=W)

        """ Results are here, if applicable... """
        self.listResults = ttk.Entry(self)
        self.listResults.insert(0, "No list generated.")
        self.listResults.config(width="75", )
        self.listResults.grid(column=0, row=3, columnspan=3)

        # attempting to add a scrollbar to the listResults widget
        self.listResultsScrollBar = ttk.Scrollbar(self, orient="horizontal")
        self.listResultsScrollBar.grid(row=4)
        self.listResults['xscrollcommand'] = self.listResultsScrollBar.set

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


root = Tk()
app = jiraComparerApplication(root)

root.geometry('500x200')

root.mainloop()

