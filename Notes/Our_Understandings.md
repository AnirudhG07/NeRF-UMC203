# Our Understanding of NeRF's

These notes includes a detailed explanation of how nerf's work, whatever we understood and mainly focuses no the implementation details of NeRF.

## Motivation

- Encoding 3D objects and scenes within the weights of a feed-forward neural network is a memory-efficient, implicit representation of 3D data that is both accurate and high-resolution.

- However, the approaches we have seen so far are not quite capable of capturing realistic and complex scenes with sufficient fidelity. Rather, discrete representations (e.g., triangle meshes or voxel grids) produce a more accurate representation, assuming a sufficient allocation of memory.

- NeRFs, which use a feed-forward neural network to model a continuous representation of scenes and objects. The representation used by NeRFs, called a radiance field, is a bit different from prior proposals.

- In particular, NeRFs map a five-dimensional coordinate (i.e., spatial location and viewing direction) to a volume density and view-dependent RGB color. By accumulating this density and appearance information across different viewpoints and locations, we can render photorealist, novel views of a scene.

## Representations of 3D objects: Info, Adv. and Disadv.

3D objects are usually stored as `point clouds`, `mesh` or `voxels`.

- **Point Clouds**

  - Group of points of form `[x,y,z]`
  - Advantage: Easy to store and manipulate. Match data's from sensors, etc.
  - Disadvantage: Do not provide `watertight` surfaces (1 closed surface).

- **Mesh**

  - Group of vertices, edges and faces. Basically closed surfaces made of polygons.
  - Advantage: Provide `watertight` surfaces.

- **Voxels**

  - 3D Pixels, with decision if it is filled or not.
  - Advantage: Easy to store. Can be used for 3D convolutional networks.
  - Disadvantage: Very High memory usage.

### Storing 3D objects

Directly Storing 3D shapes as the above 3 requires lot of memory. So `SDF ( Signed Distance Function)` is used to store 3D shapes. Given a spatial `[x, y, z]` point as input, SDFs will output the distance from that point to the nearest surface of the underlying object being represented. The sign of the SDF’s output indicates whether that spatial point is inside (negative) or outside (positive) of the object’s surface.

```
SDF(x) = {
    d(x) if x is outside the object
    -d(x) if x is inside the object
}

where `d(x)` is the distance from point `x` to the nearest surface of the underlying object.
```

If the value is 0, then the given point is at the boundary of the object. Thus this is a better way since we only need a function to represent the shape compactly and evaluate spatial queries efficiently, and store it.

# Images and Colmap

From a dataset(or camera), we have `N` RGB images of our view. These are the images obtained. Now these are passed into `COLMAP` which does the followinf process to give us our usable dataset:

COLMAP is a Structure-from-Motion (SfM) and Multi-View Stereo (MVS) pipeline. For NeRF, only the SfM stage is typically used. It processes a set of images to estimate:

## COLAMP

- Camera intrinsics (focal length, principal point)
- Camera extrinsics (position and orientation)
- A sparse 3D point cloud

### How COLMAP Works on Images

- **Feature Detection and Matching**

  - COLMAP detects features in each image (e.g., using SIFT), then matches them across image pairs to find correspondences. These matches are stored in the `database.db` file.

- **Sparse Reconstruction**

  - From matched features, COLMAP performs:

    - Intrinsic calibration (from EXIF or self-estimated)
    - Pose estimation for each image (extrinsics)
    - Triangulation of 3D points from 2D correspondences

  - This results in camera poses and a 3D point cloud, saved in binary or text formats.

## Important Output Files

- `cameras.bin`

  - Contains intrinsic parameters like `Focal Length`, `Principal Point`, and `Image Size`. These are used to compute ray directions in camera space.

- `images.bin`
  - Each line corresponds to an image and stores:
    - Quaternion rotation: `(qw, qx, qy, qz)`
    - Translation vector: `(tx, ty, tz)`
    - Image filename
  - This defines the camera’s position and orientation in world space.

* `points3D.txt`
  - Stores 3D coordinates `(X, Y, Z)` for each point in the reconstructed sparse point cloud. Also includes optional RGB color and reprojection error.

## From COLMAP Outputs to NeRF Inputs

- **3D Positions (x, y, z)**

  - Directly read from `points3D.txt`, but not directly used in training — mostly for visualization or bounding box calculation.

- **Camera Poses**
  - Derived from `images.txt`. Rotation quaternions are converted to rotation matrices, and translation vectors give the camera center. Combined, they define the full pose used to transform rays into world space.

* **Ray Directions**

  - For each image pixel, a ray is created:

    - Start from camera origin (`t`)
    - Project through the pixel using intrinsics (`cameras.txt`)
    - Rotate into world coordinates using `R`
    - Normalize to get unit view direction `d = (dx, dy, dz)`

  - These ray directions are input to NeRF's neural network (after positional encoding).

