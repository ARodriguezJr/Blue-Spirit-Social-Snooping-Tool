# Blue Spirit Program

from InstagramAPI import InstagramAPI
import getpass
import argparse
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

parser = argparse.ArgumentParser(description="Blue Spirit Instagram Snooping Tool")
#parser.add_argument("-u", help="Username to use for login", metavar="USERNAME", dest="myUsername", nargs=1, type=str, action="store", required=True)
parser.add_argument("-f", help="Show users who do not follow you back", dest="searchFakes", action="store_true")
parser.add_argument("-i", help="Intensity of target scan: 1-Basic Name Search, 2-Adaptive Name Search", dest="intensity", nargs=1, type=int, action="store")
parser.add_argument("-t", help="Username to target for snooping - can take multiple usernames", dest="tgtUsernames", nargs=argparse.REMAINDER, type=str, action="store")

args = parser.parse_args()
tgtUsernames = args.tgtUsernames

##########   START LOGIN   ##########

myUsername = input("Please enter username: ")
myPassword = getpass.getpass(prompt="Please enter password: ")

api = InstagramAPI(myUsername, myPassword)
api.login()

##########   START SELF REPORTING   ##########

# List of all followers
#followers = api.getTotalFollowers(user_id)
#print('Number of followers:', len(followers))

api.getProfileData()
myProfile = api.LastJson

print(f"USERNAME: {myProfile['user']['username']} \nNAME: {myProfile['user']['full_name']} \nID: {myProfile['user']['pk']}")
print(myProfile)

if args.searchFakes:
    myFollowers = api.getTotalSelfFollowers()
    myFollowing = api.getTotalSelfFollowings()

    followingNames = []
    followerNames = []

    for user in myFollowing:
        followingNames.append(user['username'])

    for user in myFollowers:
        followerNames.append(user['username'])

    for username in followingNames:
        #print(username)
        if username not in followerNames:
            myFakes.append(username)

    print(myFakes)



##########   START TARGET REPORTING   ##########

if tgtUsernames is None:      # Exits program if no target chosen
    print("\nNo target selected - Exiting program!")
    quit()         

##########   START PRELIMINARY REPORTING   ##########

# Objects not needed only one target exists at a time
# TODO make into object
for targetName in tgtUsernames:
    print(f"\nSEARCHING FOR: {targetName}")

    api.searchUsername(targetName)
    foundUser = api.LastJson
    if foundUser['status'] == "fail":
        print(f"{targetName} was not found!\n")
        continue

    foundUsername = foundUser['user']['username']
    foundRealName = foundUser['user']['full_name']
    foundID = foundUser['user']['pk']

    print(f"\nUSERNAME: {foundUsername} \nNAME: {foundRealName} \nID: {foundID}\n")

    ##########   START FAMILY REPORTING   ##########

    
    foundRealName = foundRealName.split(" ")

    foundLastNames = []
    foundLastNames.append(foundRealName[-1])    # Raw name
    foundLastNames.append(strip_accents(foundLastNames[0]))     # Name stripped of accents
    foundLastNames.append(foundLastNames[0].lower())    # Raw name as lowercase
    foundLastNames.append(foundLastNames[1].lower())    # Stripped name as lowercase

    #TODO: Remove duplicates
    #TODO: ask for search intensity, if strong, make new names of related names

    print(f"SEARCHING FOR: {foundLastNames}")

    # Get complete list of followers and following for parsing
    foundFollowersRaw = api.getTotalFollowers(foundID)      
    foundFollowingRaw = api.getTotalFollowings(foundID)

    # Array to hold family members info
    foundFamily = []        
    for user in foundFollowersRaw:
        personUser = user['username']
        personReal = user['full_name']

        for lastName in foundLastNames:
            if personUser.find(lastName) != -1 or personReal.find(lastName) != -1:
                foundFamily.append(user)
    
    for user in foundFollowingRaw:
        personUser = user['username']
        personReal = user['full_name']

        for lastName in foundLastNames:
            if personUser.find(lastName) != -1 or personReal.find(lastName) != -1:
                foundFamily.append(user)

    # TODO: check for variations in spelling, maybe make flag for more time and remove accents

    # Delete duplicate family members found
    uniqueFamily = [] 
    for i in foundFamily: 
        if i not in uniqueFamily: 
            uniqueFamily.append(i) 

    print(f"FOUND FAMILY: {uniqueFamily}\n\n\n")
    for member in uniqueFamily:
        print(member['username'])
    
    #TODO: Remove duplicates

    ########### START SIGNIFICANT OTHER REPORTING ################

    foundBio = myProfile['biography']

    # First splits bio into words/phrases
    # Then searches for two character phrases or initials in form of X.X.

    # TODO: Implement search for date in bio, then match date/numbers to followers/following
    foundBioSplit = foundBio.split(" ")

