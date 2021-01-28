# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os


def getParentPath(target_path):
    return os.path.abspath(os.path.join(target_path, os.pardir))


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
isTest = False
# 一小时的秒, 单位是秒
oneHoursSeconds = 3600
# 单位是秒
startOmitTime = 0
# 字体文件
targetTTFFilePath = "/Users/xiaojinzi/Documents/code/python/Test1/ttfs/ttf1.ttf"
# 单位是秒
targetSplitVideoLength = 5 * 60 - 10
# 填充的颜色
fillColor = "black"
if isTest:
    fillColor = "red"
    targetSplitVideoLength = 30
# 视频真实显示区域的宽高比, 每个视频处理的时候, 必须重新赋值
targetVideoRealAspectRatio = 962 / 538
# 导出的 crop 的比例
targetVideoExportCropAspectRatio = 16 / 9
# 文字相对真实显示内容高度的比例
targetTextRatio = 10
# 导出的视频最终比例, 其余部分补黑边
targetVideoExportAspectRatio = 1 / 1
# 目标视频文件
targetVideoPath = "/Users/xiaojinzi/Documents/video/雷神1/雷神1.mp4"
targetVideoFolder = os.path.dirname(targetVideoPath)
targetExportDir = targetVideoFolder + "/target"
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

# -------------------------------- 是否需要裁减掉黑边
isNeedCropBlack = abs(videoHeight * targetVideoRealAspectRatio - videoWidth) >= 160
print("isNeedCropBlack = " + str(isNeedCropBlack))
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


# 实现原理的流程:
# 1. 裁掉上下两边的黑边
# 2.

# -------------------------------- 视频分片

# 分片视频的目标地址
partVideoExportList = []
for indexPart in range(loopCount):
    startTimeStr = getStartTimeStr(indexPart * targetSplitVideoLength)
    if isTest:
        partPath = targetExportDir + "/part_" + str(indexPart + 1) + ".mp4"
    else:
        partPath = targetExportDir + "/part_" + str(indexPart + 1) + ".mp4"
    partVideoExportList.append(partPath)
    if not os.path.exists(partPath):
        targetCommand = "ffmpeg -ss " + startTimeStr + " -i " + targetVideoPath + " -c copy -t " + \
                        str(targetSplitVideoLength) + " " + partVideoExportList[indexPart]
        os.system(targetCommand)

# -------------------------------- crop、 真实的视频
cropedList1 = []
cropWidth = int(videoWidth)
cropHeight = int(videoHeight)
if isNeedCropBlack:
    # 计算 crop 的宽和高
    cropWidth = int(videoWidth)
    cropHeight = videoWidth / targetVideoRealAspectRatio
    if cropHeight > videoHeight:
        cropHeight = videoHeight
    cropHeight = int(cropHeight)
    # 再根据高度, 算出宽度, crop 成 16 / 9
    # cropWidth = int(cropHeight * targetVideoExportCropAspectRatio)

    # print("cropWidth, cropHeight = " + str(cropWidth) + "," + str(cropHeight))

    for indexCrop1 in range(len(partVideoExportList)):
        croped1Path = targetExportDir + "/part_crop1_" + str(indexCrop1 + 1) + ".mp4"
        cropedList1.append(croped1Path)
        if not os.path.exists(croped1Path):
            targetCommand = "ffmpeg -i " + str(partVideoExportList[indexCrop1]) + \
                            " -vf crop=" + str(cropWidth) + ":" + str(cropHeight) + " " + \
                            str(croped1Path) + " -y"
            # crop 的执行
            os.system(targetCommand)
else:
    cropedList1 = partVideoExportList

# 裁减成为 16 / 9
cropWidth = int(cropHeight * targetVideoExportCropAspectRatio)

print("cropWidth ======= " + str(cropWidth))

for index2 in range(len(cropedList1)):
    # 真正内容的 y
    realVideoContent_y = int((cropWidth - cropHeight) / 2)

    # --------------- crop2
    croped2Path = targetExportDir + "/part_crop2_" + str(index2 + 1) + ".mp4"
    if not os.path.exists(croped2Path):
        targetCommand = "ffmpeg -i " + str(cropedList1[index2]) + \
                        " -vf crop=" + str(cropWidth) + ":" + str(cropHeight) + " " + \
                        str(croped2Path) + " -y"
        # crop 2 的执行
        os.system(targetCommand)
    # 拿一次新的数据
    videoWidthCroped2 = int(
        os.popen(
            "ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 " + str(croped2Path)).read()
    )
    videoHeightCroped2 = int(
        os.popen(
            "ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 " + str(croped2Path)).read()
    )
    cropWidth = videoWidthCroped2
    cropHeight = videoHeightCroped2

    print("videoWidthCroped2 = " + str(videoWidthCroped2))
    print("videoHeightCroped2 = " + str(videoHeightCroped2))

    # --------------- scale
    scaledPath = targetExportDir + "/part_crop_scale_" + str(index2 + 1) + ".mp4"
    if not os.path.exists(scaledPath):
        targetCommand = "ffmpeg -i " + str(croped2Path) + \
                        " -vf scale=" + str(cropWidth) + ":" + str(cropHeight) + \
                        ",pad=" + str(cropWidth) + ":" + str(cropWidth) + \
                        ":0:" + str(realVideoContent_y) + ":" + fillColor + " " \
                        + str(scaledPath)
        os.system(targetCommand)

    # --------------- 绘制文本：电视剧名称(index)
    textSize = int(cropHeight / targetTextRatio)
    textedPath = targetExportDir + "/part_crop_scale_text_" + str(index2 + 1) + ".mp4"
    if not os.path.exists(textedPath):
        targetCommand = "ffmpeg -i " + scaledPath + \
                        " -vf \"drawtext=fontfile=" + targetTTFFilePath + \
                        ":text='" + str(targetVideoSimpleName) + " (" + str(index2 + 1) + ")" + "'" + \
                        ":fontcolor=white:fontsize=" + str(textSize) + ":" \
                        "x=(w-text_w)/2:y=(" + str(realVideoContent_y) + "-text_h)/2\" " + str(textedPath)
        os.system(targetCommand)

    # --------------- 绘制小金子标记文本
    textedAuthorSize = int(cropHeight / targetTextRatio * 3 / 5)
    textedAuthorPath = targetExportDir + "/result/" + targetVideoName + "_" + str(index2 + 1) + ".mp4"
    textedAuthorParentPath = getParentPath(textedAuthorPath)
    if not os.path.exists(textedAuthorParentPath):
        os.mkdir(textedAuthorParentPath)
    if not os.path.exists(textedAuthorPath):
        targetCommand = "ffmpeg -i " + textedPath + \
                        " -vf \"drawtext=fontfile=" + targetTTFFilePath + \
                        ":text='" + str("小金子") + "'" + \
                        ":fontcolor=white:fontsize=" + str(textedAuthorSize) + ":" \
                        "x=(w-text_w-20):y=" + str(realVideoContent_y + 20) + "\" " + str(textedAuthorPath)
        os.system(targetCommand)
        print("targetCommand = " + targetCommand)
