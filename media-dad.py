#!/usr/bin/python

import click
from bin.services import *

def getDadJoke():
    joke = os.system("curl -H 'Accept: text/plain' https://icanhazdadjoke.com/")

def printMediaDad():
    print("___  ___         _ _      ______          _ ")
    print("|  \/  |        | (_)     |  _  \        | |")
    print("| .  . | ___  __| |_  __ _| | | |__ _  __| |")
    print("| |\/| |/ _ \/ _` | |/ _` | | | / _` |/ _` |")
    print("| |  | |  __/ (_| | | (_| | |/ / (_| | (_| |")
    print("\_|  |_/\___|\__,_|_|\__,_|___/ \__,_|\__,_|\n")
    print("While we wait let me tell you a joke: ")
    getDadJoke()
    print("\n")

def getService(name):
    if name == "plex":
        return Plex()
    if name == "sickrage":
        return SickRage()
    if name == "tautulli":
        return Tautulli()
    if name == "transmission":
        return Transmission()
    if name == "ombi":
        return Ombi()
    if name == "ouroboros":
        return Ouroboros()
    if name == "couchpotato":
        return CouchPotato()
    if name == "all":
        return All()

def stopService(name):
    getService(name).stopContainer()
    getService(name).removeContainer()

@click.command()
@click.argument('name', nargs=1)
@click.option('-r/--run', 'run', default=False)
@click.option('-s/--stop', 'stop', default=False)
@click.option('-u/--update', 'update', default=False)
@click.option('-b/--backup', 'backup', default=False)
@click.option('-y/--sync', 'sync', default=False)
def main(name, run, stop, update, backup, sync):

    if run:
        #Run Service
        stopService(name)
        getService(name).runContainer()

    if stop:
        #Stop Service
        stopService(name)

    if update:
        #Update Service
        stopService(name)
        getService(name).updateContainer()
        getService(name).runContainer()

    if backup:
        #Backup Service
        stopService(name)
        getService(name).backupContainer()
        getService(name).updateContainer()
        getService(name).runContainer()

    if sync:
        stopService(name)
        getService(name).backupContainer()
        getService(name).updateContainer()
        getService(name).syncBackup()
        getService(name).runContainer()


    print('')

if __name__ == '__main__':
    printMediaDad()
    main()
