# Better NeRF's

Here we discuss some of the improvements made to the original NeRF paper. We will see different methods, what they have done better, why thats better and more.

## 1. [Instant-NGP (NVIDIA)](https://github.com/NVlabs/instant-ngp)

- **Key strengths:**
  - **Blazing fast training** (seconds to minutes) using a multi-resolution hash encoding.
  - Great quality for **real-time applications** like SLAM and AR/VR.
- **Notable for:** Making NeRF practical on consumer GPUs.
- **Use this if:** You want _real-time performance_ with high quality and super fast training.

## 2. [Mip-NeRF (Google)](https://github.com/google/mipnerf)

- **Key strengths:**
  - Handles **unbounded scenes** better than original NeRF.
  - Uses mipmapping to reduce aliasing and improve training stability.
- **Notable for:** Capturing _large-scale_ outdoor and indoor scenes.
- **Use this if:** You're working on **360° scenes** or datasets with wide camera baselines.

## 3. [K-Planes (Waymo)](https://github.com/snap-research/K-Planes)

- **Key strengths:**
  - Designed for **scene generalization** across multiple scenes.
  - Fast training and rendering using **feature planes**.
- **Notable for:** Combining ideas from tensor decomposition and implicit representations.
- **Use this if:** You’re interested in **multi-scene training** or generalization tasks.

## 4. [Zip-NeRF (Google)](https://github.com/google/zipnerf)

- **Key strengths:**
  - Enables **super high-quality rendering** with fewer training views.
  - Efficient through ray and sample sharing.
- **Notable for:** Pushing the quality envelope, especially in sparse view settings.
- **Use this if:** You want **high fidelity** with limited input images.

## 5. [K-Planes (2023, NVIDIA)](https://github.com/nv-tlabs/k-planes)

- **Why it’s notable**:
  - Introduces **factorized feature grids** and **k-plane representation** for fast, memory-efficient rendering.
  - Extremely **scalable**, handling large, multi-scene datasets.
  - Can generalize across different scenes more effectively than traditional NeRF.
- **Use this if**: Large-scale scene representation, generalization, and memory efficiency.

## 6. [RegNeRF (Google)](https://github.com/google-research/google-research/tree/master/regnerf)

- **Key strengths:**
  - Tackles **view-dependent artifacts** and overfitting with regularization.
  - Maintains quality even when training with **very few input views**.
- **Notable for:** Cleaner reconstructions from **sparse or noisy data**.
- **Use this if:** You’re dealing with **low-shot** or **noisy real-world captures**.

| NeRF Variant      | Training Speed | Rendering Quality | Generalization | Sparse View Handling |
| ----------------- | -------------- | ----------------- | -------------- | -------------------- |
| **Original NeRF** | \*             | **\***            | \*             | \*                   |
| **Instant-NGP**   | **\***         | \*\*\*\*          | \*\*           | \*\*\*               |
| **Mip-NeRF 360**  | \*\*           | **\***            | \*\*           | \*\*\*               |
| **K-Planes**      | \*\*\*\*       | \*\*\*            | \*\*\*\*       | \*\*\*               |
| **Zip-NeRF**      | \*\*\*         | **\***            | \*\*\*         | \*\*\*\*             |
| **NeRFStudio**    | \*\*\*         | \*\*\*\*          | \*\*\*         | \*\*\*               |
| **RegNeRF**       | \*\*           | \*\*\*\*          | \*\*           | **\***               |

- **Fastest:** Instant-NGP
- **Best quality overall:** Zip-NeRF, Mip-NeRF 360
- **Best for sparse views:** RegNeRF
- **Best for multiple scenes/generalization:** K-Planes
- **Best all-in-one toolkit:** NeRFStudio
- **Baseline (still impressive):** Original NeRF has top quality, but is slow and inflexible.
