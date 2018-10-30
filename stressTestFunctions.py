import os, sys
import shutil
import json
import time
import numpy as np
import synapseclient
from synapseclient import File
from subprocess import call

# If being throttled by Synapse:
# This will make multipart file uploads slower as we will only get 1 presigned URL at a time
# synapseclient.config.single_threaded = True


syn = synapseclient.login()

def setProjectBucket(project_id, bucket_name):
    destination = {
                   'uploadType':'S3', 
                   'concreteType':'org.sagebionetworks.repo.model.project.ExternalS3StorageLocationSetting',
                   'bucket': bucket_name
                  }
    destination = syn.restPOST('/storageLocation', body=json.dumps(destination))
    project_destination = {
                           'concreteType': 'org.sagebionetworks.repo.model.project.UploadDestinationListSetting', 
                           'settingsType': 'upload'
                          }
    project_destination['locations'] = [destination['storageLocationId']]
    project_destination['projectId'] = project_id
    project_destination = syn.restPOST('/projectSettings', body = json.dumps(project_destination))

def createDummyFile(size_in_kb, name):
    if not os.path.exists("./dummy"):
        os.makedirs("./dummy")
    # We make the data pseudorandom to avoid unknown optimizations when uploading/downloading something like /dev/zero
    # This is a relatively speedy way to do it (though not very portable).
    # See: https://superuser.com/questions/792427/creating-a-large-file-of-random-bytes-quickly/792505
    call("dd if=<(openssl enc -aes-256-ctr -pass pass:\"$(dd if=/dev/urandom bs=128 count=1 2>/dev/null | base64)\" -nosalt < /dev/zero) of=./dummy/" + name + " bs=1024 count=" + str(size_in_kb), shell=True, executable="/bin/bash")

# Returns time it took to store the file
def timedFileUpload(filepath, project_id):
    file = File(path=filepath, parent=project_id)
    start = time.time()
    file = syn.store(file)
    end = time.time()
    return(end - start)


def timedFileDownload(entity):
    shutil.rmtree(os.path.expanduser(synapseclient.cache.CACHE_ROOT_DIR))
    start = time.time()
    syn.get(entity)
    end = time.time()
    return(end - start)

# Returns list of times it took to upload files
def uploadStressTest(num_files, file_size_kb, project_id):
    # create n files
    for i in range(num_files):
        createDummyFile(file_size_kb, "output_" + str(i) + ".dat")
    
    times = []
    for i in range(num_files):
        times.append(timedFileUpload("./dummy/output_" + str(i) + ".dat", project_id))
        
    return times

def downloadStressTest(project_id):
    times = []
    for entity in syn.getChildren(project_id):
        times.append(timedFileDownload(entity["id"]))
    
    return times

def deleteAllFilesFromProject(project_id):
    for entity in syn.getChildren(project_id):
        syn.delete(entity["id"])
    
def saveToCsv(array, outfile):
    np.savetxt(outfile, np.array(array), delimiter=",")

