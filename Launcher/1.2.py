import Tkinter as Tk
import os, time, urllib2, shutil, zipfile
from os.path import expanduser

########################################################################
class Start(object):
    #----------------------------------------------------------------------
    def __init__(self, parent):
        self.root = parent
        self.root.title("Main Menu")
        self.frame = Tk.Frame(parent)
        self.frameState = 0
        #----------------------------------
        self.configs = {}
        self.props = {}
        self.path = "{0}/{1}".format(expanduser("~"), "TNFLauncher")
        self.confFile = "{0}/{1}/{2}".format(self.path, "configs", "launcher.conf")
        #----------------------------------
        self.frame.pack()
        self.startup()
        self.draw()

    #----------------------------------------------------------------------
    def draw(self):
        print("value, sep=' ', end='n', file=sys.stdout, flush=False")

    #----------------------------------------------------------------------
    def startup(self):
        self.hide()
        self.core = Thinking(self)
        self.core.makeFolders(self.path)
        self.loadProps()
        self.loadConfig()
        #with open("{0}/{1}".format(self.path, "configs/game.list"), 'w') as out:
        #    for x in range(1, 10):
        #        out.write("{0}\n".format(x))
        self.core.grannyCheck()
        self.core.checkLauncherUpdates(self.configs['Version'])
        #self.core.checkUrl("fdoom")
        #result = self.core.checkIfInstalled("fdoom")
        #if not result == "got":
        #    self.core.downloadLink()



    #----------------------------------------------------------------------
    def whileLoading(self):
        print("self.core.")

    #----------------------------------------------------------------------
    def loadProps(self):
        self.props['Version'] = '1.0'

    #----------------------------------------------------------------------
    def loadConfig(self):
        if os.path.isfile("{0}/{1}".format(self.path, "configs/launcher.conf")):

            holder = {}
            with open(self.confFile, 'r') as _in:
                for line in _in:
                    line = line.strip("\n")
                    (key, val) = line.split("=")
                    holder[str(key)] = val
            for x in holder:
                x_old = x
                c = x[0]
                x = c.upper()+x[1:]
                self.configs[x] = holder[x_old]
        else:
            self.makeConfig()

    #----------------------------------------------------------------------
    def makeConfig(self):
        results = []
        with open(self.confFile, 'w') as _out:
            for line in self.props:
                results.append('{0}={1}\n'.format(line,self.props[line]))
            for _line in results:
                _out.write(_line)


    #----------------------------------------------------------------------
    def saveConfig(self):
        results = []
        with open(self.confFile, 'w') as out:
            for line in self.configs:
                results.append('{0}={1}\n'.format(line, self.configs[line]))
            for _line in results:
                out.write(_line)

    #----------------------------------------------------------------------
    def think(self):
        print("")

    #----------------------------------------------------------------------
    def showFrame(self, frameName):
        if frameName == 1:
            subFrame = OtherFrame(self, "MainFrame", 1)

    #----------------------------------------------------------------------
    def hide(self):
        self.root.withdraw()

    #----------------------------------------------------------------------
    def show(self):
        self.root.update()
        self.root.deiconify()

########################################################################
class OtherFrame(Tk.Toplevel):
    #----------------------------------------------------------------------
    def __init__(self, parent, frameName, frameState, message):
        self.parent = parent
        self.name = frameName
        self.frame_state = frameState
        if not message == "":
            self.message = message
        Tk.Toplevel.__init__(self)
        self.geometry("400x300")
        self.title(str(self.name))
        self.drawFrame()

    #----------------------------------------------------------------------
    def drawFrame(self):
        if self.frame_state == 0:
            self.closeFrame()
        elif self.frame_state == 1:
            """ This is the Main Frame """
        elif self.frame_state == -1:
            print("This frame...")
            """ This is the Error Frame """
            errorLabel = Tk.Label(self, text="Error!")
            errorMsg = Tk.Label(self, text=self.message)
            okBtn = Tk.Button(self, text="Ok", command=self.closeFrame)

            errorLabel.grid(row=0,column=0, sticky=Tk.NSEW)
            errorMsg.grid(row=0,column=1, sticky=Tk.NSEW)
            okBtn.grid(row=1,column=1, sticky=Tk.NSEW)

    #----------------------------------------------------------------------
    def changeFrame(self, frameState):
        print("")

    #----------------------------------------------------------------------
    def closeFrame(self):
        self.destroy()
        self.parent.show()

