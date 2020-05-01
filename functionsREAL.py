# Blue Spirit Functions
from InstagramAPI import InstagramAPI
import unicodedata
import re
import time
import tkinter as tk

#TODO: Remove emojis from bios and names
#TODO: Clear your profile info box after each scan
#TODO: account for mass amounts of data/celebrities

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def run_scan(api, targetEntry, userDetails, fakesDetails, targetDetails, familyDetails):
    fakesDetails.delete(1.0, tk.END)
    targetDetails.delete(1.0, tk.END)
    familyDetails.delete(1.0, tk.END)


    ##########   START SELF REPORTING   ##########

    # List of all followers
    #followers = api.getTotalFollowers(user_id)
    #print('Number of followers:', len(followers))

    api.getProfileData()
    myProfile = api.LastJson

    userDetails.insert(tk.END, "USERNAME: " + myProfile['user']['username'] + "\nNAME: " + myProfile['user']['full_name']  + "\nID: " + str(myProfile['user']['pk']))
    #print(myProfile)

    #TODO: if args.searchFakes:
    myFollowers = api.getTotalSelfFollowers()
    myFollowing = api.getTotalSelfFollowings()

    followingNames = []
    followerNames = []
    myFakes = []

    for user in myFollowing:
        followingNames.append(user['username'])

    for user in myFollowers:
        followerNames.append(user['username'])

    for username in followingNames:
        #print(username)
        if username not in followerNames:
            myFakes.append(username)

    for fake in myFakes:
        fakesDetails.insert(tk.END, fake + "\n")



    ##########   START TARGET REPORTING   ##########
    targetName = targetEntry.get()
    if targetName is None:      # Exits program if no target chosen
        print("\nNo target selected - Exiting program!")
        quit()         

    ##########   START PRELIMINARY REPORTING   ##########

    # Objects not needed only one target exists at a time
    # TODO make into object
    #TODO: for targetName in tgtUsernames:

    print(f"\nSEARCHING FOR: {targetName}")

    api.searchUsername(targetName)
    foundUser = api.LastJson
    if foundUser['status'] == "fail":
        print(f"{targetName} was not found!\n")
        exit()

    foundUsername = foundUser['user']['username']
    foundRealName = foundUser['user']['full_name']
    foundID = foundUser['user']['pk']

    targetDetails.insert(tk.END, "\nUSERNAME: " + foundUsername +  "\nNAME: " + foundRealName +  "\nID: " + str(foundID))

    ##########   START FAMILY REPORTING   ##########

    
    foundRealName = foundRealName.split(" ")

    foundLastNames = []
    foundLastNames.append(foundRealName[-1])    # Raw name
    foundLastNames.append(strip_accents(foundLastNames[0]))     # Name stripped of accents
    foundLastNames.append(foundLastNames[0].lower())    # Raw name as lowercase
    foundLastNames.append(foundLastNames[1].lower())    # Stripped name as lowercase

    #TODO: Remove duplicates
    #TODO: ask for search intensity, if strong, make new names of related names

    #print("SEARCHING FOR: " + foundLastNames)

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

    #print(f"FOUND FAMILY: {uniqueFamily}\n\n\n")
    for member in uniqueFamily:
        #TODO: Might need to fix inserting, might overwrite
        familyDetails.insert(tk.END, member['username'] + "\n")
    
    #TODO: Remove duplicates

        ########### START SIGNIFICANT OTHER REPORTING ################
        #TODO: ENDING CODE HERE FOR WORKING DEMO
        '''
        foundBio = foundUser['user']['biography']

        # First splits bio into words/phrases
        # Then searches for two character phrases or initials in form of X.X.

        # TODO: Implement search for date in bio, then match date/numbers to followers/following
        foundBioSplit = foundBio.split(" ")

        initialsList = []
        dateList = []
        # ^([A-Z]\.)+$
        # CHecks for format like X.X. and X. and XX
        initialFormat = re.compile('^([A-Z]?(\.)?){1,3}$')
        dateFormat = re.compile('^.{0,2}[/,\-,.].{0,2}[/,\-,.].{2,4}$')
        for phrase in foundBioSplit:
            print(f"Checking Phrase: {phrase}")
            # Checks for Format X.X.
            if initialFormat.match(phrase):
                initialsList.append(phrase)
                print(f"APPENDING INITIAL: {phrase}")
            # Checks for date format MM/DD/YYYY
            elif dateFormat.match(phrase):
                dateList.append(phrase)
                print(f"APPENDING DATE: {phrase}")

            # TODO: Check for uppercase to avoid words like 'to' and 'an'
        
        # Prepare initials as alphabetical chars only for comparison with follower/ing
        for initials in initialsList:
            initials = ''.join(filter(str.isalpha, initials))
            #TODO: might have to make according list to match parsed intiials
        
        # Prepare date as numbers only for comparison with follower/ing
        for date in dateList:
            if date.find("/") != -1:
                searchDates = date.split('/')
            elif date.find("-") != -1:
                searchDates = date.split('-')
            if date.find(".") != -1:
                searchDates = date.split('.')
        

        # SEARCHING FOLLOWER/ING 

        if len(initialsList) != 0 or len(dateList) != 0:
            # TODO: Find a way to speed this up?
            # TODO: Add delay to prevent max API requests per minute?
            foundFollowersInfo = []
            foundFollowingsInfo = []

            # TODO: Sleep for seconds based on error message instead of amount of calls made
            for user in foundFollowersRaw:
                print(f"SEARCHING FOR FOLLOWER: {user['username']}")
                api.searchUsername(user['username'])
                foundFollowerInfo = api.LastJson

                api.searchUsername(user['username'])
                foundFollowerInfo = api.LastJson
                time.sleep(0.5)
                foundFollowersInfo.append(foundFollowerInfo)



            print("Finished followers bio parsing")
            '''
        '''
            for user in foundFollowersRaw:
                print(f"SEARCHING FOR FOLLOWER: {user['username']}")
                api.searchUsername(user['username'])
                foundFollowerInfo = api.LastJson

                # Waits then redoes request if request fails
                if foundFollowerInfo['status'] == 'fail':
                    time.sleep(80)
                    api.searchUsername(user['username'])
                    foundFollowerInfo = api.LastJson
                foundFollowersInfo.append(foundFollowerInfo)

            '''
        '''
            for user in foundFollowingRaw:
                print(f"SEARCHING FOR FOLLOWING: {user['username']}")
                api.searchUsername(user['username'])
                foundFollowingInfo = api.LastJson

                # Waits then redoes request if request fails
                if foundFollowingInfo['status'] == 'fail':
                    time.sleep(80)
                    api.searchUsername(user['username'])
                    foundFollowingInfo = api.LastJson
                foundFollowingsInfo.append(foundFollowingInfo)

        '''
        '''
            for user in foundFollowingRaw:
                print(f"SEARCHING FOR FOLLOWING: {user['username']}")
                api.searchUsername(user['username'])
                foundFollowingInfo = api.LastJson

                api.searchUsername(user['username'])
                foundFollowingInfo = api.LastJson
                time.sleep(1)
                foundFollowingsInfo.append(foundFollowingInfo)

            for user in foundFollowersInfo:
                #TODO: Also work on parsing username for initials
                #TODO: Parse bio/name for initials/date
                userName = user['full_name'].split(' ')
                userBio = user['biography'].split(' ')

                for initials in initialsList:
                    # Checks first and last name for initial
                    # TODO: handle lower/uppercase letters
                    if userName[0][0] == intials[0] and userName[-1][0] == initials[-1]:
                        print(f"Initial matched with {user['username']}")
                    
                for phrase in userBio:
                    for date in searchDates:
                        if phrase.find(date) != -1:
                            print(f"Date: {date} found in {user['username']} Bio")
        else:
            print("No Initials or Dates Found")

        '''
