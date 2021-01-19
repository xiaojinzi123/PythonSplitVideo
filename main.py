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


tempIndex = -1
# 是否测试
isTest = True
# 一小时的秒, 单位是秒
oneHoursSeconds = 3600
# 单位是秒
startOmitTime = 0
# 字体文件
targetTTFFilePath = "/Users/xiaojinzi/Documents/code/python/Test1/ttfs/ttf1.ttf"
# 单位是秒
targetSplitVideoLength = 5 * 60
if isTest:
    targetSplitVideoLength = 30
# 视频真实显示区域的宽高比
targetVideoRealAspectRatio = 948 / 393
# 导出的 crop 的比例
targetVideoExportCropAspectRatio = 16 / 9
# 导出的视频最终比例, 其余部分补黑边
targetVideoExportAspectRatio = 1 / 1
# 目标视频文件
targetVideoPath = "/Users/xiaojinzi/Documents/video/功夫/功夫.mkv"
# targetVideoPath = "/Users/xiaojinzi/Documents/video/西虹市首富/西虹市首富.mp4"
targetVideoFolder = os.path.dirname(targetVideoPath)
targetExportDir = targetVideoFolder + "/targetTest"
targetVideoName = os.path.basename(targetVideoPath)
targetVideoSimpleName = targetVideoName
isMp4 = targetVideoPath[-4:] == ".mp4"
tempIndex = targetVideoName.index(".")
if tempIndex >= 0:
    targetVideoSimpleName = targetVideoName[0:tempIndex]

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
    if isTest:
        partPath = targetExportDir + "/part_" + str(indexPart + 1) + ".mp4"
    else:
        partPath = targetExportDir + "/part/part_" + str(indexPart + 1) + ".mp4"
    partVideoExportList.append(partPath)
    targetCommand = "ffmpeg -ss " + startTimeStr + " -i " + targetVideoPath + " -c copy -t " + \
                    str(targetSplitVideoLength) + " " + partVideoExportList[indexPart]
    os.system(targetCommand)

# -------------------------------- crop、 真实的视频
cropedList = []
if isNeedCrop:
    # 计算 crop 的宽和高
    cropWidth = int(videoWidth)
    cropHeight = videoWidth / targetVideoRealAspectRatio
    if cropHeight > videoHeight:
        cropHeight = videoHeight
    cropHeight = int(cropHeight)
    # 再根据高度, 算出宽度, crop 成 16 / 9
    cropWidth = int(cropHeight * targetVideoExportCropAspectRatio)

    # print("cropWidth, cropHeight = " + str(cropWidth) + "," + str(cropHeight))

    for indexCrop in range(len(partVideoExportList)):
        cropedPath = targetExportDir + "/part_crop_" + str(indexCrop + 1) + ".mp4"
        cropedList.append(cropedPath)
        # 命令
        targetCommand = "ffmpeg -i " + str(partVideoExportList[indexCrop]) + \
                        " -vf crop=" + str(cropWidth) + ":" + str(cropHeight) + " " + \
                        str(cropedList[indexCrop]) + " -y"
        # crop 的执行
        os.system(targetCommand)
        # scale
        scaledPath = targetExportDir + "/part_crop_scale_" + str(indexCrop + 1) + ".mp4"
        targetCommand = "ffmpeg -i " + str(cropedPath) + \
                        " -vf scale=" + str(cropWidth) + ":" + str(cropHeight) + \
                        ",pad=" + str(cropWidth) + ":" + str(cropWidth) + ":0:206:red " + str(scaledPath)
        os.system(targetCommand)
        # 绘制文本：电视剧名称(index)
        realVideoContent_y = int((cropWidth - cropHeight) / 2)
        textedPath = targetExportDir + "/part_crop_scale_text_" + str(indexCrop + 1) + ".mp4"
        targetCommand = "ffmpeg -i " + scaledPath + \
                        " -vf \"drawtext=fontfile=" + targetTTFFilePath + \
                        ":text='" + str(targetVideoSimpleName) + "(" + str(indexCrop + 1) + ")" + "'" + \
                        ":fontcolor=white:fontsize=50:" \
                        "x=(w-text_w)/2:y=(" + str(realVideoContent_y) + "-text_h)/2\" " + str(textedPath)
        os.system(targetCommand)
        # 绘制小金子标记文本
        textedAuthorPath = targetExportDir + "/part_crop_scale_text_author_" + str(indexCrop + 1) + ".mp4"
        targetCommand = "ffmpeg -i " + textedPath + \
                        " -vf \"drawtext=fontfile=" + targetTTFFilePath + \
                        ":text='" + str("小金子") + "'" + \
                        ":fontcolor=white:fontsize=30:" \
                        "x=(w-text_w-20):y=" + str(realVideoContent_y + 20) + "\" " + str(textedAuthorPath)
        os.system(targetCommand)
        print("targetCommand = " + targetCommand)
else:
    cropedList = partVideoExportList
