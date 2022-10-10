{
    "header": {
        "pipelineVersion": "2.2", 
        "releaseVersion": "2021.1.0", 
        "fileVersion": "1.1", 
        "template": true, 
        "nodesVersions": {
            "ExportAnimatedCamera": "2.0", 
            "FeatureMatching": "2.0", 
            "DistortionCalibration": "2.0", 
            "CameraInit": "8.0", 
            "ImageMatchingMultiSfM": "1.0", 
            "ImageMatching": "2.0", 
            "FeatureExtraction": "1.1", 
            "StructureFromMotion": "2.0"
        }
    }, 
    "graph": {
        "DistortionCalibration_1": {
            "inputs": {
                "input": "{CameraInit_2.output}"
            }, 
            "nodeType": "DistortionCalibration", 
            "uids": {
                "0": "8afea9d171904cdb6ba1c0b116cb60de3ccb6fb4"
            }, 
            "parallelization": {
                "blockSize": 0, 
                "split": 1, 
                "size": 0
            }, 
            "outputs": {
                "outSfMData": "{cache}/{nodeType}/{uid0}/sfmData.sfm"
            }, 
            "position": [
                1024, 
                393
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "ImageMatching_1": {
            "inputs": {
                "input": "{FeatureExtraction_1.input}", 
                "featuresFolders": [
                    "{FeatureExtraction_1.output}"
                ]
            }, 
            "nodeType": "ImageMatching", 
            "uids": {
                "0": "46fb9072ac753d60bec7dda9c8674b0568506ddf"
            }, 
            "parallelization": {
                "blockSize": 0, 
                "split": 1, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/imageMatches.txt"
            }, 
            "position": [
                400, 
                0
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "FeatureExtraction_1": {
            "inputs": {
                "input": "{CameraInit_1.output}"
            }, 
            "nodeType": "FeatureExtraction", 
            "uids": {
                "0": "a07fb8d05b63327d05461954c2fd2a00f201275b"
            }, 
            "parallelization": {
                "blockSize": 40, 
                "split": 0, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/"
            }, 
            "position": [
                200, 
                0
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "StructureFromMotion_1": {
            "inputs": {
                "describerTypes": "{FeatureMatching_1.describerTypes}", 
                "input": "{FeatureMatching_1.input}", 
                "featuresFolders": "{FeatureMatching_1.featuresFolders}", 
                "matchesFolders": [
                    "{FeatureMatching_1.output}"
                ]
            }, 
            "nodeType": "StructureFromMotion", 
            "uids": {
                "0": "5af4f4052aa22b0450708941b40928d46170f364"
            }, 
            "parallelization": {
                "blockSize": 0, 
                "split": 1, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/sfm.abc", 
                "extraInfoFolder": "{cache}/{nodeType}/{uid0}/", 
                "outputViewsAndPoses": "{cache}/{nodeType}/{uid0}/cameras.sfm"
            }, 
            "position": [
                800, 
                0
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "ExportAnimatedCamera_1": {
            "inputs": {
                "sfmDataFilter": "{StructureFromMotion_1.output}", 
                "input": "{StructureFromMotion_2.output}"
            }, 
            "nodeType": "ExportAnimatedCamera", 
            "uids": {
                "0": "c28dfbc702edbecf8bf6721224cf6b10799a6a5d"
            }, 
            "parallelization": {
                "blockSize": 0, 
                "split": 1, 
                "size": 1
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/", 
                "outputUndistorted": "{cache}/{nodeType}/{uid0}/undistort", 
                "outputCamera": "{cache}/{nodeType}/{uid0}/camera.abc"
            }, 
            "position": [
                1629, 
                212
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "CameraInit_1": {
            "inputs": {}, 
            "nodeType": "CameraInit", 
            "uids": {
                "0": "f9436e97e444fa71a05aa5cf7639b206df8ba282"
            }, 
            "parallelization": {
                "blockSize": 0, 
                "split": 1, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/cameraInit.sfm"
            }, 
            "position": [
                0, 
                0
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "ImageMatchingMultiSfM_1": {
            "inputs": {
                "nbNeighbors": 10, 
                "nbMatches": 5, 
                "input": "{FeatureExtraction_2.input}", 
                "inputB": "{StructureFromMotion_1.output}", 
                "featuresFolders": [
                    "{FeatureExtraction_2.output}"
                ]
            }, 
            "nodeType": "ImageMatchingMultiSfM", 
            "uids": {
                "0": "a789cef752e327c0f2ee58012ca4792e9ab6a70e"
            }, 
            "parallelization": {
                "blockSize": 0, 
                "split": 1, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/imageMatches.txt", 
                "outputCombinedSfM": "{cache}/{nodeType}/{uid0}/combineSfM.sfm"
            }, 
            "position": [
                1029, 
                212
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "CameraInit_2": {
            "inputs": {}, 
            "nodeType": "CameraInit", 
            "uids": {
                "0": "f9436e97e444fa71a05aa5cf7639b206df8ba282"
            }, 
            "parallelization": {
                "blockSize": 0, 
                "split": 1, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/cameraInit.sfm"
            }, 
            "position": [
                -2, 
                223
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "FeatureExtraction_2": {
            "inputs": {
                "input": "{CameraInit_2.output}"
            }, 
            "nodeType": "FeatureExtraction", 
            "uids": {
                "0": "a07fb8d05b63327d05461954c2fd2a00f201275b"
            }, 
            "parallelization": {
                "blockSize": 40, 
                "split": 0, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/"
            }, 
            "position": [
                198, 
                223
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "FeatureMatching_2": {
            "inputs": {
                "describerTypes": "{FeatureExtraction_2.describerTypes}", 
                "imagePairsList": "{ImageMatchingMultiSfM_1.output}", 
                "input": "{DistortionCalibration_1.outSfMData}", 
                "featuresFolders": "{ImageMatchingMultiSfM_1.featuresFolders}"
            }, 
            "nodeType": "FeatureMatching", 
            "uids": {
                "0": "142e98e3637aedcd3ebc1e19a03878690896a35b"
            }, 
            "parallelization": {
                "blockSize": 20, 
                "split": 0, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/"
            }, 
            "position": [
                1229, 
                212
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "FeatureMatching_1": {
            "inputs": {
                "describerTypes": "{FeatureExtraction_1.describerTypes}", 
                "imagePairsList": "{ImageMatching_1.output}", 
                "input": "{ImageMatching_1.input}", 
                "featuresFolders": "{ImageMatching_1.featuresFolders}"
            }, 
            "nodeType": "FeatureMatching", 
            "uids": {
                "0": "534c5224ba51c770ae3793cc085ae3aaa8c2c415"
            }, 
            "parallelization": {
                "blockSize": 20, 
                "split": 0, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/"
            }, 
            "position": [
                600, 
                0
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }, 
        "StructureFromMotion_2": {
            "inputs": {
                "minAngleForLandmark": 0.5, 
                "minNumberOfObservationsForTriangulation": 3, 
                "describerTypes": "{FeatureMatching_2.describerTypes}", 
                "input": "{FeatureMatching_2.input}", 
                "featuresFolders": "{FeatureMatching_2.featuresFolders}", 
                "matchesFolders": [
                    "{FeatureMatching_2.output}"
                ], 
                "minInputTrackLength": 5, 
                "minAngleForTriangulation": 1.0
            }, 
            "nodeType": "StructureFromMotion", 
            "uids": {
                "0": "eddc0ed596eb15943d6acd74a7d64753344b40dd"
            }, 
            "parallelization": {
                "blockSize": 0, 
                "split": 1, 
                "size": 0
            }, 
            "outputs": {
                "output": "{cache}/{nodeType}/{uid0}/sfm.abc", 
                "extraInfoFolder": "{cache}/{nodeType}/{uid0}/", 
                "outputViewsAndPoses": "{cache}/{nodeType}/{uid0}/cameras.sfm"
            }, 
            "position": [
                1429, 
                212
            ], 
            "internalFolder": "{cache}/{nodeType}/{uid0}/"
        }
    }
}