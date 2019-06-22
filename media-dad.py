#!/usr/bin/python

import os
import subprocess
import click
import docker
from bin.services import *
from halo import Halo

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
    if name == "organizr":
        return Organizr()
    if name == "sickrage":
        return SickRage()
    if name == "tautulli":
        return Tautulli()
    if name == "transmission":
        return Transmission()

@click.command()
@click.argument('name', nargs=1)
@click.option('-r/--run', 'run', default=False)
@click.option('-s/--stop', 'stop', default=False)
@click.option('-u/--update', 'update', default=False)
def main(name, run, stop, update, convert):

    if run:
        #Run Service
        getService(name).runContainer()
    if stop:
        #Stop Service
        getService(name).stopContainer()
    if update:
        getService(name).updateContainer()
    print("")

if __name__ == '__main__':
    printMediaDad()
    main()
