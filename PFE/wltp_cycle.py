import matplotlib.pyplot as plt
import numpy as np

def generate_wltp_cycle():
    time_urban = np.linspace(0, 400, 1000)
    time_suburban = np.linspace(400, 900, 1500)
    time_extra_urban = np.linspace(900, 1200, 1000)

    # Urban cycle (first 400 seconds)
    speed_urban = np.piecewise(time_urban, [
        time_urban < 100,
        (100 <= time_urban) & (time_urban < 200),
        (200 <= time_urban) & (time_urban < 300),
        time_urban >= 300
    ], [
        30, 10, 30, 10
    ])

    # Suburban cycle (next 500 seconds)
    speed_suburban = np.piecewise(time_suburban, [
        time_suburban < 500,
        (500 <= time_suburban) & (time_suburban < 700),
        (700 <= time_suburban) & (time_suburban < 900),
        time_suburban >= 900
    ], [
        50, 30, 50, 30
    ])

    # Extra-urban cycle (last 300 seconds)
    speed_extra_urban = np.piecewise(time_extra_urban, [
        time_extra_urban < 1050,
        (1050 <= time_extra_urban) & (time_extra_urban < 1150),
        time_extra_urban >= 1150
    ], [
        80, 60, 80
    ])

    # Combine the cycles
    time = np.concatenate((time_urban, time_suburban, time_extra_urban))
    speed = np.concatenate((speed_urban, speed_suburban, speed_extra_urban))

    return time, speed

def simulate_electric_truck_cycle():
    time, speed = generate_wltp_cycle()
    
    # Plot the speed-time profile
    plt.plot(time, speed)
    plt.title('Custom Drive Cycle - Electric Truck')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (km/h)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    simulate_electric_truck_cycle()
