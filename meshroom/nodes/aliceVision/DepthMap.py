__version__ = "2.0"

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
        desc.IntParam(
            name='sgmScale',
            label='SGM: Downscale factor',
            description='Semi Global Matching: Downscale factor used to compute the similarity volume.',
            value=-1,
            range=(-1, 10, 1),
            uid=[0],
        ),
        desc.IntParam(
            name='sgmStepXY',
            label='SGM: Step XY',
            description='Semi Global Matching: Step used to compute the similarity volume on X and Y axis.',
            value=-1,
            range=(-1, 10, 1),
            uid=[0],
        ),
        desc.IntParam(
            name='sgmStepZ',
            label='SGM: Step Z',
            description='Semi Global Matching: Step used to compute the similarity volume on Z axis.',
            value=-1,
            range=(-1, 10, 1),
            uid=[0],
        ),
        desc.IntParam(
            name='sgmMaxSideXY',
            label='SGM: Max Side',
            description='Semi Global Matching: Max side in pixels used to automatically decide for sgmScale/sgmStep if not defined.',
            value=700,
            range=(-1, 1000, 1),
            uid=[0],
        ),
        desc.IntParam(
            name='sgmMaxTCams',
            label='SGM: Nb Neighbour Cameras',
            description='Semi Global Matching: Number of neighbour cameras.',
            value=10,
            range=(1, 100, 1),
            uid=[0],
        ),
        desc.IntParam(
            name='sgmWSH',
            label='SGM: WSH',
            description='Semi Global Matching: Half-size of the patch used to compute the similarity.',
            value=4,
            range=(1, 20, 1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='sgmGammaC',
            label='SGM: GammaC',
            description='Semi Global Matching: GammaC Threshold.',
            value=5.5,
            range=(0.0, 30.0, 0.5),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='sgmGammaP',
            label='SGM: GammaP',
            description='Semi Global Matching: GammaP Threshold.',
            value=8.0,
            range=(0.0, 30.0, 0.5),
            uid=[0],
            advanced=True,
        ),

        desc.FloatParam(
            name='sgmP1',
            label='SGM: P1',
            description='Semi Global Matching: P1.',
            value=10.0,
            range=(0.0, 255.0, 0.5),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='sgmP2',
            label='SGM: P2',
            description='Semi Global Matching: P2 weight.',
            value=100.0,
            range=(-255.0, 255.0, 0.5),
            uid=[0],
            advanced=True,
        ),
        desc.IntParam(
            name='sgmMaxDepths',
            label='SGM: Max Depths',
            description='Semi Global Matching: Max number of depths in the overall similarity volume.',
            value=3000,
            range=(1, 5000, 1),
            uid=[0],
            advanced=True,
        ),
        desc.IntParam(
            name='sgmMaxDepthsPerTc',
            label='SGM: Max Depths Per Camera Pairs',
            description='Semi Global Matching: Max number of depths to sweep in the similarity volume per Rc/Tc cameras.',
            value=1500,
            range=(1, 5000, 1),
            uid=[0],
            advanced=True,
        ),
        desc.BoolParam(
            name='sgmUseSfmSeeds',
            label='SGM: Use SfM Landmarks',
            description='Semi Global Matching: Use landmarks from SfM to define the ranges for the plane sweeping.',
            value=True,
            uid=[0],
            advanced=True,
        ),
        desc.StringParam(
            name='sgmFilteringAxes',
            label='SGM: Filtering Axes',
            description="Semi Global Matching: Define axes for the filtering of the similarity volume.",
            value='YX',
            uid=[0],
            advanced=True,
        ),
        desc.IntParam( 
            name='refineMaxTCams', 
            label='Refine: Nb Neighbour Cameras', 
            description='Refine: Number of neighbour cameras.', 
            value=6, 
            range=(1, 20, 1), 
            uid=[0], 
        ), 
        desc.IntParam(
            name='refineNSamplesHalf',
            label='Refine: Number of Samples',
            description='Refine: Number of samples.',
            value=150,
            range=(1, 500, 10),
            uid=[0],
            advanced=True,
        ),
        desc.IntParam(
            name='refineNDepthsToRefine',
            label='Refine: Number of Depths',
            description='Refine: Number of depths.',
            value=31,
            range=(1, 100, 1),
            uid=[0],
            advanced=True,
        ),
        desc.IntParam(
            name='refineNiters',
            label='Refine: Number of Iterations',
            description='Refine:: Number of iterations.',
            value=100,
            range=(1, 500, 10),
            uid=[0],
            advanced=True,
        ),
        desc.IntParam(
            name='refineWSH',
            label='Refine: WSH',
            description='Refine: Half-size of the patch used to compute the similarity.',
            value=3,
            range=(1, 20, 1),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='refineSigma',
            label='Refine: Sigma',
            description='Refine: Sigma Threshold.',
            value=15.0,
            range=(0.0, 30.0, 0.5),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='refineGammaC',
            label='Refine: GammaC',
            description='Refine: GammaC Threshold.',
            value=15.5,
            range=(0.0, 30.0, 0.5),
            uid=[0],
            advanced=True,
        ),
        desc.FloatParam(
            name='refineGammaP',
            label='Refine: GammaP',
            description='Refine: GammaP threshold.',
            value=8.0,
            range=(0.0, 30.0, 0.5),
            uid=[0],
            advanced=True,
        ),
        desc.BoolParam(
            name='refineUseTcOrRcPixSize',
            label='Refine: Tc or Rc pixel size',
            description='Refine: Use minimum pixel size of neighbour cameras (Tc) or current camera pixel size (Rc)',
            value=False,
            uid=[0],
            advanced=True,
        ),
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
            label='Output',
            description='Output folder for generated depth maps.',
            value=desc.Node.internalFolder,
            uid=[],
        ),
    ]
