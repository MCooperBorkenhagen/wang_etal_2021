import os,random, glob, os.path, sys
from psychopy import visual, core, gui, event
import helpfunctions as function
import datetime
import randomization as r

#windows setup, image setup, fixation cross setup
win = visual.Window(fullscr=False,allowGUI=True,color="white", units='pix')
images=function.loadFiles('images','.jpg','image',win=win)
#print 'test image list: ', images
fixCross = visual.TextStim(win, text='+', height=40, color="black", pos=[0,0])

crossDur=.8
ISI=.3
targetWait=.2
noiseWait=.3
ITI=.2

#Open dialog box to define ID for current participant
userInfo = {'subjID':'Enter SubNum'}
dlg = gui.DlgFromDict(userInfo)
subjID = userInfo['subjID']

#Create data file for participant
dataFile='output/'+str(subjID)+'_Data.txt'
if not (os.path.exists('trials') & os.path.exists('output')) :
    os.makedirs('trials')
    os.makedirs('output')

#Keep prompting user to change participant ID until they choose a unique one
while os.path.isfile(dataFile):
    function.popupError('File Exists')
    dlg = gui.DlgFromDict(userInfo)
    subjID = userInfo['subjID']
    dataFile='output/'+str(subjID)+'_Data.txt'

# write first column of datafile
dataFile=open(dataFile, 'w')
dataColName=('\t'.join(['trialNum','blockNum','RefCat','targetType','target','correctResp','resp','correctOrNot','RT']) +'\n')
dataFile.write(dataColName)

#Create trial sequence file for participants
OrderName='trials/'+str(subjID)+'_trialOrder.txt'

#gets randomized sequence and writes to to file readable by importTrials
#rc_blocks = r.randRefCat()
#cond_blocks=r.randTargets(rc_blocks)
#randomizedTrials=r.matchRCTarget(rc_blocks,cond_blocks);
#r.exportRandBlocks(randomizedTrials,OrderName)
randomizedTrials=r.shuffleTrials(OrderName)

# set initial state of exp
testClock=core.Clock()
# load practice order sequence
#pracList=function.importTrials('trials/Prac_trialOrder.txt')
pracList=[('rc16', 'r', 'r16', 'z')]
# load real order sequence
###[('rc16', 'r', 'r16', 'z'), ('rc35', 'u', 'u35', 'n'), ('rc4', 'o', 'o4', 'z'...
### four blocks of tuple list, each tuple is a trial
testList=randomizedTrials

#present practice instructions
images['prac'][0].draw()
win.flip()
event.waitKeys(keyList=['space'])

#present practice trials
for trial in range (len(pracList)):
    rc=pracList[trial][0]
    targetType=pracList[trial][1]
    target=pracList[trial][2]
    correctResp=pracList[trial][3]

    #blank and ref cat
    win.flip()
    displayRC=images[rc][0]
    displayRC.pos=[-200,200]
    displayRC.draw()
    displayRC.setAutoDraw(True)
    core.wait(ISI)
    win.flip()
    core.wait(crossDur)

    #display fixation cross
    fixCross.draw()
    win.flip()
    core.wait(crossDur)

    #display target
    displayTarget=images[target][0]
    displayTarget.draw()
    win.flip()
    core.wait(targetWait)

    #display noise 
    images['noise'][0].draw()
    win.flip()
    core.wait(noiseWait)

    #wait participant's respond 
    win.flip()
    visual.TextStim(win, text='Yes, press "z"; No, press "n"',alignHoriz='center',alignVert='center')
    #red='no'; green='yes'
    displayPressRG = images['pressRG'][0]
    displayPressRG.draw()
    win.flip()
    resp=event.waitKeys(keyList=['z','n'])
    RT=str(testClock.getTime()*1000)

# remove this for real exp
    if resp[0]=='space':
        core.quit()
    elif resp[0]==correctResp:
        correct='1'
        feedback='CORRECT'
    else:
        correct='0'
        feedback='INCORRECT'
    win.flip()
    feedback = visual.TextStim(win, text=feedback, height=40, color='black', pos=[0,0])
    feedback.draw()
    win.flip()
    core.wait(ITI)
    displayRC.setAutoDraw(False)

# present real trial instructions
testinstructions=images['test'][0]
testinstructions.draw()
win.flip()
event.waitKeys(keyList=['space'])

# present real trial instructions
blockNum=1
trialNum=1
for block in testList:		# block[('rc16', 'r', 'r16', 'z'), ('rc35', 'u', 'u35', 'n'), (...
	for trial in block:		# trial, ('rc16', 'r', 'r16', 'z')
		
		rc=trial[0]
		targetType=trial[1]
		target=trial[2]
		correctResp=trial[3]

#	targetType=testList[trial]['targetType']#O/S/U
#    target=testList[trial]['target']#O1/S1/U1
#    rc=testList[trial]['refCat']#RC1...
#    correctResp=testList[trial]['correctResponse']#b/n
#    trialNum=testList[trial]['trialNum']


		#display fixation cross
		win.flip()
		displayRC=images[rc][0]
		displayRC.pos=[-200,200]
		displayRC.draw()
		displayRC.setAutoDraw(True)
		core.wait(ISI) 
		win.flip()
		core.wait(crossDur)

		#display fixation cross
		fixCross.draw()
		win.flip()
		core.wait(crossDur)

		#present target
		displayTarget=images[target][0]
		displayTarget.draw()
		win.flip()
		core.wait(targetWait)

		#display noise
		images['noise'][0].draw()
		win.flip()
		core.wait(noiseWait)

		#ask participant to press z/n and reset clock for respond time
		win.flip()
		testClock.reset()
		visual.TextStim(win, text='Yes, press "z"; No, press "n"',alignHoriz='center',alignVert='center').draw()

		#record responding time and press
		resp=event.waitKeys(keyList=['z','n','space'])
		RT=str(testClock.getTime()*1000)
    
		# remove this for real exp
		if resp[0]=='space':
			core.quit()
		elif resp[0]==correctResp:
			correct='1'
		else:
			correct='0'

		win.flip()
		core.wait(ITI)
		testTrials=('\t'.join([str(trialNum),str(blockNum),rc,targetType,target,correctResp,resp[0],correct,RT]) +'\n')
		dataFile.write(testTrials)
		#clear ref cat on screen
		displayRC.setAutoDraw(False)

		#increment trial number
		trialNum=trialNum+1

	#increment block number
	blockNum=blockNum+1


### end of this exp, disp thank you instr
instructions=visual.TextStim(win, text="""Thank you!
Press any key to exit.""", height=30, color="black", pos=[0,0])
instructions.draw()
win.flip()
event.waitKeys()
dataFile.close()
