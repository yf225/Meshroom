__version__ = "0.1"

from meshroom.core import desc
import os
import cv2 as cv
import numpy as np
import math
import json


class DepthMapImport(desc.CommandLineNode):
    commandLine = 'aliceVision_depthMapImport {allParams}'
    category = 'Dense Reconstruction'
    documentation = '''
Import depth maps (Kinect, Android Tof, ....). Thoses imported depth maps can override calculated depthmaps or enhance them.
That script expect the depth image to be aside the rgb image, and have similar name (eg 0000234_image.jpg 0000234_depth16.bin)
'''

    inputs = [
        desc.File(
            name='input',
            label='Views and Poses',
            description='Path views and poses generated by StructureFromMotion node (usually cameras.sfm)',
            value='',
            uid=[0],
        ),    
        desc.File(
            name="depthMapsFolder",
            label="DepthMaps Folder",
            description="Input depth maps folder to calculate the scale between calculated depthMaps and imported depthMaps",
            value="/fsx/users/willfeng/3d_recon/images_jpg_depth/steamer",
            uid=[0],
        ),
        desc.StringParam(
            name='rgbImageSuffix',
            label='Rgb Image suffix',
            description='Used to guess the depthImage filename using the rgbImage filename: rgbPath.replace(rgbImageSuffix, depthImageSuffix)',
            value=".jpg",
            uid=[0],
            advanced=True,
        ),
        desc.StringParam(
            name='depthImageSuffix',
            label='Depth Image suffix',
            description='Used to guess the depthImage filename using the rgbImage filename: rgbPath.replace(rgbImageSuffix, depthImageSuffix)',
            value="-depth.jpg",
            uid=[0],
            advanced=True,
        ),
        desc.StringParam(
            name='depthIntrinsics',
            label='Depth Image Intrinsics',
            description='The depth image intrinsics are expected to be similar than rgb image. If unset will use assume than rgbIntrinsics==depthIntrincis',
            value='{"w": 240,"h": 180,"fx": 178.8240,"fy": 179.2912,"cx": 119.8185,"cy": 90.5689}', #Honor View 20 intrinsics
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='ratio',
            label='Ratio/Scale',
            description='Ratio between Sfm coordinate and imported depth. If 0, we will estimate it comparating center point of 1st image. Usually imported depth are in meters/millimeters',
            value=0,
            range=(0.0, 10.0, 0.1), #I dont want it, but thats mandatory
            uid=[0],
            advanced=True,
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='''verbosity level (fatal, error, warning, info, debug, trace).''',
            value='info',
            values=['fatal', 'error', 'warning', 'info', 'debug', 'trace'],
            exclusive=True,
            uid=[],
        ),
    ]

    outputs = [
        desc.File(
            name='output',
            label='Enhanced/Tof DepthMaps Folder',
            description='Output folder for generated depth maps.',
            value=desc.Node.internalFolder,
            uid=[],
        ),
    ]

    def processChunk(self, chunk):
        try:
            self._stopped = False
            chunk.logManager.start(chunk.node.verboseLevel.value)
            chunk.logger.info("started")

            inputCameras = chunk.node.input.value
            inputDepthMapsFolder = chunk.node.depthMapsFolder.value
            outputDepthMapsFolder = chunk.node.output.value
            depthIntrinsics = json.loads(chunk.node.depthIntrinsics.value)
            rgbImageSuffix = chunk.node.rgbImageSuffix.value
            depthImageSuffix = chunk.node.depthImageSuffix.value
            ratio = chunk.node.ratio.value

            self.importDepthMaps(chunk, inputCameras, inputDepthMapsFolder, outputDepthMapsFolder, depthIntrinsics, rgbImageSuffix, depthImageSuffix, ratio)

            chunk.logger.info("ended")
        except Exception as e:
            chunk.logger.error(e)
            raise RuntimeError()
        finally:
            chunk.logManager.end()

    def stopProcess(self, chunk):
        self._stopped = True


    def importDepthMaps(self, chunk, cameras, inputDepthMapsFolder, outputDepthMapsFolder, depthIntrinsics, rgbImageSuffix, depthImageSuffix, ratio = 0.0):
        try:
            f = open(cameras, )
            data = json.load(f)
        except Exception as e:
            raise Exception("here0")
        intrinsicsScaled = None

        for view in data["views"]:
            if self._stopped: raise RuntimeError("User asked to stop")
            rgb = view["path"]
            intputTofPath = rgb.replace(rgbImageSuffix, depthImageSuffix)  # add type png, jpg or depth16
            if not os.path.isfile(intputTofPath): raise Exception("Depth file not found", intputTofPath, "check if the file exists or if the rgbImageSuffix and depthImageSuffix are properly set")
            inputExrPath = inputDepthMapsFolder + "/" + view["viewId"] + "_depthMap.exr"
            if not os.path.isfile(inputExrPath): raise Exception("Input Exr not found", inputExrPath)
            os.path.isfile(inputExrPath)
            outputExrPath = outputDepthMapsFolder + "/" + view["viewId"] + "_depthMap.exr"

            if not intrinsicsScaled:
                try:
                    inputExr = cv.imread(inputExrPath, -1)
                except Exception as e:
                    raise Exception("here1")
                exrWidth = inputExr.shape[1]
                intrinsicsScaled = Utils.scaleIntrinsics(depthIntrinsics, exrWidth)

            if not ratio:
                ratio = self.calculateRatioExrvsTof(inputExrPath, intputTofPath, intrinsicsScaled)
                chunk.logger.info("calculated ratio:" + str(ratio))

            self.writeExr(intputTofPath, intrinsicsScaled, inputExrPath, outputExrPath, ratio)
            chunk.logger.info("wrote " + outputExrPath)

    # Compare the calculated depth and tof depth of centered pixel
    # Make sure that that center pixel has an high confidence both calculated and measured
    def calculateRatioExrvsTof(self, inputExrPath, inputTofPath, intrscs):
        try:
            depthsexr = cv.imread(inputExrPath, -1)
        except Exception as e:
            raise Exception("here2")
        depthstof = self.readInputDepth(inputTofPath)
        h, w = depthsexr.shape
        depthstof = cv.resize(depthstof, (w, h), interpolation=cv.INTER_NEAREST)

        y, x = (int(h / 2), int(w / 2))  # best pixel to compare is centered one (distance to pinhole == z, intrinsics has no impact)
        depthexr_distancepinhole = depthsexr[y][x]
        depthexr_z = Utils.pinholeDistanceToZ(depthexr_distancepinhole, x, y, intrscs) # it must be exr intrinsics, useless if it's center
        depthtof_z = depthstof[y][x] / 1000
        ratio = depthexr_z / depthtof_z
        return ratio

    # intrinsics sized to output exr
    def writeExr(self, inputTofPath, intrscs, inputExrPath, outputExrPath, ratio):
        depths = self.readInputDepth(inputTofPath)

        w, h, fx, fy, cx, cy = intrscs["w"], intrscs["h"], intrscs["fx"], intrscs["fy"], intrscs["cx"], intrscs["cy"]

        if depths.shape[1] != w:
            depths = cv.resize(depths, (w, h), interpolation=cv.INTER_NEAREST)
            # confidences = cv.resize(confidences, (w, h), interpolation=cv.INTER_NEAREST)

        outputExr = np.zeros((h, w), np.float32)

        if inputExrPath:
            try:
                inputExr = cv.imread(inputExrPath, -1)
            except Exception as e:
                raise Exception("here3")

        for y in range(0, h):
            for x in range(0, w):
                d = inputExr[y, x]
                if d < 0:
                    z3 = depths[y, x] / 1000 * ratio
                    d = Utils.zToPinholeDistance(z3, x, y, intrscs)

                outputExr[y, x] = d

        cv.imwrite(outputExrPath, outputExr)

    def readInputDepth(self, depthPath):
        if depthPath.endswith(".png") or depthPath.endswith(".jpg"):
            try:
                return cv.imread(depthPath, -1)
            except Exception as e:
                raise Exception("here4")
        else:
            raise Exception("only .png or .jpg format is supported")

class Utils:
    def scaleIntrinsics(intrinsics, w):
        ratio = w / intrinsics["w"]
        intrinsics2 = {}
        for k in intrinsics:
            intrinsics2[k] = int(intrinsics[k] * ratio)
        return intrinsics2

    def pinholeDistanceToZ(d, x, y, intrsc):
        w, h, fx, fy, cx, cy = intrsc["w"], intrsc["h"], intrsc["fx"], intrsc["fy"], intrsc["cx"], intrsc["cy"]
        pcx, pcy = x - cx, y - cy
        hypoxy = math.hypot(pcy, fx, pcx)
        return fx * d / hypoxy

    def zToPinholeDistance(z3, x, y, intrsc):
        # x3,y3,z3 : 3d point; x,y: 2d point
        fx, fy, cx, cy = intrsc["fx"], intrsc["fy"], intrsc["cx"], intrsc["cy"]
        pcx = x - cx
        pcy = y - cy
        x3 = pcx * z3 / fx
        y3 = pcy * z3 / fy
        return math.hypot(x3, y3, z3)