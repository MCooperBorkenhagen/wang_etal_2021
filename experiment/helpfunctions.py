import os,random, glob, os.path, sys
from psychopy import visual, core, gui, event, sound

def popupError(text):
	errorDlg = gui.Dlg(title="Error", pos=(200,400))
	errorDlg.addText('Error: '+text, color='Red')
	errorDlg.show()


def loadFiles(directory,extension,fileType,win,whichFiles='*',stimList=[]):
	path = os.getcwd() #set path to current directory
	if isinstance(extension,list):
		fileList = []
		for curExtension in extension:
			fileList.extend(glob.glob(os.path.join(path,directory,whichFiles+curExtension)))
	else:
		fileList = glob.glob(os.path.join(path,directory,whichFiles+extension))
	fileMatrix = {} #initialize fileMatrix  as a dict because it'll be accessed by picture names, sound names, whatever
	for num,curFile in enumerate(fileList):
		fullPath = curFile
		fullFileName = os.path.basename(fullPath)
		stimFile = os.path.splitext(fullFileName)[0]
		if fileType=="image":
			try:
				surface = pygame.image.load(fullPath) #gets height/width of the image
				stim = visual.SimpleImageStim(win, image=fullPath)
				fileMatrix[stimFile] = ((stim,fullFileName,num,surface.get_width(),surface.get_height(),stimFile))
			except: #no pygame, so don't store the image dims
				stim = visual.SimpleImageStim(win, image=fullPath)
				fileMatrix[stimFile] = ((stim,fullFileName,num,'','',stimFile))
		elif fileType=="sound":
			soundRef = sound.Sound(fullPath)
			fileMatrix[stimFile] = ((soundRef))
	#check
	if stimList and set(fileMatrix.keys()).intersection(stimList) != set(stimList):
		#print stimList, fileMatrix.keys(),set(stimList).difference(fileMatrix.keys())
		popupError(str(set(stimList).difference(fileMatrix.keys())) + " does not exist in " + path+'\\'+directory)

	return fileMatrix

# read tab delimited file with header
# make list of {header:data} dicts out of it for each line
def importTrials(trialFile,separator='\t'):
	trialList = [trial.split(separator) for trial in open(trialFile,'r').readlines()]
	colNames = trialList[0]
	trialList = trialList[1:]
	trialDict = []
	for curTrial in trialList:
		tempDict={}
		for colNum,curCol in enumerate(colNames):
			tempDict[curCol.rstrip()]=curTrial[colNum].rstrip()
		trialDict.append(tempDict)
	return trialDict

def repetitions (seq, itemRep, seqRep):
	l=[]
	for item in seq:
		l.extend([item]*itemRep)
	return l * seqRep
