import os,random, glob, os.path, sys
from psychopy import visual, core, gui, event
import helpfunctions as function
import datetime
import randomization as r

#windows setup, image setup, fixation cross setup
win = visual.Window(fullscr=False,size=[1080,1080],allowGUI=True,color="white", units='pix')
fixCross = visual.TextStim(win, text='+', height=40, color="black", pos=[0,0])

#load images
images=function.loadFiles('images','.jpg','image',win=win)

#time setup
rcWait1=1.5			#rc_frame
targetWait=0.2		#target frame (different values were considered; originally .057)
#noiseWait=0.3		#mask was tested in pilot but ultimately not included
#rcWait2=1		#rc frame
respWait=10   #response frame, different values were considered - originally 1.5
crossDur=0.2		#fixation cross
ITI=0.1			#after responding to next page, before next cat ref
ISI=0.1			#after instr wait
PRAC_STIMULI = [("pracRC1", "pracT1", "pracFeedback1"), ("pracRC2", "pracT2", "pracFeedback2"), ("pracRC3", "pracT3", "pracFeedback3"), ("pracRC4", "pracT4", "pracFeedback4")]

'''
	This function is to set up the experiment and generate data file, sequence order file
	for each participant
	'''
def setup():
	#Open dialog box to define ID for current participant
	dlg=gui.Dlg(title="LCNL SRC2 Experiment")
	#userInfo = {'subjID':'Enter SubNum'}
	dlg.addField("Subject ID:")
	dlg.addField('Condition', choices=["1", "2", "3", "4"])
	dlg.show()
	if dlg.OK:
		subjID = str(dlg.data[0])
		cond=int(dlg.data[1])
	else:
		core.quit()
	#Create data file for participant
	dataFile='output/'+str(subjID)+'_Data.txt'
	trialFile='trials/'+str(subjID)+'_trialOrder.txt'
	if not (os.path.exists('trials') & os.path.exists('output')) :
		os.makedirs('trials')
		os.makedirs('output')

	#Keep prompting user to change participant ID until they choose a unique one
	while os.path.isfile(dataFile) | os.path.isfile(trialFile):
		function.popupError('File Exists')
		
		#Open dialog box to define ID for current participant
		dlg=gui.Dlg(title="LCNL SRC2 Experiment")
		#userInfo = {'subjID':'Enter SubNum'}
		dlg.addField("Subject ID:")
		dlg.addField('Condition', choices=["1", "2", "3", "4"])
		dlg.show()
		if dlg.OK:
			subjID = str(dlg.data[0])
			cond=int(dlg.data[1])
			dataFile='output/'+str(subjID)+'_Data.txt'
			trialFile='trials/'+str(subjID)+'_trialOrder.txt'
		else:
			core.quit()
        
    
	# prepare output/data file for each participants
	dataFile='output/'+str(subjID)+'_Data.txt'
	# write first column of datafile
	f=open(dataFile, 'w')
	dataColName=('\t'.join(['trialNum','blockNum','RefCat','targetType','target','correctResp','resp','correctOrNot','RT']) +'\n')
	f.write(dataColName)
	f.close()

	#Create trial sequence file for participants
	OrderName='trials/'+str(subjID)+'_trialOrder.txt'

	#gets randomized sequence and writes to to file readable by importTrials
	randomizedTrials=r.shuffleTrials(cond, OrderName)
	return (randomizedTrials,dataFile)

def practiceTrials():

    timer=core.Clock()  #use for record response time

    #present practice instructions
    images['prac'][0].draw()
    win.flip()
    core.wait(ISI)
    event.waitKeys(keyList=['space'])

    #present practice trials
    for trial in PRAC_STIMULI:

        rc=trial[0]
        target=trial[1]
        feedback=trial[2]

        #blank and ref cat
        displayRC=images[rc][0]
        displayRC.pos=[0,100]
        displayRC.draw()
        win.flip()
        core.wait(ISI)
        displayRC.setAutoDraw(True)
        core.wait(rcWait1) #display rc frame1 for 1500ms

        #display fixation cross for .2s
        fixCross.draw()
        win.flip()
        core.wait(crossDur) #0.2s

        #display target for .2s
        displayTarget=images[target][0]
        timer.reset()	# collect rt before target appears
        displayTarget.draw()
        win.flip()
        resp=event.waitKeys(maxWait=targetWait, keyList=['z', 'n'])
        rt=str(timer.getTime()*1000)
        displayRC.setAutoDraw(False)

        # enter response frame
        if not resp:
            win.flip()
            resp=event.waitKeys(maxWait=respWait, keyList=['z', 'n'])
            rt=str(timer.getTime()*1000)
        
        # enter feedback frame
        displayFeedback=images[feedback][0]
        displayFeedback.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        print ('prac trial: (resp, rt) ', resp, rt)

    event.clearEvents(eventType='keyboard')
    

def realTrials(randomizedTrials, dataFile):

    # append data to file and prepare timer
    f=open(dataFile, "a")
    timer=core.Clock()
    
    # present real trial instructions
    testinstructions=images['test'][0]
    testinstructions.draw()
    win.flip()
    core.wait(ISI)
    event.waitKeys(keyList=['space'])

    # present real trial instructions
    trialNum=0
    for block in randomizedTrials:		# block[('A''rc16', 'r', 'r16', 'z'), ('rc35', 'u', 'u35', 'n'), (...
        for trial in block:		# trial, ('A', 'rc13', 's', 's13', 'n')
            b=trial[0]
            rc=trial[1]
            targetType=trial[2]
            target=trial[3]
            correctResp=trial[4]
            
            #increment trial number
            trialNum=trialNum+1

            #blank and ref cat
            win.flip()
            displayRC=images[rc][0]
            displayRC.pos=[0,100]
            displayRC.draw()
            displayRC.setAutoDraw(True)
            core.wait(ISI)  #0.5s
            win.flip()
            core.wait(rcWait1) #display rc frame1 for 1200ms
            
            
            #display fixation cross for .2s
            fixCross.draw()
            win.flip()
            core.wait(crossDur) #0.2s

            #display target for .2s
            displayTarget=images[target][0]
            displayTarget.draw()
            timer.reset()	# collect rt before target appears
            win.flip()
            resp=event.waitKeys(maxWait=targetWait, keyList=['z', 'n'])
            RT=str(timer.getTime()*1000)
            displayRC.setAutoDraw(False)

            if not resp:
                win.flip()
                resp=event.waitKeys(keyList=['z', 'n', 'q'])
                RT=str(timer.getTime()*1000)
                
            win.flip()
            
            if resp[0]=='q':
                core.quit()
            elif resp[0]==correctResp:
                correct='1'
            else:
                correct='0'
            
            # write in data file
            win.flip()
            
            realTrials=('\t'.join([str(trialNum),str(b),rc,targetType,target,correctResp,resp[0],correct,RT]) +'\n')
            f.write(realTrials)
            core.wait(ITI)

    f.close()
            

def end():
### end of this exp, disp thank you instr
    end=images['end'][0].draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    core.quit()



################
## MAIN CALLS ##
################
(randomizedTrials, dataFile)=setup()

practiceTrials()

realTrials(randomizedTrials,dataFile)

end()