########################################################################
class Thinking():
    #----------------------------------------------------------------------
    def __init__(self, mainFrame):
        """
        """
        self.parent = mainFrame
        self.baseUrl = "http://thenightforum.github.io/"

    #----------------------------------------------------------------------
    def core(self, arg1):
        print("Arg1 = {0}".format(arg1))

    #----------------------------------------------------------------------
    def checkIfInstalled(self, code):
        games = os.listdir("{0}/{1}".format(self.path, "games"))
        for game in games:
            if game == code:
                return "got"
        else:
            result = self.checkUrl(code)
            return result

    #----------------------------------------------------------------------
    def checkUrl(self, code):
        self.GameURL = "{0}/Games/{1}/".format(self.baseUrl, code)
        self.GameCode = code
        try:
            urllib2.urlopen("{0}{1}".format(self.GameURL, "version"))
            return True
        except urllib2.HTTPError, e:
            return False
        except urllib2.URLError, e:
            return False

    #----------------------------------------------------------------------
    def downloadLink(self):
        response = urllib2.urlopen("{0}{1}.zip".format(self.GameURL, self.GameCode))
        zipcontent= response.read()
        with open("{0}/{1}/{2}.zip".format(self.path, "temp", self.GameCode), 'w') as f:
            f.write(zipcontent)
        self.unZipGame()

    #----------------------------------------------------------------------
    def unZipGame(self):
        path = "{0}/{1}/{2}.zip".format(self.path, "temp", self.GameCode)
        zip_ref = zipfile.ZipFile(path, 'r')
        zip_ref.extractall("{0}/{1}/{2}/".format(self.path, "games", self.GameCode))
        zip_ref.close()
        os.remove(path)

    #----------------------------------------------------------------------
    def grannyCheck(self):
        """
        This method is here to perform checks throughout the use of the launcher
        to make sure we are not letting just any random stick their fingers into
        our files and edit stuff to break us.
        """
        games_w_folders = os.listdir("{0}/{1}".format(self.path, "games"))
        num = games_w_folders.index(".DS_Store")
        del games_w_folders[num]
        results = []

        with open ("{0}/{1}".format(self.path, "configs/launcher.conf"), 'r') as check:
            for line in check:
                ## Compare to the loaded configs...
                print("WOW")

        with open ("{0}/{1}".format(self.path, "configs/game.list"), 'r') as check:
            for line in check:
                line = line.strip("\n")
                path = "{0}/{1}/{2}".format(self.path, "games", line)
                if os.path.exists(path):
                    results.append(line)
                else:
                    pass

        with open ("{0}/{1}".format(self.path, "configs/game.list"), 'w') as check:
            for line in results:
                check.write("{0}\n".format(line))

        for game in games_w_folders:
            for line in results:
                if game == line:
                    break
            else:
                if os.path.isdir("{0}/{1}/{2}".format(self.path, "games", game)):
                    results.append(game)
                else:
                    os.remove("{0}/{1}/{2}".format(self.path, "games", game))

    #----------------------------------------------------------------------
    def makeFolders(self, path):
        self.path = path
        folders = ["/games", "/configs", "/temp"]
        for folder in folders:
            path = self.path + folder
            if os.path.exists(path):
                pass
            else:
                os.makedirs(path)
        self.folderCheckRun = True

    #----------------------------------------------------------------------
    def makeFolder(self, folderToMake):
        path = "{0}/{1}".format(self.path, folderToMake)
        if os.path.exists(path):
            subFrame = OtherFrame(self.parent, "Error!", -1, "Folder already exists!")
        else:
            os.makedirs(path)

    #----------------------------------------------------------------------
    def startGame(self):
        print("")

    #----------------------------------------------------------------------
    def checkGameUpdates(self):
        print("")

    #----------------------------------------------------------------------
    def checkLauncherUpdates(self, local):
        self.onlineVersion = float(urllib2.urlopen("{0}{1}".format(self.baseUrl, "VERSION")).read().strip("\n"))
        self.localVersion = float(local)
        if self.onlineVersion > self.localVersion:
            return "Please wait."
            self.selfModify("", "", 1)
        elif self.localVersion > self.onlineVersion:
            return "Please wait."
            self.selfModify("", "", 1)
        else:
            return "All is good."

    #----------------------------------------------------------------------
    def selfModify(self, tochange, changeto, mode):
        if mode == 1:
            data = urllib2.urlopen("{0}{1}/{2}.py".format(self.baseUrl, "Launcher", self.onlineVersion)).read()
            print(data)



#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk.Tk()
    root.geometry("800x600")
    app = Start(root)
    root.mainloop()
