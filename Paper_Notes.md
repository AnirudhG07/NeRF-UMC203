# Notes of [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](https://arxiv.org/abs/2003.08934)

## Introduction Notes

The main function is to create a mapping from 5D coordinates `(x, y, z, θ, φ)` to `(R,G,B,σ)` where (x, y, z) are the 3D coordinates and (θ, φ) are the viewing direction. The output is the RGB color and the volume density σ at that point.

### Steps for Rendering an NeRF

- march camera rays through the scene to generate a sampled set of 3D points.
- use those points and their corresponding 2D viewing directions as input to the neural network to produce an output set of colors and densities.
- use classical volume rendering techniques to accumulate those colors and densities into a 2D image.

The process is naturally differentiable, allowing the use of `gradient descent` to `minimize error` between observed images and rendered views. This encourages the network to predict a coherent scene model by assigning accurate colors and high volume densities to true scene content locations.

### Main Technical Contributions

- An approach for representing continuous scenes with complex geometry and
  materials as 5D neural radiance fields, parameterized as basic MLP networks.
- A differentiable rendering procedure based on classical volume rendering tech-
  niques, which we use to optimize these representations from standard RGB
  images. This includes a hierarchical sampling strategy to allocate the MLP’s
  capacity towards space with visible scene content.

- A positional encoding to map each input 5D coordinate into a higher dimen-
  sional space, which enables us to successfully optimize neural radiance fields
  to represent high-frequency scene content.

### General Limitations and How NeRF Addresses Them

The basic implementation of optimizing a neural radiance field for complex scenes struggles with resolution and efficiency. These issues are addressed by using positional encoding for higher frequency functions and a hierarchical sampling procedure to reduce the number of required samples.

- **Limited spatial resolution**: NeRF can represent high-frequency details in the scene by using positional encoding to map each input 5D coordinate into a higher dimensional space.
- **Limited view-dependent effects**: NeRF can model view-dependent effects by conditioning the network on the viewing direction.

## Related Work Notes

- **Neural 3D Shape Representations**: Recent work has investigated the implicit representation of continuous 3D shapes as level sets by optimizing deep networks that map xyz coordinates to signed distance functions or occupancy fields. However, these models are limited by their requirement of access to ground truth 3D geometry, typically obtained from synthetic 3D shape datasets such as ShapeNet.

  - Subsequent work has relaxed this requirement of ground truth 3D shapes by formulating diﬀerentiable rendering functions that allow neural implicit shape representations to be optimized using only 2D images.

- `Niemeyer et al.` represent surfaces as 3D occupancy fields and use a numerical method to find the surface intersection for each ray, then calculate an
  exact derivative using implicit differentiation. Each ray intersection location is provided as the input to a neural 3D texture field that predicts a diﬀuse color for that point.
- `Sitzmann et al.` use a less direct neural 3D representation that simply outputs a feature vector and RGB color at each continuous 3D coordinate, and propose a differentiable rendering function consisting of a recurrent neural network that marches along each ray to decide where the surface is located.

- **View synthesis and image-based rendering**: Given a dense sampling of views, photorealistic novel views can be reconstructed by simple light field sam ple interpolation techniques.

  - One popular class of approaches uses mesh-based representations of scenes with either diffuse or view-dependent appearance.Differentiable rasterizers or pathtracers can directly optimize mesh representations to reproduce a set of input images using gradient descent.

    - However, gradient-based mesh optimization based on image reprojection is often difficult due to local minima or poor conditioning of the loss landscape. Additionally, this strategy requires a template mesh with fixed topology for initialization, which may not be available for unconstrained scenes.

  - Volumetric representations methods are used to address the task of high-quality photorealistic view synthesis from a set of input RGB images.
    - **Good Point:** Volumetric approaches are able to realistically represent complex shapes and materials, are well-suited for gradient-based optimization, and tend to produce less visually distracting artifacts than mesh-based methods. (See more details in paper about implementation)
    - **Issues:** While these volumetric techniques have achieved impressive results for novel view synthesis, their ability to scale to higher resolution imagery is fundamentally limited by poor time and space complexity due to their discrete sampling — rendering higher resolution images requires a finer sampling of 3D space.
    - **NeRF Approach:** NeRF circumvent this problem by instead encoding a continuous volume within the parameters just a fraction of the storage cost of those sampled volumetric representations of a deep fully-connected neural network, which not only produces significantly higher quality renderings than prior volumetric approaches, but also requires just a fraction of the storage cost of those sampled volumetric representations.

## Neural Radiance Field Scene Representation

- NeRF represents a scene as a continuous 5D function that maps 3D spatial locations `(x, y, z)` and viewing directions `(θ, φ)` to radiance `c = (r, g, b)` and volume density `σ`. We approximate this continuous 5D scene representation with an MLP network `FΘ : (x,d) →(c,σ)` and optimize its weights Θ to map from each input 5D coordinate to its corresponding volume density and directional emitted color.

- NeRF recommends the below -

  - **Multiview Consistency**: The network ensures multiview consistency by predicting the volume density (σ) solely based on the 3D location (x), while the RGB color (c) is predicted using both the location and the viewing direction. This separation enforces that the geometry (density) remains consistent across different views, while the appearance (color) can vary with the viewing angle.

  - **Network Architecture**: The MLP `(FΘ)` processes the 3D coordinates (x) through 8 fully-connected layers (256 channels, ReLU activations) to output σ and a 256-dimensional feature vector. This feature vector is then combined with the viewing direction and passed through an additional fully-connected layer (128 channels, ReLU activation) to produce the view-dependent RGB color. This design allows the network to efficiently model both geometry and appearance.
