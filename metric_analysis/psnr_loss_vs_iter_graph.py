import matplotlib.pyplot as plt
import pandas as pd

# Read CSV file
df = pd.read_csv("../nerf/logs/hmb/psnr_loss.csv")  # replace with your actual path

# Plot PSNR vs Iteration
plt.figure(figsize=(8, 5))
plt.plot(df["iteration"], df["psnr"], marker='o', color='b')
plt.title("PSNR vs Iteration")
plt.xlabel("Iteration")
plt.ylabel("PSNR")
plt.grid(True)
plt.tight_layout()
plt.savefig("psnr_vs_iteration.png")
plt.show()

# Plot Loss vs Iteration
plt.figure(figsize=(8, 5))
plt.plot(df["iteration"], df["loss"], marker='o', color='r')
plt.title("Loss vs Iteration")
plt.xlabel("Iteration")
plt.ylabel("Loss")
plt.grid(True)
plt.tight_layout()
plt.savefig("loss_vs_iteration.png")
plt.show()


plt.figure(figsize=(8, 5))
plt.plot(df["iteration"], df["loss"], marker='o', color='r')
plt.yscale('log')  # <-- This is the key
plt.title("Loss vs Iteration (Log Scale)")
plt.xlabel("Iteration")
plt.ylabel("Loss (log scale)")
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.savefig("loss_vs_iteration_log.png")
plt.show()
