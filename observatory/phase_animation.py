import json
import matplotlib.pyplot as plt
import imageio
from pathlib import Path

def animate(timeline="observatory/experiment_timeline.json"):

    events = json.load(open(timeline))

    frames = []
    frame_dir = Path("reports/phase_frames")
    frame_dir.mkdir(parents=True, exist_ok=True)

    for e in events:

        plt.figure()

        plt.scatter(
            e["artifact_pressure"],
            e["governance_capacity"]
        )

        plt.title(f"Step {e['step']}")
        plt.xlabel("Artifact Pressure")
        plt.ylabel("Governance Capacity")

        frame = frame_dir / f"frame_{e['step']:04}.png"

        plt.savefig(frame)
        plt.close()

        frames.append(frame)

    images = [imageio.imread(f) for f in frames]

    Path("reports").mkdir(exist_ok=True)
    imageio.mimsave("reports/phase_animation.gif", images, fps=10)

    print("Animation written: reports/phase_animation.gif")


if __name__ == "__main__":
    animate()
