# Blue Spirit Program

from InstagramAPI import InstagramAPI
import getpass
import argparse
import unicodedata
import re
import time
import tkinter as tk
import functionsREAL as scan



parser = argparse.ArgumentParser(description="Blue Spirit Instagram Snooping Tool")

##########   START LOGIN   ##########

myUsername = input("Please enter username: ")
myPassword = getpass.getpass(prompt="Please enter password: ")

api = InstagramAPI(myUsername, myPassword)
api.login()


######### START GUI ##########
window = tk.Tk(className="Blue Spirit Social Snooping")

mainTitle = tk.Label(text="Blue Spirit Instagram Snooping Tool", fg="yellow", bg="black")

targetTitle = tk.Label(text="Enter your target's Instagram Handle", fg="yellow", bg="black")
targetEntry = tk.Entry(width=50)
userTitle = tk.Label(text="Your Details", fg="yellow", bg="black")
userDetails = tk.Text(width=100, height=7)
fakesTitle = tk.Label(text="Who Doesn't Follow You Back", fg="yellow", bg="black")
fakesDetails = tk.Text(width=100, height=7)
targetInfoTitle = tk.Label(text="Your Target's Details", fg="yellow", bg="black")
targetDetails = tk.Text(width=100, height=7)
familyTitle = tk.Label(text="Your Target's Family Members on Instagram", fg="yellow", bg="black")
familyDetails = tk.Text(width=100, height=7)


submit = tk.Button(
    text="Submit",
    width=25,
    height=5,
    bg="white",
    fg="black",
    command= lambda: scan.run_scan(api, targetEntry, userDetails, fakesDetails, targetDetails, familyDetails)
)

targetTitle.pack()
targetEntry.pack()
submit.pack()
userTitle.pack()
userDetails.pack()
fakesTitle.pack()
fakesDetails.pack()
targetInfoTitle.pack()
targetDetails.pack()
familyTitle.pack()
familyDetails.pack()



window['bg'] = "black"
window.mainloop()


   

