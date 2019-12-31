# Blue Spirit Program

from InstagramAPI import InstagramAPI
import getpass
import argparse
import time

parser = argparse.ArgumentParser(description="Blue Spirit Instagram Snooping Tool")
#parser.add_argument("-u", help="Username to use for login", metavar="USERNAME", dest="myUsername", nargs=1, type=str, action="store", required=True)
parser.add_argument("-f", help="Show users who do not follow you back", dest="searchFakes", action="store_true")
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

    foundLastName = foundRealName[-1]

    print(f"LAST NAME: {foundLastName}")

    # Get complete list of followers and following for parsing
    foundFollowersRaw = api.getTotalFollowers(foundID)      
    foundFollowingRaw = api.getTotalFollowings(foundID)

    # Array to hold family members info
    foundFamily = []        
    for user in foundFollowersRaw:
        personUser = user['username']
        personReal = user['full_name']

        if personUser.find(foundLastName) != -1 or personReal.find(foundLastName) != -1:
            foundFamily.append(user)
    
    for user in foundFollowingRaw:
        personUser = user['username']
        personReal = user['full_name']

        if personUser.find(foundLastName) != -1 or personReal.find(foundLastName) != -1:
            foundFamily.append(user)

    # TODO: check for variations in spelling, maybe make flag for more time and remove accents
    print(f"FOUND FAMILY: {foundFamily}\n\n\n")
    for member in foundFamily:
        print(member['full_name'])
    

#api.getUsernameInfo()

