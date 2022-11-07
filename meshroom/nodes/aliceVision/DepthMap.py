__version__ = "3.0"

from meshroom.core import desc


class DepthMap(desc.CommandLineNode):
    commandLine = 'aliceVision_depthMapEstimation {allParams}'
    gpu = desc.Level.INTENSIVE
    size = desc.DynamicNodeSize('input')
    parallelization = desc.Parallelization(blockSize=3)
    commandLineRange = '--rangeStart {rangeStart} --rangeSize {rangeBlockSize}'

    category = 'Dense Reconstruction'
    documentation = '''
For each camera that have been estimated by the Structure-From-Motion, it estimates the depth value per pixel.

Adjust the downscale factor to compute depth maps at a higher/lower resolution.
Use a downscale factor of one (full-resolution) only if the quality of the input images is really high (camera on a tripod with high-quality optics).

## Online
[https://alicevision.org/#photogrammetry/depth_maps_estimation](https://alicevision.org/#photogrammetry/depth_maps_estimation)
'''

    inputs = [
        desc.File(
            name='input',
            label='SfMData',
            description='SfMData file.',
            value='',
            uid=[0],
        ),
        desc.File(
            name='imagesFolder',
            label='Images Folder',
            description='Use images from a specific folder instead of those specify in the SfMData file.\nFilename should be the image uid.',
            value='',
            uid=[0],
        ),
       desc.ChoiceParam(
            name='downscale',
            label='Downscale',
            description='Image downscale factor.',
            value=2,
            values=[1, 2, 4, 8, 16],
            exclusive=True,
            uid=[0],
        ),
        desc.FloatParam(
            name='minViewAngle',
            label='Min View Angle',
            description='Minimum angle between two views.',
            value=2.0,
            range=(0.0, 10.0, 0.1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='maxViewAngle',
            label='Max View Angle',
            description='Maximum angle between two views.',
            value=70.0,
            range=(10.0, 120.0, 1.0),
            uid=[0],
            advanced=True,
        ),
        desc.GroupAttribute(
            name="tilling",
            label="Tilling Parameters",
            description='Tilling Parameters.',
            group=None,
            groupDesc=[
            desc.IntParam(
                name='tileWidth',
                label='Width',
                description='Maximum tile buffer width.',
                value=1024,
                range=(-1, 2000, 10),
                uid=[0],
            ),
            desc.IntParam(
                name='tileHeight',
                label='Height',
                description='Maximum tile buffer height.',
                value=1024,
                range=(-1, 2000, 10),
                uid=[0],
            ),
            desc.IntParam(
                name='tilePadding',
                label='Padding',
                description='Tile buffer padding for overlapping.',
                value=128,
                range=(0, 500, 1),
                uid=[0],
            ),
        ]),
        desc.BoolParam(
            name='chooseTCamsPerTile',
            label='Choose Neighbour Cameras Per Tile',
            description='Choose neighbour cameras per tile.',
            value=True,
            uid=[0],
            advanced=True,
        ),
        desc.IntParam(
            name='maxTCams',
            label='Max Nb Neighbour Cameras',
            description='Maximum number of neighbour cameras.',
            value=10,
            range=(1, 20, 1),
            uid=[0],
        ),
        desc.GroupAttribute(
            name="sgm",
            label="SGM Parameters",
            description='Semi Global Matching Parameters.',
            group=None,
            groupDesc=[
            desc.IntParam(
                name='sgmScale',
                label='Downscale factor',
                description='Downscale factor used to compute the similarity volume.',
                value=2,
                range=(-1, 10, 1),
                uid=[0],
            ),
            desc.IntParam(
                name='sgmStepXY',
                label='Step XY',
                description='Step used to compute the similarity volume on X and Y axis.',
                value=2,
                range=(-1, 10, 1),
                uid=[0],
            ),
            desc.IntParam(
                name='sgmStepZ',
                label='Step Z',
                description='Step used to compute the similarity volume on Z axis.',
                value=-1,
                range=(-1, 10, 1),
                uid=[0],
            ),
            desc.IntParam(
                name='sgmMaxSideXY',
                label='Max Side',
                description='Max side in pixels used to automatically decide for sgmScale/sgmStep if not defined.',
                value=700,
                range=(-1, 1000, 1),
                uid=[0],
            ),
            desc.IntParam(
                name='sgmMaxTCamsPerTile',
                label='Max Nb Neighbour Cameras Per Tile',
                description='Maximum number of neighbour cameras.',
                value=4,
                range=(1, 20, 1),
                uid=[0],
            ),
            desc.IntParam(
                name='sgmWSH',
                label='WSH',
                description='Half-size of the patch used to compute the similarity.',
                value=4,
                range=(1, 20, 1),
                uid=[0],
                advanced=True,
            ),
            desc.FloatParam(
                name='sgmGammaC',
                label='GammaC',
                description='GammaC Threshold.',
                value=5.5,
                range=(0.0, 30.0, 0.5),
                uid=[0],
                advanced=True,
            ),
            desc.FloatParam(
                name='sgmGammaP',
                label='GammaP',
                description='GammaP Threshold.',
                value=8.0,
                range=(0.0, 30.0, 0.5),
                uid=[0],
                advanced=True,
            ),
            desc.FloatParam(
                name='sgmP1',
                label='P1',
                description='P1 parameter.',
                value=10.0,
                range=(0.0, 255.0, 0.5),
                uid=[0],
                advanced=True,
            ),
            desc.FloatParam(
                name='sgmP2Weighting',
                label='P2 Weighting',
                description='P2 weighting parameter.',
                value=100.0,
                range=(-255.0, 255.0, 0.5),
                uid=[0],
                advanced=True,
            ),
            desc.IntParam(
                name='sgmMaxDepths',
                label='Max Depths',
                description='Max number of depths in the overall similarity volume.',
                value=3000,
                range=(1, 5000, 1),
                uid=[0],
                advanced=True,
            ),
            desc.IntParam(
                name='sgmMaxDepthsPerTc',
                label='Max Depths Per Camera Pairs',
                description='Max number of depths to sweep in the similarity volume per Rc/Tc cameras.',
                value=1500,
                range=(1, 5000, 1),
                uid=[0],
                advanced=True,
            ),
            desc.StringParam(
                name='sgmFilteringAxes',
                label='Filtering Axes',
                description="Define axes for the filtering of the similarity volume.",
                value='YX',
                uid=[0],
                advanced=True,
            ),
            desc.BoolParam(
                name='sgmUseSfmSeeds',
                label='Use SfM Landmarks',
                description='Use landmarks from SfM to define the ranges for the plane sweeping.',
                value=True,
                uid=[0],
                advanced=True,
            ),
            desc.BoolParam(
                name='sgmChooseDepthListPerTile',
                label='Choose Depth List Per Tile',
                description='SChoose depth list per tile.',
                value=True,
                uid=[0],
                advanced=True,
            ),
        ]),
        desc.GroupAttribute(
            name="refine",
            label="Refine Parameters",
            description='Refine Parameters.',
            group=None,
            groupDesc=[
            desc.IntParam(
                name='refineScale',
                label='Downscale factor',
                description='Downscale factor.',
                value=1,
                range=(-1, 10, 1),
                uid=[0],
            ),
            desc.IntParam(
                name='refineStepXY',
                label='Step XY',
                description='Step on X and Y axis.',
                value=1,
                range=(-1, 10, 1),
                uid=[0],
            ),
            desc.IntParam(
                name='refineNSamplesHalf',
                label='Number of Samples',
                description='Number of samples.',
                value=150,
                range=(1, 500, 10),
                uid=[0],
                advanced=True,
            ),
            desc.IntParam(
                name='refineNDepthsToRefine',
                label='Number of Depths',
                description='Number of depths.',
                value=31,
                range=(1, 100, 1),
                uid=[0],
                advanced=True,
            ),
            desc.IntParam(
                name='refineNiters',
                label='Number of Iterations',
                description='Number of iterations.',
                value=100,
                range=(1, 500, 10),
                uid=[0],
                advanced=True,
            ),
            desc.IntParam(
                name='refineMaxTCamsPerTile',
                label='Max Nb Neighbour Cameras Per Tile',
                description='Maximum number of neighbour cameras.',
                value=4,
                range=(1, 20, 1),
                uid=[0],
            ),
            desc.IntParam(
                name='refineWSH',
                label='WSH',
                description='Half-size of the patch used to compute the similarity.',
                value=3,
                range=(1, 20, 1),
                uid=[0],
                advanced=True,
            ),
            desc.FloatParam(
                name='refineSigma',
                label='Sigma',
                description='Sigma Threshold.',
                value=15.0,
                range=(0.0, 30.0, 0.5),
                uid=[0],
                advanced=True,
            ),
            desc.FloatParam(
                name='refineGammaC',
                label='GammaC',
                description='GammaC Threshold.',
                value=15.5,
                range=(0.0, 30.0, 0.5),
                uid=[0],
                advanced=True,
            ),
            desc.FloatParam(
                name='refineGammaP',
                label='GammaP',
                description='GammaP threshold.',
                value=8.0,
                range=(0.0, 30.0, 0.5),
                uid=[0],
                advanced=True,
            ),
            desc.BoolParam(
                name='refineDoRefineFuse',
                label='Refine and Fuse',
                description='Perform Refine/Fuse',
                value=True,
                uid=[0],
                advanced=True,
            ),
            desc.BoolParam(
                name='refineDoRefineOptimization',
                label='Post-Process Optimization',
                description='Perform Refine post-process optimization',
                value=True,
                uid=[0],
                advanced=True,
            ),
        ]),
        desc.BoolParam(
            name='exportIntermediateResults',
            label='Export Intermediate Results',
            description='Export intermediate results from the SGM and Refine steps.',
            value=False,
            uid=[],
            advanced=True,
        ),
        desc.IntParam(
            name='nbGPUs',
            label='Number of GPUs',
            description='Number of GPUs to use (0 means use all available GPUs).',
            value=0,
            range=(0, 5, 1),
            uid=[],
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
            label='Folder',
            description='Output folder for generated depth maps.',
            value=desc.Node.internalFolder,
            uid=[],
        ),
        # these attributes are only here to describe more accurately the output of the node
        # by specifying that it generates 2 sequences of images
        # (see in Viewer2D.qml how these attributes can be used)
        desc.File(
            name='depth',
            label='Depth Maps',
            description='Generated depth maps.',
            semantic='image',
            value=desc.Node.internalFolder + '<VIEW_ID>_depthMap.exr',
            uid=[],
            group='', # do not export on the command line
        ),
        desc.File(
            name='sim',
            label='Sim Maps',
            description='Generated sim maps.',
            semantic='image',
            value=desc.Node.internalFolder + '<VIEW_ID>_simMap.exr',
            uid=[],
            group='', # do not export on the command line
        ),
    ]
