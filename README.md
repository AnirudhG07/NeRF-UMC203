# NeRF - Neural Radiance Field, for UMC203 AIML Course Project

NeRF (Neural Radiance Fields) is a deep learning model that generates high-quality 3D scenes from 2D
images. It represents a scene as a continuous function, mapping 3D coordinates and viewing directions
to color and density values. NeRF is trained using a set of posed images and can synthesize novel
views with realistic lighting and details. It works by optimizing a volumetric rendering function using
a neural network, making it particularly useful for applications like 3D reconstruction, virtual reality,
and synthetic view generation.

## Resources and References

- [NeRF Website](https://www.matthewtancik.com/nerf)
- Paper: [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](https://arxiv.org/pdf/2003.08934)
- [NeRF: GitHub](https://github.com/bmild/nerf?tab=readme-ov-file)
- [Youtube Project Video](https://www.youtube.com/watch?v=JuH79E8rdKc)

- [NeRF Data](https://drive.google.com/drive/folders/1cK3UDIJqKAAm7zyrxRYVFJ0BRMgrwhh4) - Link taken from the NeRF Website.

## Environment Setup

Since the project uses python3.7 which is very outdated, we will use python3.10. Also for more convenience and faster implementation, please use [uv](https://docs.astral.sh/uv/getting-started/installation/) python package manager. Why use this? Cause it's very FAST!

### Setting up

1. Run the below commands to set python3 environment -

```bash
uv venv --python 3.10
uv init
```

2. Add the dependencies from the `requirements.txt` file using -

```bash
uv pip install -r requirements.txt
```

Note that NeRF code in our repo is for tensorflow version 2.* since we have fixed all the deprications of v1.* present in the original repository.

3. Now you can source the python `.venv` environment using the below command -

```bash
source .venv/bin/activate
```

## Our Dataset

We have created 3 datasets using our camera. These are all mainly LLFF Type datasets. These include -

- 1. Wifiroom Dataset
- 2. Humanities Project Dataset(HMB)
- 3. JNT Statue Dataset(JNTS)

Check out [Releases](https://github.com/AnirudhG07/NeRF-UMC203/releases) to see the datasets and a detailed account on how they made.

## Outputs Obtained from NeRF-Orig

We have run the below datasets on nerf to test and see the results of the outputs by ourselves. The outputs of these have been saved as `.zip` on [outputs_db](https://github.com/AnirudhG07/NeRF-UMC203/releases/tag/outputs_db) release. These include:

- Fern Example Dataset
- Lego Example Configuration
- Lego Paper Configuration
- Wifiroom Dataset
- HMB Dataset
- JNT one-side Dataset

## How to reproduce our results

We assume you have created the environment as above. Download the dataset from Releases or any online source. The folder structure should look like-

```
dataset_name/
    images/
        image1.png
        image2.png
        ...
    poses_bounds.npy
    database.db
    colmap_output.txt
```

Now you can use the config files present in [configs/](./configs/) and run the below command -

```bash
python nerf/run_nerf.py --config configs/dataset_name.txt
```

This will automatically run the dataset and create a `logs/` folder in the current directory which will contain the outputs of the dataset. This should take about 15-18 hours on GPU for 200K-250K iterations. The outputs will include a depth, rgb and rgb_spiral video.mp4 files.

### How to produce camera poses for custom dataset

You can use [COLMAP](https://colmap.github.io/) to produce the camera poses for your custom dataset. Simply run `colmap gui`, Goto Automatic Reconstruction and select the folder containing the images, and run with defaults. You can select `Video Frames` if you extracted frames from a video using `ffmpeg`.

## PSNR Metric analysis

The `run_nerf.py` contains a script which will provide the value of `psnr` and `loss` calculated at each iteration by the model. We save this in a `psnr_loss.csv` file, which stores the same every 1000 iterations. You can then run the below to obtain the graphical results.

```bash
python3 metric_analysis.py /path/to/psnr_loss.csv
```

The graphs include `psnr vs iterations`, `loss vs iterations` and `log loss vs iterations` graph. Since NeRF algorithm converges, after 200K iterations you will see a band of convergence in the graphs, in all 3 graphs.

## Comparing performance with change in positional encoding Parameters(L)

NeRF uses `L(γ(x), γ(d)) = (10, 4)` by default, which can be change by adding additional parameters to `(20,6)` as -

```bash
python3 nerf/run_nerf.py --config configs/dataset_name.txt --multires 20 --multires_views 6
```

To compare the performance of the new video, you can run a comparative analysis using the below command. You will have to go and give 3 video files inside the python file, which are the 2 new NeRF video generated you want to compare and a ground truth video.

```bash
python3 metric_analysis/psnr_gt_nerfvids.py
```

This code will generate frames for the 2 videos and groundtruth again, find PSNR values for 2 videos and plot a graph comparing all 3 metrics. Note that you might have to change `fps` of the images so that the shape matches. For HMB dataset, we have chosen first 90 images at `3fps`.

## Running Gaussian Splatting

We have also run the Gaussian Splatting algorithm on the datasets. Refer [gaussian_splatting](https://github.com/graphdeco-inria/gaussian-splatting) for installation instructions. You can also use `gaussian_splatting.sh` file to see installation instruction using `uv` package manager.

We have run the Gaussian Splatting on HMB, JNTS and Wifiroom datasets. The outputs can be found in the [output_db](https://github.com/AnirudhG07/NeRF-UMC203/releases/tag/outputs_db) releases.

## Running nerfacto

Nerfacto is a Nerfstudio model meant for faster and better NeRF implementation on you datasets. Check of [NeRFStudio](https://docs.nerf.studio/) for instructions on running. We have run Nerfacto for Wifiroom and Fern Datasets, again whose outputs are present in the [output_db](https://github.com/AnirudhG07/NeRF-UMC203/releases/tag/outputs_db) Release.

## Conclusion

We have successfully implemented the NeRF algorithm and run it on our datasets. We have also run Gaussian Splatting and Nerfacto on the datasets. The results are satisfactory and we have also compared the performance of the models using PSNR metric. The results are promising and we can see that the models are able to generate high quality 3D scenes from 2D images.

## Project Members

- Anirudh Gupta
- Saksham Agrawal
- Shivey Ravi Guttal
- Aditya Arsh
