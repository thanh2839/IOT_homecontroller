import os
import random
import shutil
from itertools import islice

outputFolderPath = "Dataset/SplitData"
inputFolderPath = "Dataset/All"
splitRatio = {"train": 0.7, "val": 0.2, "test": 0.1}
classes = ["fake", "real"]

try:
    shutil.rmtree(outputFolderPath)
    print("Remove Directory")
except OSError as e:
    os.mkdir(outputFolderPath)


# Create Directories
os.makedirs(f"{outputFolderPath}/train/images", exist_ok=True)
os.makedirs(f"{outputFolderPath}/train/labels", exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/images", exist_ok=True)
os.makedirs(f"{outputFolderPath}/val/labels", exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/images", exist_ok=True)
os.makedirs(f"{outputFolderPath}/test/labels", exist_ok=True)

# Get names
listNames = os.listdir(inputFolderPath)
print(len(listNames))
uniqueNames = []
for name in listNames:
    uniqueNames.append(name.split(".")[0])
uniqueNames = list(set(uniqueNames))

# Shuffle
random.shuffle(uniqueNames)

# Find number of each folder
lenData = len(uniqueNames)
print(f"Total Images: {lenData}")
lenTrain = int(lenData * splitRatio["train"])
lenVal = int(lenData * splitRatio["val"])
lenTest = int(lenData * splitRatio["test"])

# Put remaining images in Training
if lenData != lenTrain + lenVal + lenTest:
    remaining = lenData - (lenTrain + lenVal + lenTest)
    lenTrain += remaining
print(f"Total Images: {lenData} \nSplit: {lenTrain} {lenVal} {lenTest}")

# Split the list
lengthToSplit = [lenTrain, lenVal, lenTest]
Input = iter(uniqueNames)
Output = [list(islice(Input, elem)) for elem in lengthToSplit]

# Copy the files
sequence = ["train", "val", "test"]
for i, out in enumerate(Output):
    for fileName in out:
        shutil.copy(
            f"{inputFolderPath}/{fileName}.jpg",
            f"{outputFolderPath}/{sequence[i]}/images/{fileName}.jpg",
        )
        shutil.copy(
            f"{inputFolderPath}/{fileName}.txt",
            f"{outputFolderPath}/{sequence[i]}/labels/{fileName}.txt",
        )

dataYaml = f"path: ../Data\n\
train: ../train/images\n\
val: ../val/images\n\
test: ../test/images\n\
\n\
nc: {len(classes)}\n\
names: {classes}"

dataYamlOffline= f"path: E:\IOT\DataSet\SplitData\n\
train: train/images\n\
val: val/images\n\
test: test/images\n\
\n\
nc: {len(classes)}\n\
names: {classes}"
f = open(f"{outputFolderPath}/data.yaml", "a")
f.write(dataYaml)
f.close()
f = open(f"{outputFolderPath}/dataOffline.yaml", "a")
f.write(dataYamlOffline)
f.close()
print("Created data yaml")
