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


# 是否测试
isTest = True
# 一小时的秒, 单位是秒
oneHoursSeconds = 3600
# 单位是秒
startOmitTime = 0
# 单位是秒
targetSplitVideoLength = 5 * 60
if isTest:
    targetSplitVideoLength = 5
# 视频真实显示区域的宽高比
targetVideoRealAspectRatio = 1081 / 300
# 目标视频文件
targetVideoPath = "/Users/xiaojinzi/Documents/video/功夫/功夫.mkv"
# targetVideoPath = "/Users/xiaojinzi/Documents/video/西虹市首富/西虹市首富.mp4"
targetVideoFolder = os.path.dirname(targetVideoPath)
targetExportDir = targetVideoFolder + "/targetTest"
targetVideoName = os.path.basename(targetVideoPath)
isMp4 = targetVideoPath[-4:] == ".mp4"

print("是否是 Mp4 文件：" + str(isMp4))
print(targetVideoFolder)
print(targetVideoName)
print()

# -------------------------------- 读取视频大小
# videoSizeStr = os.popen("ffmpeg -i " + targetVideoPath + " 2>&1 | grep 'Stream #0:0: Video'").read()
videoWidth = int(
    os.popen(
        "ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 " + targetVideoPath).read()
)
videoHeight = int(
    os.popen(
        "ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 " + targetVideoPath).read()
)

print("videoWidth = " + str(videoWidth))
print("videoHeight = " + str(videoHeight))

print()

# -------------------------------- 是否需要裁减
isNeedCrop = abs(videoHeight * targetVideoRealAspectRatio - videoWidth) >= 160
print("isNeedCrop = " + str(isNeedCrop))
print()

# -------------------------------- 读取视频时长
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

# -------------------------------- 分片的个数
isAddOne = (totalSeconds % targetSplitVideoLength) != 0
loopCount = int(totalSeconds / targetSplitVideoLength)
if isAddOne:
    loopCount = loopCount + 1

if isTest:
    loopCount = 1

# -------------------------------- 创建目标文件夹
isExistTargetExportDir = os.path.exists(targetExportDir)
if not isExistTargetExportDir:
    os.mkdir(targetExportDir)

print("exportDir = " + targetExportDir)

# -------------------------------- 视频分片

# 分片视频的目标地址
partVideoExportList = []
for indexPart in range(loopCount):
    startTimeStr = getStartTimeStr(indexPart * targetSplitVideoLength)
    partVideoExportList.append(targetExportDir + "/part_" + str(indexPart + 1) + ".mp4")
    targetCommand = "ffmpeg -ss " + startTimeStr + " -i " + targetVideoPath + " -c copy -t " + \
                    str(targetSplitVideoLength) + " " + partVideoExportList[indexPart]
    os.system(targetCommand)

# -------------------------------- crop 真实的视频
cropedList = []
if isNeedCrop:
    cropWidth = int(videoWidth)
    cropHeight = videoWidth / targetVideoRealAspectRatio
    if cropHeight > videoHeight:
        cropHeight = videoHeight
    cropHeight = int(cropHeight)

    for indexCrop in range(len(partVideoExportList)):
        cropedList.append(targetExportDir + "/part_crop_" + str(indexCrop + 1) + ".mp4")
        # 命令
        targetCommand = "ffmpeg -i " + str(partVideoExportList[indexCrop]) + \
                        " -vf crop=" + str(cropWidth) + ":" + str(cropHeight) + " " + \
                        str(cropedList[indexCrop]) + " -y"
        print("targetCommand = " + targetCommand)
        os.system(targetCommand)
else:
    cropedList = partVideoExportList
