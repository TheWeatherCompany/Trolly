# Uses Trolly - https://github.com/TheWeatherCompany/Trolly

# @ckelner - 2016/08/14 - I really hacked this up after Annika did the init
# so it is a big fugly and waaay not DRY.  Quick Sunday hacks.  Love.

import trolly
import sys

# Trello API Key and user auth token 
API_KEY		         = sys.argv[1]
TRLAB_TOKEN        = sys.argv[2]
print 'API key is %s, token is %s' % (API_KEY, TRLAB_TOKEN)

tc = trolly.client.Client(API_KEY, TRLAB_TOKEN)

# Template board ID and organization ID  
TEMPLATE_BOARD_ID  = '565c7388e9437c96e0febd3d'
ORG_ID             = '54088113bc859376bccb0ce5'

org = trolly.Organisation(tc, ORG_ID)
allBoards = org.get_boards()

templateBoard = tc.get_board(TEMPLATE_BOARD_ID)
templateLabels = templateBoard.get_labels()
allowedLabelNames = []
allowedLabels = []
debugOnce = 0
print '='*50
print 'These are the allowed labels names:'
for label in templateLabels:
    if debugOnce is 0:
        print '+'*25
        print "DEBUG"
        print label.name
        print label.color
        print label.id
        print '+'*25
        debugOnce = 1
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
print '='*50
print "These are ALL label names"
for label in allLabels:
    print label.id, label.name
    allLabelNames.append(label.name)

print '='*50
print 'These are the common label names:'
commonLabels = set(allowedLabelNames).intersection(allLabelNames)
print commonLabels

print '='*50
print 'These are the labels based on name that need to be deleted:'
badLabels = list(set(allLabelNames) - set(allowedLabelNames))
print badLabels

for label in allLabels:
   if label.name in badLabels:
     print "Removing", label.name
     label.remove_label()

#for board in allBoards:
#    if !board.closed:
#        boardLabels = board.get_labels()
#        for label in boardLabels:
#            for tempLabel in allowedLabels:
#                if
