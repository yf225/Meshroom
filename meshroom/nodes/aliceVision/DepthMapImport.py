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
That script expect the depth image to be aside the rgb image, and have similar name (eg 0000234_image.jpg -> 0000234_depth16.bin or 0000234_image.depth_jpg)
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
            value="",
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
            value=".depth_jpg",
            uid=[0],
            advanced=True,
        ),
        # desc.StringParam(
        #     name='depthIntrinsics',
        #     label='Depth Image Intrinsics',
        #     description='The depth image intrinsics are expected to be similar than rgb image. If unset will use assume than rgbIntrinsics==depthIntrinsics',
        #     value='{"w": 576,"h": 768, "fx": 178.8240, "fy": 179.2912, "cx": 119.8185, "cy": 90.5689}',  # iPhone 13 Pro lidar intrinsics
        #     uid=[0],
        #     advanced=True,
        # ),
        desc.StringParam(
            name='rgbIntrinsics',
            label='RGB Image Intrinsics',
            description='',
            value=None,
            uid=[0],
            advanced=True,
        ),
        # desc.FloatParam(
        #     name='ratio',
        #     label='Ratio/Scale',
        #     description='Ratio between Sfm coordinate and imported depth. If 0, we will estimate it comparating center point of 1st image. Usually imported depth are in meters/millimeters',
        #     value=0.0,
        #     range=(0.0, 10.0, 0.1),  # I dont want it, but thats mandatory
        #     uid=[0],
        #     advanced=True,
        # ),
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
            depthIntrinsics = {"w": 576, "h": 768}  # iPhone 13 Pro lidar depth map values

            rgbIntrinsics = chunk.node.rgbIntrinsics.value
            rgbImageSuffix = chunk.node.rgbImageSuffix.value
            depthImageSuffix = chunk.node.depthImageSuffix.value
            # ratio = chunk.node.ratio.value

            self.importDepthMaps(chunk, inputCameras, inputDepthMapsFolder, outputDepthMapsFolder, depthIntrinsics, rgbIntrinsics, rgbImageSuffix, depthImageSuffix) # , ratio)

            chunk.logger.info("ended")
        except Exception as e:
            chunk.logger.error(e)
            raise RuntimeError()
        finally:
            chunk.logManager.end()

    def stopProcess(self, chunk):
        self._stopped = True


    def importDepthMaps(self, chunk, cameras, inputDepthMapsFolder, outputDepthMapsFolder, depthIntrinsics, rgbIntrinsics, rgbImageSuffix, depthImageSuffix):  #, ratio = 0.0):
        # chunk.logger.info(f"depthIntrinsics: {depthIntrinsics}")
        # chunk.logger.info(f"rgbIntrinsics._objects: {rgbIntrinsics._objects}")
        # import meshroom
        # for key in rgbIntrinsics._objects[0]._value._objects:
        #     obj = rgbIntrinsics._objects[0]._value._objects[key]
        #     if type(obj) == meshroom.core.attribute.Attribute:
        #         chunk.logger.info(f"{key}, {obj._value}")
        #     elif type(obj) == meshroom.core.attribute.GroupAttribute:
        #         chunk.logger.info(f"{key}, {obj._value._objects}")
        #     elif type(obj) == meshroom.core.attribute.ListAttribute:
        #         chunk.logger.info(f"{key}, {obj._value._objects}")
        # import pickle
        # with open('/fsx/users/willfeng/3d_recon/Meshroom/rgbIntrinsics.pickle', 'wb') as f:
        #     pickle.dump(rgbIntrinsics._objects[0]._value._objects, f, protocol=pickle.HIGHEST_PROTOCOL)

        f = open(cameras,)
        data = json.load(f)

        depthIntrinsics_scaled = None

        for view in data["views"]:
            if self._stopped: raise RuntimeError("User asked to stop")
            rgb_image_path = view["path"]
            inputTofPath = rgb_image_path.replace(rgbImageSuffix, depthImageSuffix)  # add type png, jpg or depth16
            if not os.path.isfile(inputTofPath): raise Exception("Depth file not found", inputTofPath, "check if the file exists or if the rgbImageSuffix and depthImageSuffix are properly set")
            inputExrPath = inputDepthMapsFolder + "/" + view["viewId"] + "_depthMap.exr"
            if not os.path.isfile(inputExrPath): raise Exception("Input Exr not found", inputExrPath)
            os.path.isfile(inputExrPath)
            outputExrPath = outputDepthMapsFolder + "/" + view["viewId"] + "_depthMap.exr"

            if not depthIntrinsics_scaled:
                inputExr = cv.imread(inputExrPath, -1)
                exrWidth = inputExr.shape[1]
                depthIntrinsics_scaled = Utils.scaleIntrinsics(depthIntrinsics, rgbIntrinsics)
                chunk.logger.info(f"depthIntrinsics_scaled: {depthIntrinsics_scaled}")

            # if not ratio:
            ratio = self.calculateRatioExrvsTof(inputExrPath, inputTofPath, depthIntrinsics_scaled)
            chunk.logger.info("calculated ratio for Exr vs. Tof:" + str(ratio))

            self.writeExr(inputTofPath, depthIntrinsics_scaled, inputExrPath, outputExrPath, ratio, chunk)
            chunk.logger.info("wrote " + outputExrPath)

    # Compare the calculated depth and tof depth of centered pixel
    # Make sure that that center pixel has an high confidence both calculated and measured
    def calculateRatioExrvsTof(self, inputExrPath, inputTofPath, intrscs):
        depthsexr = cv.imread(inputExrPath, -1)
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
    def writeExr(self, inputTofPath, intrscs, inputExrPath, outputExrPath, ratio, chunk):
        chunk.logger.info("here1")
        depths = self.readInputDepth(inputTofPath)
        chunk.logger.info("here2")

        # fx and fy are the focal lengths, cx, cy are the camera principal point.
        #   focalLength = (pxFocalLength / width) * sensorWidth
        w, h, fx, fy, cx, cy = intrscs["w"], intrscs["h"], intrscs["fx"], intrscs["fy"], intrscs["cx"], intrscs["cy"]

        chunk.logger.info("here3")
        if depths.shape[1] != w:
            depths = cv.resize(depths, (w, h), interpolation=cv.INTER_NEAREST)
            # confidences = cv.resize(confidences, (w, h), interpolation=cv.INTER_NEAREST)

        chunk.logger.info("here4")
        outputExr = np.zeros((h, w), np.float32)
        chunk.logger.info("here5")

        if inputExrPath:
            inputExr = cv.imread(inputExrPath, -1)

        chunk.logger.info("here6")

        for y in range(0, h):
            for x in range(0, w):
                d = inputExr[y, x]
                chunk.logger.info("here7")
                if d < 0:
                    z3 = depths[y, x] / 1000 * ratio
                    chunk.logger.info("here8")
                    d = Utils.zToPinholeDistance(z3, x, y, intrscs, chunk)
                    chunk.logger.info("here9")

                outputExr[y, x] = d
                chunk.logger.info("here10")

        chunk.logger.info("here11")
        cv.imwrite(outputExrPath, outputExr)
        chunk.logger.info("here12")

    def readInputDepth(self, depthPath):
        if depthPath.endswith(".depth_png") or depthPath.endswith(".depth_jpg"):
            return cv.imread(depthPath, -1)
        else:
            raise Exception("only .depth_png or .depth_jpg format is supported")

