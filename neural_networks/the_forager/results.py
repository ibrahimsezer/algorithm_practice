import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# --- 1. MATHEMATICAL ENGINE (UTILS) ---
def get_relative_info(agent_pos, target_pos, agent_angle):
    """
    Calculates the target's position from the agent's perspective.
    Returns 3 values: Distance, Angle Difference, Target's Global Angle
    """
    dx = target_pos[0] - agent_pos[0]
    dy = target_pos[1] - agent_pos[1]

    # Distance (Pythagorean)
    distance = np.sqrt(dx**2 + dy**2)

    # Target's global angle in the world (Radians)
    target_angle_global = np.arctan2(dy, dx)

    # Difference relative to the agent's perspective
    angle_diff = target_angle_global - agent_angle

    # Normalize angle between -PI and +PI (-180 to +180 degrees)
    angle_diff = (angle_diff + np.pi) % (2 * np.pi) - np.pi

    return distance, angle_diff, target_angle_global


# --- 2. PLOT 1: PERCEPTION ANALYSIS (STATIC SNAPSHOT) ---
def draw_perception_analysis(ax):
    # Example Static State
    hunter_pos = np.array([100.0, 100.0])
    hunter_angle = np.radians(45)  # Looking at 45 degrees (North-East)
    target_pos = np.array([300.0, 250.0])

    # Perform Calculations
    dist, angle_diff, target_angle_global = get_relative_info(
        hunter_pos, target_pos, hunter_angle
    )

    # A. Points
    ax.scatter(*hunter_pos, c="blue", s=200, label="Hunter", zorder=5)
    ax.scatter(*target_pos, c="green", s=200, label="Food", zorder=5)

    # B. Gaze Direction Arrow (Blue)
    arrow_len = 80
    arrow_end_x = hunter_pos[0] + np.cos(hunter_angle) * arrow_len
    arrow_end_y = hunter_pos[1] + np.sin(hunter_angle) * arrow_len

    # Draw the arrow
    ax.annotate(
        "",
        xy=(arrow_end_x, arrow_end_y),
        xytext=hunter_pos,
        arrowprops=dict(arrowstyle="->", color="blue", lw=2.5),
    )
    ax.text(
        arrow_end_x,
        arrow_end_y,
        "  Gaze Direction",
        color="blue",
        fontsize=10,
        va="center",
    )

    # C. Distance Line (Gray Dashed)
    ax.plot(
        [hunter_pos[0], target_pos[0]], [hunter_pos[1], target_pos[1]], "k--", alpha=0.5
    )

    # Distance Text (Boxed)
    mid_point = (hunter_pos + target_pos) / 2
    bbox_props = dict(boxstyle="square,pad=0.3", fc="white", ec="black", alpha=0.8)
    ax.text(
        mid_point[0],
        mid_point[1],
        f"Distance: {dist:.1f}",
        ha="center",
        va="center",
        bbox=bbox_props,
        fontsize=9,
    )

    # D. Angle Arc (Red Arc)
    theta1 = np.degrees(hunter_angle)
    theta2 = np.degrees(target_angle_global)
    arc = patches.Arc(
        hunter_pos, 80, 80, angle=0, theta1=theta1, theta2=theta2, color="red", lw=2
    )
    ax.add_patch(arc)
    ax.text(
        hunter_pos[0] + 50,
        hunter_pos[1] + 10,
        f"Angle Diff:\n{np.degrees(angle_diff):.1f}°",
        color="red",
        fontsize=10,
    )

    # Settings
    ax.set_title("1. Perception Analysis (Input Data)")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 400)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")


# --- 3. PLOT 2: TRAJECTORY SIMULATION (DYNAMIC MOVEMENT) ---
def draw_trajectory_simulation(ax):
    # Initial State
    hunter_pos = np.array([0.0, 0.0])
    hunter_angle = 0.0
    hunter_speed = 5.0
    target_pos = np.array([200.0, 150.0])

    path_x = [hunter_pos[0]]
    path_y = [hunter_pos[1]]

    # Simulation Loop (60 Steps)
    for _ in range(60):
        # A. Perceive
        dist, angle_diff, _ = get_relative_info(hunter_pos, target_pos, hunter_angle)

        # B. Decide (Turn to Target)
        turn_force = angle_diff * 0.1  # Soft turn
        hunter_angle += turn_force

        # C. Move
        dx = np.cos(hunter_angle) * hunter_speed
        dy = np.sin(hunter_angle) * hunter_speed
        hunter_pos += np.array([dx, dy])

        path_x.append(hunter_pos[0])
        path_y.append(hunter_pos[1])

        if dist < 10:
            break

    # Drawing
    ax.plot(path_x, path_y, "b.-", label="Path Taken", zorder=1)
    ax.scatter(*target_pos, c="green", s=150, marker="*", label="Food", zorder=2)
    ax.scatter(
        path_x[-1], path_y[-1], c="blue", s=100, label="Hunter (Final)", zorder=2
    )

    # Final direction arrow
    ax.arrow(
        path_x[-1],
        path_y[-1],
        np.cos(hunter_angle) * 30,
        np.sin(hunter_angle) * 30,
        head_width=8,
        color="blue",
    )

    # Settings
    ax.set_title("2. Trajectory Simulation (Result)")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Create 2 plots side-by-side (1 row, 2 columns)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Draw the plots
    draw_perception_analysis(ax1)  # Left Side
    draw_trajectory_simulation(ax2)  # Right Side

    plt.tight_layout()
    plt.show()
