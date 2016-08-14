# Uses Trolly - https://github.com/TheWeatherCompany/Trolly

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
print '='*50
print 'These are the allowed labels:'
for label in templateLabels:
    print label.id, label.name
    allowedLabelNames.append(label.name)

# print allowedLabelNames

allLabels = []
for board in allBoards:
    if board.closed:
#        print 'Closed board: %s' % board.name
        continue
    allLabels += board.get_labels()

allLabelNames = []
print '='*50
print "These are ALL labels"
for label in allLabels:
    print label.id, label.name
    allLabelNames.append(label.name)

print '='*50
print 'These are the common labels:'
commonLabels = set(allowedLabelNames).intersection(allLabelNames)
print commonLabels

print '='*50
print 'These are the labels that need to be deleted:'
badLabels = list(set(allLabelNames) - set(allowedLabelNames))
print badLabels

for label in allLabels:
   if label.name in badLabels:
     print "Removing", label.name
     label.remove_label()

#for board in allBoards:
#    if !board.closed:
        