class Utils:
    def scaleIntrinsics(depthIntrinsics, rgbIntrinsics):
        ratio = rgbIntrinsics._objects[0]._value._objects["width"]._value / depthIntrinsics["w"]
        depthIntrinsics_scaled = {}
        depthIntrinsics_scaled["w"] = depthIntrinsics["w"]
        depthIntrinsics_scaled["h"] = depthIntrinsics["h"]
        depthIntrinsics_scaled["fx"] = rgbIntrinsics._objects[0]._value._objects["pxFocalLength"]._value / ratio
        depthIntrinsics_scaled["fy"] = rgbIntrinsics._objects[0]._value._objects["pxFocalLength"]._value / ratio
        depthIntrinsics_scaled["cx"] = rgbIntrinsics._objects[0]._value._objects["principalPoint"]._value._objects["x"]._value / ratio
        depthIntrinsics_scaled["cy"] = rgbIntrinsics._objects[0]._value._objects["principalPoint"]._value._objects["y"]._value / ratio
        return depthIntrinsics_scaled

    def pinholeDistanceToZ(d, x, y, intrsc):
        w, h, fx, fy, cx, cy = intrsc["w"], intrsc["h"], intrsc["fx"], intrsc["fy"], intrsc["cx"], intrsc["cy"]
        pcx, pcy = x - cx, y - cy
        hypoxy = math.hypot(pcy, fx, pcx)
        return fx * d / hypoxy

    def zToPinholeDistance(z3, x, y, intrsc, chunk):
        # x3,y3,z3 : 3d point; x,y: 2d point
        chunk.logger.info("here81")
        fx, fy, cx, cy = intrsc["fx"], intrsc["fy"], intrsc["cx"], intrsc["cy"]
        chunk.logger.info("here82")
        chunk.logger.info(f"x: {x}")
        chunk.logger.info(f"y: {y}")
        chunk.logger.info(f"cx: {cx}")
        chunk.logger.info(f"cy: {cy}")
        chunk.logger.info(f"z3: {z3}")
        chunk.logger.info(f"fx: {fx}")
        chunk.logger.info(f"fy: {fy}")
        pcx = x - cx
        chunk.logger.info("here83")
        pcy = y - cy
        chunk.logger.info("here84")
        x3 = pcx * z3 / fx
        chunk.logger.info("here85")
        y3 = pcy * z3 / fy
        chunk.logger.info("here86")
        chunk.logger.info(f"x3: {x3}")
        chunk.logger.info(f"y3: {y3}")
        chunk.logger.info(f"z3: {z3}")
        out = math.hypot(x3, y3, z3)
        chunk.logger.info("here87")
        return out