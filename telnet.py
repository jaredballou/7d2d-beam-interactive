import telnetlib, sys, re, time

#Games server info     
host = '<IP/HOST_NAME>'
port = <TELNET_PORT>
password = '<TELNET_PASSWORD>'
 
########################################################################
######################## NO EDIT PAST THIS LINE ######################## 
########################################################################

#Chat Dictionary
chat = {
	1 : 'AIR DROP INCOMING!!',
	2 : 'ZOMBIE ALERT!!',
	3 : 'WATCH OUT... there is a WILD',
	4 : 'LOOK DOWN... Someone gave you',
}

#List of words to filter out for prettier wording
itemList = ['GUN', 'ANIMAL', 'spawnwanderinghorde']

#Test if args supplied
if __name__ == "__main__":
     
    if(len(sys.argv) < 2) :
        print 'ERROR: No args supplied'
        sys.exit()
        
#Get the game command
cmdList = []

#Loop through args provided
for x in sys.argv:
	#Add to the cmdList list for storage
	cmdList.append(x)
	
#Store arg for chat logic
whatToSay = int(cmdList[1])

#Placeholders
user = ''
item = cmdList[2]

#Check if we have a user in args
if(len(sys.argv) > 3) :
	user = cmdList[3].upper()

#checks to see if we have enough args supplied for an item to be given	
if(len(sys.argv) > 4) :
	item = cmdList[4].upper()
	
	#Search list and remove ugly words
	for a in itemList :
		if re.match('^'+a+'', item) :
			item = re.sub('^'+a+'', '', item)
	
#Remove the first and second element as it is not needed past here
cmdList.pop(0)
cmdList.pop(0)

#Convert the list into a strin seperated by a space
cmd = ' '.join(cmdList)
 
# connect to remote host
try :
	tn = telnetlib.Telnet(host, port)
except :
	print 'Unable to connect'
	sys.exit()
  
#Send Password
tn.read_until('Password: ', 2)
tn.write(password + '\n') 	

#BASIC Say something in game when button pressed
#Will make this more robust in the future
if whatToSay == 1 :
	tn.write('say " ' + chat[1] + '" \n')
elif whatToSay == 2 :
	if item == 'spawnwanderinghorde' :
		tn.write('say "WANDERING HORDE INCOMING" \n')
	else :	
		tn.write('say " ' + user + ' ' + chat[2] + '" \n')
		time.sleep(10)
elif whatToSay == 3 :
	tn.write('say " ' + user + ' ' + chat[3] + ' ' + item + ' around you!" \n')
elif whatToSay == 4 :
	if item == "WOOD" :
		tn.write('say " ' + user + ' ' + chat[4] + ' some ' + item + '!" \n')
	else :
		tn.write('say " ' + user + ' ' + chat[4] + ' a ' + item + '!" \n')
else :
	print 'OOPS!!'
	sys.exit()

#Send the command to the game server
tn.write(cmd + '\n')
sys.exit()

#Allow interaction with telnet
tn.mt_interact()
