import os, sys
from time import gmtime, strftime
import stressTestFunctions as util
import pandas as pd
import synapseclient
from synapseclient import File

syn = synapseclient.login()

dataProjectId = 'syn17018506'
encryptedProjectId = 'syn17016492'
unencryptedProjectId = 'syn17016502'
encryptedBucketName = 'plfm-5212-encrypted-bucket'
unencryptedBucketName = 'plfm-5212-unencrypted-bucket'

# setProjectBucket(encryptedProjectId, encryptedBucketName)
# setProjectBucket(unencryptedProjectId, unencryptedBucketName)

def upload_download_test(num_files, file_size_kb):
    # Empty the project space beforehand
    util.deleteAllFilesFromProject(unencryptedProjectId)
    util.deleteAllFilesFromProject(encryptedProjectId)
    # Test the unencrypted bucket and empty it
    unencrypted_up_times = util.uploadStressTest(num_files, file_size_kb, unencryptedProjectId)
    unencrypted_down_times = util.downloadStressTest(unencryptedProjectId)
    util.deleteAllFilesFromProject(unencryptedProjectId)
    # Test the encrypted bucket and empty it
    encrypted_up_times = util.uploadStressTest(num_files, file_size_kb, encryptedProjectId)
    encrypted_down_times = util.downloadStressTest(encryptedProjectId)
    util.deleteAllFilesFromProject(encryptedProjectId)
    # Assemble the dataframe and return it
    df = pd.DataFrame({"time": unencrypted_up_times, "bucket": "unencrypted", "type": "upload", "file_size": file_size_kb})
    df = df.append(pd.DataFrame({"time": encrypted_up_times, "bucket": "encrypted", "type": "upload", "file_size": file_size_kb}))
    df = df.append(pd.DataFrame({"time": unencrypted_down_times, "bucket": "unencrypted", "type": "download", "file_size": file_size_kb}))
    df = df.append(pd.DataFrame({"time": encrypted_down_times, "bucket": "encrypted", "type": "download", "file_size": file_size_kb}))
    return df

df = pd.DataFrame()

# Test 1KB, 1MB, 5MB, 50MB, 100MB, 1GB
for file_size_kb in [1, 1024, 1024 * 10, 1024 * 50, 1024 * 100, 1024 * 500, 1024 * 1024]:
    df = df.append(upload_download_test(num_files=25, file_size_kb=file_size_kb))

outfile = "output_data_" + strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + ".csv"
df.to_csv(outfile, index = False)

syn.store(File(path=outfile, parent=dataProjectId))
