# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os


def getStartTimeStr(target_time):
    targetHours = int(target_time / oneHoursSeconds)
    if targetHours > 9:
        targetHoursStr = str(targetHours)
    else:
        targetHoursStr = "0" + str(targetHours)
    target_time = target_time - targetHours * oneHoursSeconds
    targetMinutes = int(target_time / 60)
    if targetMinutes > 9:
        targetMinutesStr = str(targetMinutes)
    else:
        targetMinutesStr = "0" + str(targetMinutes)
    target_time = target_time - targetMinutes * 60
    targetSeconds = target_time
    if targetSeconds > 9:
        targetSecondsStr = str(targetSeconds)
    else:
        targetSecondsStr = "0" + str(targetSeconds)
    return targetHoursStr + ":" + targetMinutesStr + ":" + targetSecondsStr


# 一小时的秒, 单位是秒
oneHoursSeconds = 3600
# 单位是秒
startOmitTime = 0
# 单位是秒
targetSplitVideoLength = 5 * 60
# 目标视频文件
targetVideoPath = "/Users/xiaojinzi/Documents/video/夏洛特烦恼/夏洛特烦恼.mp4"
targetVideoFolder = os.path.dirname(targetVideoPath)
targetVideoName = os.path.basename(targetVideoPath)
print(targetVideoFolder)
print(targetVideoName)

durationStr = os.popen("ffmpeg -i " + targetVideoPath + " 2>&1 | grep 'Duration'").read()
durationStr = durationStr.split(",")[0]
durationPrefixStr = "Duration: "
durationStrIndex = durationStr.index(durationPrefixStr) + len(durationPrefixStr)
durationStr = durationStr[durationStrIndex: durationStrIndex + 8]
print("读到的时长：" + durationStr)
timeStrArr = durationStr.split(":")
totalSeconds = int(timeStrArr[0]) * 60 * 60 + int(timeStrArr[1]) * 60 + int(timeStrArr[2]) + 1

print("totalSeconds = " + str(totalSeconds))
print("totalSeconds = " + getStartTimeStr(totalSeconds))

isAddOne = (totalSeconds % targetSplitVideoLength) != 0
loopCount = int(totalSeconds / targetSplitVideoLength)
if isAddOne:
    loopCount = loopCount + 1

exportDir = targetVideoFolder + "/target"
isExistTargetExportDir = os.path.exists(exportDir)
if not isExistTargetExportDir:
    os.mkdir(exportDir)

print("exportDir = " + exportDir)

for index in range(loopCount):
    startTimeStr = getStartTimeStr(index * targetSplitVideoLength)
    targetCommand = "ffmpeg -ss " + startTimeStr + " -i " + targetVideoPath + " -c copy -t " + \
                    str(targetSplitVideoLength) + " " + exportDir + "/" + str(index + 1) + ".mp4"
    os.system(targetCommand)
