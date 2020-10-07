#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:15:29 2020

@author: mcellinluke
"""
#!/usr/bin/env python2
"""Implement the Erikson Flanker Task"""

## CATCH THE SNITCH.... TWO LETTERS.... SNITCH IS A THIRD LETTER....VERY LOW PROBABILITY BUT DOUBLES POINTS ON THAT BLOCK




from psychopy import core, visual, event
import numpy as np

############ participant variables ##############
parno=9              ####### ENTER PAR NUMBER HERE
cond=0              ####### ENTER COND HERE
balance=0
gender=2             ###### ENTER PAR GENDER HERE
age=26               ####### ENTER PAR AGE HERE 

# ===== PARAMETERS ===== #
# Declare primary task parameters
nBlocks = 14             # how many blocks will there be?
nTrialsB = 96     # how many trials between breaks? 64 per block
ITI_min = 0.5           # fixation dot before arrows appear
ITI_range = 0.5        # ITI will be between ITI_min and ITI_min + ITI_range (in seconds)
flankerDur = 0.0        # time flanker arrows are onscreen before target (in seconds)
targetDur = 2          # time target arrow is onscreen (in seconds)
blankDur = 0
respDur = 2             # max time (after onset of target) to respond (in seconds)
respKeys = ['a', 'f','d']   # keys to be used for responses
fixCrossSize = 30       # size of cross, in pixels
rtDeadline = 1.5          # responses after this time will be considered too slow (in seconds)
rtTooSlowDur = 1.5        # duration of 'too slow!' message (in seconds)
counter=0               #counter for every trial

if balance==0:
    arrowChars=['H','G']    #left and right letters
elif balance==1:
    arrowChars=['G','H']    #left and right letters

#set up trial matrix


#cond 0 = ind first, cond 1 = joint first
if cond==0:
    socArr=[0,1]*(1+(nBlocks/2))
elif cond==1:
    socArr=[1,0]*(1+(nBlocks/2))


# enumerate constants
arrowNames = ['Left','Right']

# empty zeros for saving data
flankerdata=np.zeros((5000,12)) #order is: participant,age,gender,block,trial,socType,rewardType,trialType,snitch,targetdirection,ITI,accuracy,RT

# ===== SET UP STIMULI ===== #
#create window and stimuli
globalClock = core.Clock()#to keep track of time
trialClock = core.Clock()#to keep track of time
win = visual.Window([1400,900],color='white', monitor='testMonitor', screen=0, units='deg', name='win')
fixation = visual.ShapeStim(win,lineColor='slategrey',lineWidth=2.0,vertices=((-fixCrossSize/2,0),(fixCrossSize/2,0),(0,0),(0,fixCrossSize/2),(0,-fixCrossSize/2)),units='pix',closeShape=False);

# declare list of prompts
topPrompts = ["Keep your eyes on the cross at the center of the screen when it appears. You will then see a series of arrows. Using your left hand, press the LEFT BUTTON whenever the middle character is a H and the RIGHT BUTTON when the middle character is a G.... If the snitch S appears amongst the arrows (it will not appear in the middle arrow) press the middle left button to catch it! During the practice, if you answer too slowly, you'll see a message reminding you to speed up. Please respond as accurately as possible without being slower than this deadline."]
bottomPrompts = ["Press a middle button to continue."]


message1 = visual.TextStim(win, text=topPrompts, pos=[0,3], color='slategrey', alignHoriz='center', name='topMsg')
message2 = visual.TextStim(win, text=bottomPrompts, pos=[0,-8], color='slategrey', alignHoriz='center', name='bottomMsg')

# make target arrow
target = visual.TextStim(win,pos=[0,0], color='slategrey', alignHoriz='center', height=1, name='target', text = arrowChars[0])
flankers = []
flankerPos = [-2, -1, 1, 2] #should be 0.6 visual angle distance
for i in range(0,len(flankerPos)):
    flankers.append(visual.TextStim(win,pos=[flankerPos[i],0], color='slategrey', alignHoriz='center', height=1 , name='flanker%d'%(i+1), text = arrowChars[1]))
# make too-slow message
tooSlowStim = visual.TextStim(win, pos=[0,0], color='red', alignHoriz='center', name='tooSlow', text="Too Slow!")



# ======= SUBFUNCTIONS ======= #
#for block instructions
def blockInstr(socType,iBlock,nBlocks):
    
    # define social instructions
    if socType==0:
        socText=visual.TextStim(win, text='INDIVIDUAL trial..... You will be scored on your own performance',color='slategrey',pos=[0,3])
    elif socType==1:
        socText=visual.TextStim(win, text='JOINT trial...... You and your partner will be scored together',color='slategrey',pos=[0,3])
    elif socType==99:
        socText=visual.TextStim(win, text='PRACTICE trial',color='slategrey',pos=[0,3])
       
    #space to continue message but different message to get experimenter if halfway through
    if iBlock==(nBlocks/2)+2:
        spaceprompt = visual.TextStim(win, text="Press a middle button to continue.",color='slategrey',pos=[0,-4])
    else:
        #space continue
        spaceprompt = visual.TextStim(win, text="Press a middle button to continue.",color='slategrey',pos=[0,-4])


    #draw instructions
    socText.draw()
    win.flip()
    core.wait(1)

    #continue space
    socText.draw()
    spaceprompt.draw()
    win.flip()
    event.waitKeys(keyList=['s','d'])


#for trial
def RunTrial(targetDir,flankerDir,ITI,targetDur):
    
    # display fixation cross
    fixation.draw()
    win.flip()
    
    #wait for random ITI
    core.wait(ITI)
    
    # get trial time
    tTrial = globalClock.getTime()
    # reset clock
    trialClock.reset()
    
    # count amount of greys generated
    # display flankers ONLY
    for flanker in flankers:
        flanker.text = arrowChars[flankerDir] #draw usual flanker
        
        # determine if snitch will appear
        snitch=np.random.random()>0.75; # 1% chance per flanker
        if snitch==True:
            flanker.text='S'
            
        flanker.color='slategrey'
        flanker.draw()
             
    win.flip()
    core.wait(flankerDur)
    
    # display flankers AND target 
    for flanker in flankers:
        flanker.draw()
    target.text = arrowChars[targetDir]
    target.color='slategrey'
    target.draw()
    win.flip()
    tStim = trialClock.getTime() # get time when stim was displayed
    event.clearEvents() # flush buffer
     
    # get responses
    pressed=event.waitKeys(maxWait=2,keyList=respKeys,timeStamped=trialClock)
    if pressed == None:
        allKeys=[9999,9999]
    else:
        allKeys=pressed[0]
        allKeys[1]=allKeys[1]-tStim
    
    if allKeys[1] >= rtDeadline:
        tooSlowStim.draw()
        win.flip()
        core.wait(rtTooSlowDur,rtTooSlowDur)
        
    #draw snitch caught 
    if snitch==True and allKeys[0]=='d':
        snText=visual.TextStim(win, text='SNITCH CAUGHT',color='slategrey',pos=[0,0])
        snText.draw()
        win.flip()
        core.wait(2)
        
    # return trial time, response(s)
    return (tTrial,allKeys,snitch)

# ======= RUN PROMPTS ======= #

#display instructions and wait
message1.draw()
message2.draw()
win.flip()

#short wait
core.wait(0.4)
event.waitKeys(keyList=['s','d'])

# ===== MAIN EXPERIMENT ===== #
for iBlock in range(3,nBlocks): # for each block of trials
    
    # determine trial types on block level
    socType=socArr[iBlock]
    
    #first two trial are short practices with feedback
    if iBlock<2:
        isPractice = True
        socType=99
        nTrialsPerBlock=nTrialsB/8
    else:
        isPractice = False
        nTrialsPerBlock = nTrialsB

    
    # add instructions for block type (reward structure and condition)
    blockInstr(socType,iBlock,nBlocks)
    
    #make blocks..... randomly paired flank and target arr, but equal cong & incong
    flankArr=[0,1]*(nTrialsPerBlock/2)
    flankArr=np.sort(flankArr)
    targArr=[0,1]*(nTrialsPerBlock/2)
    arrmatrix=np.array([flankArr,targArr]) 
    arrmatrix=np.transpose(arrmatrix)
    np.random.shuffle(arrmatrix) #randomize order
    
    for iTrial in range(0,nTrialsPerBlock): # for each trial
                
        #pick arrow dirs
        flankerDir = arrmatrix[iTrial,0]
        targetDir = arrmatrix[iTrial,1]
                    
        #determine ITI
        ITI = ITI_min + np.random.random()*ITI_range

        # Run Trial
        [tTrial, allKeys,snitch] = RunTrial(targetDir,flankerDir,ITI,targetDur)
                
        # check responses
        keyChar=allKeys[0]
        RT = allKeys[1]   
        
        #check correct or incorrect
        if keyChar == 0:
            thisResp = 2 #timeout
        elif keyChar == respKeys[targetDir]:
            thisResp = 0 # correct
        else:
            thisResp = 1 # incorrect
        
        # give feedback if this is practice
        if isPractice and thisResp==1:
            message1.setText("Whoops! That was incorrect. Press LEFT whenever the middle arrow is < and RIGHT when the middle arrow is >")
            message2.setText("Press a middle button to continue.")
            message1.draw()
            message2.draw()
            win.flip()
            core.wait(0.25) # quick pause to make sure they see it
            event.waitKeys(keyList=['s','d'])
        
        #determine whether congruent or incongruent
        trialType=flankerDir==targetDir
        
        # save trial data and write to CSV at every iteration
        flankerdata[counter]=parno,age,gender,iBlock,iTrial,socType,trialType,targetDir,snitch,ITI,thisResp,RT   #order is: participant,age,gender,block,trial,socType,rewardType,trialType,snitch,targetdirection,ITI,accuracy,RT
        np.savetxt(str(parno)+'data',flankerdata,delimiter=',')
        counter+=1 #update counterfor every iteration        
          