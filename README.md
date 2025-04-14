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


```

Now you can use the config files present in [configs/](./configs/) and run the below command - 
