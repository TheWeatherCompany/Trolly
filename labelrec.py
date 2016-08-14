# Uses Trolly - https://github.com/TheWeatherCompany/Trolly

# @ckelner - 2016/08/14 - I really hacked this up after Annika did the init
# so it is a big fugly and waaay not DRY.  Quick Sunday hacks.  Love.

import trolly
import sys
import time

# Trello API Key and user auth token 
API_KEY		       = sys.argv[1]
TRLAB_TOKEN        = sys.argv[2]
#print 'API key is %s, token is %s' % (API_KEY, TRLAB_TOKEN)
print ''

tc = trolly.client.Client(API_KEY, TRLAB_TOKEN)

# Template board ID and organization ID  
TEMPLATE_BOARD_ID  = '565c7388e9437c96e0febd3d'
ORG_ID             = '54088113bc859376bccb0ce5'
TEMPLATE_CARD_ID   = '574d8df23a213308f26a3c2d'

org = trolly.Organisation(tc, ORG_ID)
allBoards = org.get_boards()

templateBoard = tc.get_board(TEMPLATE_BOARD_ID)
templateLabels = templateBoard.get_labels()
templateCard = templateBoard.get_card(TEMPLATE_CARD_ID)
templateBoardLists = templateBoard.get_lists()

allowedLabelNames = []
allowedLabels = []
debugOnce = 0
for label in templateLabels:
    if debugOnce is 0:
        print '+'*55
        print "DEBUG"
        print '+'*55
        print label.name
        print label.color
        print label.id
        print '+'*55
        debugOnce = 1
        print ''
        print '='*150
        print 'These are the allowed labels names:'
        print '='*150
    print label.name
    allowedLabelNames.append(label.name)
    allowedLabels.append(label)

# print allowedLabelNames

allLabels = []
for board in allBoards:
    if board.closed:
#        print 'Closed board: %s' % board.name
        continue
    allLabels += board.get_labels()

allLabelNames = []
print ''
print '='*150
print "These are ALL label names"
print '='*150
for label in allLabels:
    print label.id, label.name
    allLabelNames.append(label.name)

print ''
print '='*150
print 'These are the common label names:'
print '='*150
commonLabels = set(allowedLabelNames).intersection(allLabelNames)
print commonLabels

print ''
print '='*150
print 'These are the labels based on name that need to be deleted:'
print '='*150
badLabels = list(set(allLabelNames) - set(allowedLabelNames))
print badLabels

for label in allLabels:
   if label.name in badLabels:
     print "Removing label with name: '" + label.name + "'"
     label.remove_label()

print ''
print '='*150
print 'Reconciling labels for color and name across all boards -- this can take awhile, moves card with labels to each board:'
print '='*150
for board in allBoards:
    if board.closed is False:
        boardLabels = board.get_labels()
        boardLists = board.get_lists()
        templateCard.update_card({'idList':boardLists[0].id,'idBoard':board.id})
        time.sleep(3)
        templateCard.update_card({'idList':templateBoardLists[0].id,'idBoard':TEMPLATE_BOARD_ID})
        time.sleep(3)
        for label in boardLabels:
            #foundLabel = False
            for tempLabel in allowedLabels:
                if tempLabel.name == label.name:
                    if tempLabel.color != label.color:
                        print "-- Removing " + label.name + " from " + board.name + " for color mismatch"
                        label.remove_label()
                        #print "++ Adding " + label.name + " with color '" + tempLabel.color + "' to board '" + board.name + "'"
                        #board.add_label({'name': tempLabel.name, 'color': tempLabel.color})
                    #foundLabel = True
                #if foundLabel is False:
                #    print "++ Label with name '" + tempLabel.name + "' not found on board '" + board.name + "', adding to board"
                #    board.add_label({'name': tempLabel.name, 'color': tempLabel.color})

