# project_pepper
A repository for project pepper

The circuitry for connecting the motors to the laptop USB are given in the following images:-

![Connection Pic 1](/pics/circuit_conn_001.jpeg?raw=true "Circuit Connection 1")
![Connection Pic 2](/pics/circuit_conn_002.jpeg?raw=true "Circuit Connection 2")

### Object Detection
We obtained pre-trained models for Object Detection. Due to lack of training data, we were unable to successfully implement transfer learning to our needs.
Listed below is the GitHub repository from where we utilized the pre-trained models from. The repo has a lot of Object Detection models.
After trying a lot of models, the one that had a decent accuracy, as well as run smoothly was Mobilenet SSD trained on the COCO dataset.

[Object Detection Repository](https://github.com/KleinYuan/tf-object-detection "Object Detection Pre-trained Models")
