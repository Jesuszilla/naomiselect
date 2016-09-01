from __future__ import absolute_import
from celery import shared_task, group
from django.conf import settings
from naomi_boot import NAOMI
import hashlib

# Runs the damn game
@shared_task
def runGame(game):
    try:
        # Create the NAOMI object
        naomi = NAOMI(settings.DEVICE_IP)

        # Display "Now loading..."
        res = naomi.HOST_SetMode(0, 1)

        loadGame.s(game).delay()

        return (res != "")
    except:
        return False

#    # Set time limit to 10h.
#    while True:
#        naomi.TIME_SetLimit(10*60*1000)
#        time.sleep(5)

@shared_task
def loadGame(game):
    try:
        # Create the NAOMI object. The device is already in the mode
        # we previously set.
        naomi = NAOMI(settings.DEVICE_IP)

        # Disable encryption by setting magic zero-key
        res = naomi.SECURITY_SetKeycode("\x00" * 8)

        # Uploads file. Also sets "dimm information" (file length and CRC32)
        res = naomi.DIMM_UploadFile(settings.ROMS_FOLDER + game)

        # Restart host to boot into game
        res = naomi.HOST_Restart()

        # Set time limit to 10h
        naomi.TIME_SetLimit(10*60*1000)

        return True
    # So uh-oh, we fucked up!
    except:
        return False

# Calculates the MD5 hash
@shared_task
def getMD5Hash(path, block_size=256*128, hr=True):
    '''
    Block size directly depends on the block size of your filesystem
    to avoid performances issues
    Here I have blocks of 4096 octets (Default NTFS)
    '''
    md5 = hashlib.md5()
    with open(path,'rb') as f: 
        for chunk in iter(lambda: f.read(block_size), b''): 
             md5.update(chunk)
    if hr:
        return md5.hexdigest()
    return md5.digest()
