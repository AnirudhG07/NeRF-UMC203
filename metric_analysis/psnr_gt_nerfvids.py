import os
import subprocess

import cv2
import matplotlib.pyplot as plt
import numpy as np

# Paths to your videos
GROUNDTRUTH = "../../data/nerf_hmb/1_slowmo.mp4"
VIDEO_A = "../nerf/logs/hmb_l20/hmb_spiral_200000_rgb.mp4"
VIDEO_B = "../nerf/logs/hmb_orig/hmb_spiral_200000_rgb.mp4"

# Output folders
os.makedirs("frames/gt", exist_ok=True)
os.makedirs("frames/a", exist_ok=True)
os.makedirs("frames/b", exist_ok=True)

# Function to extract first 90 frames 
def extract_frames(video_path, output_dir, fps=3):
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"fps={fps}",
        "-vframes", "90",
        f"{output_dir}/frame_%04d.png",
        "-y"
    ]
    subprocess.run(cmd, check=True)

print("Extracting frames...")
extract_frames(GROUNDTRUTH, "frames/gt", 3)
extract_frames(VIDEO_A, "frames/a", 27)
extract_frames(VIDEO_B, "frames/b", 27)

# PSNR Calculation
def psnr(img1, img2):
    mse = np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)
    if mse == 0:
        return 100.0
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))


def compute_psnr_series(dir1, dir2):
    files1 = sorted(os.listdir(dir1))
    files2 = sorted(os.listdir(dir2))
    psnr_vals = []
    for f1, f2 in zip(files1, files2):
        img1 = cv2.imread(os.path.join(dir1, f1))
        img2 = cv2.imread(os.path.join(dir2, f2))
        
        # Resize the larger image to match the smaller one
        if img1.shape != img2.shape:
            h, w = img2.shape[:2]
            img1 = cv2.resize(img1, (w, h), interpolation=cv2.INTER_AREA)
        
        psnr_vals.append(psnr(img1, img2))
    return psnr_vals


print("Computing PSNR values...")
psnr_gt_a = compute_psnr_series("frames/gt", "frames/a")
psnr_gt_b = compute_psnr_series("frames/gt", "frames/b")
psnr_a_b = [(psnr_gt_a[i] - psnr_gt_b[i]) for i in range(len(psnr_gt_a))] 

# Averages
avg_gt_a = np.mean(psnr_gt_a)
avg_gt_b = np.mean(psnr_gt_b)
avg_a_b = np.mean(psnr_a_b)

print(f"Average PSNR (Groundtruth vs Video_206): {avg_gt_a:.2f} dB")
print(f"Average PSNR (Groundtruth vs Video_104): {avg_gt_b:.2f} dB")
print(f"Average PSNR (Video_206 vs Video_104): {avg_a_b:.2f} dB")

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(psnr_gt_a, label="GT vs Video_206")
plt.plot(psnr_gt_b, label="GT vs Video_104")
plt.plot(psnr_a_b, label="Video_206 vs Video_104")
plt.xlabel("Frame Index")
plt.ylabel("PSNR (dB)")
plt.title("Frame-wise PSNR Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("psnr_diff_comparison.png")
plt.show()
