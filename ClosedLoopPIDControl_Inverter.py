import numpy as np
import matplotlib.pyplot as plt
import control as ct
num_samples = 1000
mean = 0
std_dev = 0.05

# Generate four noise samples

noise_samples = np.random.normal(mean, std_dev, 4)

# Add noise to the parameters (which means uncertainties within power electronics converter)

a1 = -1.976 + noise_samples[0]
a2 = 0.978 + noise_samples[1]
b1 = 0.8907 + noise_samples[2]
b2 = -0.0932 + noise_samples[3]

# The inverter transfer function (The mathematical representation of power electronics converter)

numerator_inverter = [b1, b2]
denominator_inverter = [1, a1, a2]
Ts = 1/20000
inverter_discrete = ct.TransferFunction(numerator_inverter, denominator_inverter, dt=Ts)

# PID parameters

Kp = 1.0  # Proportional gain
Ki = 0.3  # Integral gain
Kd = 0  # Derivative gain

# Time array for simulation

t = np.arange(0, 0.05, Ts)  # Adjusted for the discrete time steps

# Define the PID controller

pid_continuous = ct.TransferFunction([Kd, Kp, Ki], [1, 0])

# Discretize the PID controller

pid_discrete = pid_continuous.sample(Ts, method='tustin')

# Form the closed-loop system

sys_cl = ct.feedback(pid_discrete * inverter_discrete, 1)

# Define the reference signal (Alternating current)

freq = 314.16  # Frequency in Hz
ref = 350*np.sin(2 * np.pi * freq * t)


# Simulate the system response to the reference signal

_, y = ct.forced_response(sys_cl, t, ref)

# Plot the results

plt.figure()
plt.step(t, ref, label='Reference')
plt.step(t, y, label='Output')
plt.legend()
plt.grid()
plt.title('Output Voltage with PID controller')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.show()
print(a1)