## Theta and Phi

COLMAP does not store `θ` (azimuth) and `φ` (elevation) directly. If needed, they can be computed from the direction vector `d` as:

```
θ = atan2(dy, dx)
φ = arccos(dz / ||d||)
```

# Neural Network and Details

1. The input to the NeRF is 3D coordinates which undergo positional Encoding (γ(x)) to capture fine details. This encoded information flows through 8 hidden layers with ReLU activations at the end and 256 channels per layer.

> More into Positional Encoding later below.

2. The output is volume density `σ` and 256-dimensional feature vector. This feature vector is concatenated with camera ray's viewing direction and passed to 1 full connected layer (with ReLU activation(or sigmoid) and 128 channels). The output is RGB colors obtained.

## Advantages of View-dependent output

The color is simply an RGB value. However, this value is view-dependent, meaning that the color output might change given a different viewing direction as input! Such a property allows NeRFs to capture reflections and other view-dependent appearance effects. In contrast, volume density is only dependent upon spatial location and captures opacity (i.e., how much light accumulates as it passes through that position), hence not view-dependent.

# Position Encoding

- This is basically using input 3D coordinates and converting to higher dimensional space. This is to make a high-frequency function to capture the variation in color and geometry(because mapping the network to a higher dimensional space using high frequency before passing them to the model network enavles better fitting of data that contains high frequenct variations).

- The NeRF uses the `sin, cos` encoding, which is a `2L` dimensional input from `1` i.e. `R -> R^(2L)` dimension, for each of `x,y,z` separately. NeRF uses `L = 10` so we have a `60` dimension input vector as input to the Neural Network.

Thus positional encoding help in increasing the quality of the output and also helps in reducing the number of parameters in the model. The positional encoding is done using the following formula:

```
γ(x) = [sin(2^0 * π * x), cos(2^0 * π * x), sin(2^1 * π * x), cos(2^1 * π * x), ..., sin(2^(L-1) * π * x), cos(2^(L-1) * π * x)]
```

Where `x` is the input coordinate and `L` is the number of frequency bands.

# Getting the RGB colors.

The RGB color of each pixel is obtained at the last layer in the MLP. It uses inputs such as `σ` (volume density) and `d` (viewing direction). The output is a 3D vector of RGB values. The MLP is trained to minimize the difference between the predicted RGB values and the ground truth RGB values from the images, using the loss (see paper).

## Method to get the color

- From the ray, `r(t) = o + t*d`, and near/far bounds, we have to solve an integral `C(r)` which contained terms like `T(t)`, `σ(r(t))`, `c(r(t))`.

- `T(t)` is transmittance. The farther you move along the ray, the higher the probability that the ray is absorbed within the scene. More the particles in a position, more it is absorbed. Consequently, the transmittance is determined by the negative exponent of the cumulative volumetric density integrated from the near plane to the point t where the transmittance is being calculated.

- `σ(r(t))` (volume density at `r(t)`) and can be interpreted as the probability that the point contains material capable of emitting or reflecting light.
- `c(r(t))` is the color at `r(t)` and is a function of the viewing direction.

# Volume Rendering

Rays at each pixel site project into the 3D space at a given viewing direction perpendicular to the image/camera plane and are used to represent the volume or occupancy of the space along the ray. The volume density of the pixel is determined by taking the integral of volumes along the ray; this process is known as `volume rendering`.

For each ray, to obtain the color `c = (r, g, b)`, we have `r(t) = o + t*d` with near and far bounds and solving integeral `C(r)`. Rendering a view from our continuous neural radiance field requires estimating the integral `C(r)` for a camera rat traced through each pixel. Special methods are used to solve this integral here, which is a sampling approach to partition the `[tn, tf]` into `N` evenly spaced bins and drawing a sample `ti`.

Although discrete samples are used to estimate integral, statified sampling enables the `NeRF` to represent continuous scene representation because MLP evaluates at continuous positions over course of optimization.

## Heirarchical Volume Sampling Optimization

- When a batch of rays are sent, querying each of `N` evenly spaced points along each camera ray is inefficient, because free space and occluded regions are still repeatedly samples.

- From a camera position.

# References

- [Understanding-nerfs Blog](https://cameronrwolfe.substack.com/p/understanding-nerfs)
- [viso.ai](https://viso.ai/deep-learning/neural-radiance-fields/)
- [NeRF: A Review and Some Recent Developments](https://arxiv.org/pdf/2305.00375)
- [medium.com/A beginner's 12 Step Guide to Understanding-nerfs](https://medium.com/data-science/a-12-step-visual-guide-to-understanding-nerf-representing-scenes-as-neural-radiance-fields-24a36aef909a)
- [Volume Rendering Math](https://arxiv.org/pdf/2209.02417)
