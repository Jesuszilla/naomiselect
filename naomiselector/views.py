from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from naomiselector.models import Game
from naomiselect.tasks import runGame, getMD5Hash
from celery.result import ResultSet
import naomi_boot as naomi
import json
import os
import time
import hashlib

# Constants
NAME_OFFSET = 0x30
NAME_LENGTH = 0x20


# Main call
def getROMList(request):
    roms = []
    getAllROMs(roms)
    return HttpResponse(json.dumps(roms))

# Request to select a particular game 
def selectROM(request):
    # Only valid request is POST
    if request.method == "GET": 
        if runGame.delay(request.GET.get('game', "")).get() == True:
            return HttpResponse("Game loading!")
        else:
            return HttpResponse("Game could not start.");
    else:
        return HttpResponseBadRequest("Invalid request.")


# Helper methods

# Returns all ROMs in the ROM directory specified by the ROMS_FOLDER in settings.py
def getAllROMs(roms):
    for file in os.listdir(settings.ROMS_FOLDER):
        if file.endswith(".bin"):
            fullPath = settings.ROMS_FOLDER + "/" + file
            f = open(fullPath, 'r')
            f.seek(0x30)
            rom = {}
            rom['filename'] = file
            rom['name'] = f.read(NAME_LENGTH)
            roms.append(rom)
            f.close()

    # Get the MD5 hash for each ROM
    results = getHashes(roms)

    # Now add the videos to the ROMs
    idx = 0
    for rom in roms:
        theQuakerQuery = Game.objects.raw("SELECT id,video FROM naomiselector_game WHERE hash=\'" + results[idx] + "\'")
        if len(list(theQuakerQuery)) > 0:
            rom['video'] = "https://www.youtube.com/embed/" + theQuakerQuery[0].video
        else:
            rom['video'] = ''
        idx += 1

    return roms

# Gets the hashes for the games.
def getHashes(roms):
    resultSet = ResultSet([])
    for rom in roms:
        # Need the full path for the MD5 hash function to operate on the file
        fullPath = settings.ROMS_FOLDER + "/" + rom['filename']
        resultSet.add(getMD5Hash.delay(fullPath))
    return resultSet.get()

# Runs the damn game
#def runGame(game):
#    # Display "Now loading..."
#    naomi.HOST_SetMode(settings.DEVICE_IP, 0, 1)

#    # Disable encryption by setting magic zero-key
#    naomi.SECURITY_SetKeycode("\x00" * 8)

#    # Uploads file. Also sets "dimm information" (file length and CRC32)
#    naomi.DIMM_UploadFile(settings.ROMS_FOLDER + game)

#    # Restart host to boot into game
#    naomi.HOST_Restart()

#    # Set time limit to 10h.
#    while True:
#        naomi.TIME_SetLimit(10*60*1000)
#        time.sleep(5)

#    return True

# Gets the MD5 checksum
#def getMD5Hash(path, block_size=256*128, hr=True):
#    '''
#    Block size directly depends on the block size of your filesystem
#    to avoid performances issues
#    Here I have blocks of 4096 octets (Default NTFS)
#    '''
#    md5 = hashlib.md5()
#    with open(path,'rb') as f: 
#        for chunk in iter(lambda: f.read(block_size), b''): 
#             md5.update(chunk)
#    if hr:
#        return md5.hexdigest()
#    return md5.digest()

# Gets the SHA1 hash
def getSHA1Hash(filename):
    sha1 = hashlib.sha1()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(128*sha1.block_size), b''):
            sha1.update(chunk)
    return sha1.hexdigest()
