#!/usr/bin/python

import docker
import os
from halo import Halo

################################################################################
################################################################################

class Service:

    def __init__(self):
        self.dockerClient = docker.from_env()
        self.capAdd = {}
        self.network = "bridge"
        self.restartType = {'Name': 'always'}
        self.timezone = "America/Denver"
        self.env = {}
        self.log = {}
        self.spinner = Halo(spinner='dots')
        self.ports = {}
        self.volumes = {}
        self.links = {}

    def runContainer(self):
        self.stopContainer()
        self.removeContainer()

        try:
            self.spinner.start(self.name + " - Starting")
            self.dockerClient.containers.run(
                self.image,
                name=self.name,
                cap_add=self.capAdd,
                network_mode=self.network,
                restart_policy=self.restartType,
                environment=self.env,
                volumes=self.volumes,
                ports=self.ports,
                log_config=self.log,
                links=self.links,
                detach=True
            )
            self.spinner.succeed(self.name + " - Started")
        except:
            self.spinner.fail(self.name + " - Failed To Start")

    def stopContainer(self):
        try:
            self.spinner.start(self.name + " - Stopping")
            container = self.dockerClient.containers.get(self.name).stop()
            self.spinner.succeed(self.name + " - Stopped")
        except:
            self.spinner.fail(self.name + " - Failed To Stop")

    def removeContainer(self):
        try:
            self.spinner.start(self.name + " - Removing")
            self.dockerClient.containers.get(self.name).remove()
            self.spinner.succeed(self.name + " - Removed")
        except:
            self.spinner.fail(self.name + " - Failed To Removed")

    def updateContainer(self):
        try:
            self.spinner.start(self.name + " - Updating")
            self.dockerClient.containers.get(self.name).restart()
            self.spinner.succeed(self.name + " - Updated")
        except:
            self.spinner.fail(self.name + " - Failed To Update")

    def backupContainer(self):
        try:
            self.spinner.start(self.name + " - Backing Up")
            os.system('cd /apps && tar -czf ./backup/'+self.name+'.tar.gz ./'+self.name)
            self.spinner.succeed(self.name + " - Backed Up")
        except:
            self.spinner.fail(self.name + " - Failed To Backup")

################################################################################
################################################################################

class Organizr(Service):

    def __init__(self):
        super(Organizr, self).__init__()
        self.image = "organizrtools/organizr-v2:latest"
        self.name = "organizr"
        self.volumes = {'/apps/'+self.name: {'bind': '/config', 'mode': 'rw'}}
        self.env = {'TZ':  self.timezone}
        self.ports = {'80/tcp': 80, '443/tcp': 443}

################################################################################
################################################################################

class SickRage(Service):

    def __init__(self):
        super(SickRage, self).__init__()
        self.image = "sickrage/sickrage:latest"
        self.name = "sickrage"
        self.volumes = {'/apps/'+self.name: {'bind': '/config', 'mode': 'rw'},
                        '/local_media/downloads': {'bind': '/downloads', 'mode': 'rw'},
                        '/local_media/tv_shows': {'bind': '/tv', 'mode': 'rw'}}
        self.env = {'TZ': self.timezone}
        self.ports = {'8081/tcp': 8081}

################################################################################
################################################################################

class Tautulli(Service):

    def __init__(self):
        super(Tautulli, self).__init__()
        self.image = "tautulli/tautulli:latest"
        self.name = "tautulli"
        self.volumes = {'/apps/'+self.name: {'bind': '/config', 'mode': 'rw'},
                        '/apps/plex/Library/Application\ Support/Plex\ Media\ Server/Logs': {'bind': '/plex_logs', 'mode': 'ro'}}
        self.env = {'TZ': self.timezone}
        self.ports = {'8181/tcp': 8181}

################################################################################
################################################################################

class Plex(Service):

    def __init__(self):
        super(Plex, self).__init__()
        self.image = "plexinc/pms-docker:public"
        self.name = "plex"
        self.network = "host"
        self.volumes = {'/apps/'+self.name: {'bind': '/config', 'mode': 'rw'},
                        '/local_media/transcode': {'bind': '/transcode', 'mode': 'rw'},
                        '/local_media': {'bind': '/local_media', 'mode': 'rw'}}
        self.env = {'TZ': self.timezone}

################################################################################
################################################################################

class Transmission(Service):

    def __init__(self):
        super(Transmission, self).__init__()
        self.image = "haugene/transmission-openvpn:latest"
        self.name = "transmission"
        self.capAdd = "NET_ADMIN"
        self.log = {'Type': 'json-file'}
        self.volumes = {'/apps/'+self.name: {'bind': '/data', 'mode': 'rw'},
                        '/local_media/downloads': {'bind': '/downloads', 'mode': 'rw'},
                        '/etc/localtime': {'bind': '/etc/localtime', 'mode': 'ro'}}
        self.env = {'TZ': self.timezone,
                    'CREATE_TUN_DEVICE': True,
                    'OPENVPN_PROVIDER': 'WINDSCRIBE',
                    'OPENVPN_CONFIG': 'US-West-tcp',
                    'OPENVPN_USERNAME': 'yatesab12_cq53bd',
                    'OPENVPN_PASSWORD': 'bsd7rwthc8',
                    'WEBPROXY_ENABLED': False,
                    'LOCAL_NETWORK': '192.168.29.0/24',
                    'TRANSMISSION_DOWNLOAD_DIR': '/downloads/complete',
                    'TRANSMISSION_INCOMPLETE_DIR': '/downloads/incomplete',
                    'TRANSMISSION_RPC_AUTHENTICATION_REQUIRED': True,
                    'TRANSMISSION_RPC_USERNAME': 'yatesab',
                    'TRANSMISSION_RPC_PASSWORD': 'Aug0616!',
                    'TRANSMISSION_SPEED_LIMIT_UP_ENABLED': True,
                    'TRANSMISSION_SPEED_LIMIT_UP': '0',
                    'TRANSMISSION_RATIO_LIMIT': '0',
                    'TRANSMISSION_RATIO_LIMIT_ENABLED': True,
                    'TRANSMISSION_DOWNLOAD_QUEUE_SIZE': '2'}
        self.ports = {'9091/tcp': 9092}
        self.proxy = TransmissionProxy()

    def runContainer(self):
        super(Transmission, self).runContainer()
        self.proxy.runContainer()

    def stopContainer(self):
        super(Transmission, self).stopContainer()
        self.proxy.stopContainer()

    def removeContainer(self):
        super(Transmission, self).removeContainer()
        self.proxy.removeContainer()

    def updateContainer(self):
        super(Transmission, self).updateContainer()
        self.proxy.updateContainer()

################################################################################
################################################################################

class TransmissionProxy(Service):

    def __init__(self):
        super(TransmissionProxy, self).__init__()
        self.image = "haugene/transmission-openvpn-proxy"
        self.name = "transmission-proxy"
        self.ports = {'8080/tcp': 9091}
        self.links = {'transmission': 'transmission'}

################################################################################
################################################################################

class All():

    services = { SickRage(), Tautulli(), Transmission(), Plex() }

    def __init__(self):
        super(All, self).__init__()

    def runContainer(self):
        for service in self.services:
            service.runContainer()
            print('')

    def stopContainer(self):
        for service in self.services:
            service.stopContainer()
            print('')

    def removeContainer(self):
        for service in self.services:
            service.removeContainer()
            print('')

    def updateContainer(self):
        for service in self.services:
            service.updateContainer()
            print('')

    def backupContainer(self):
        for service in self.services:
            service.backupContainer()
            print('')
