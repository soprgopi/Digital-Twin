import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# -------------------------------
# STEP 1: Define system parameters
# -------------------------------

C = 500              # Thermal capacity (J/K)
h = 50               # Heat transfer coefficient (W/m²K)
A = 1.5              # Area (m²)
T_coolant = 300      # Coolant temperature (K)

# -------------------------------
# STEP 2: Heat generation function (variable)
# -------------------------------

def Q_gen(t):
    return 1000 + 1500 * np.sin(0.05 * t)

# -------------------------------
# STEP 3: Differential equation
# -------------------------------

def model(T, t):
    Q_in = Q_gen(t)
    Q_cooling = h * A * (T - T_coolant)
    dTdt = (Q_in - Q_cooling) / C
    return dTdt

# -------------------------------
# STEP 4: Time setup
# -------------------------------

t = np.linspace(0, 200, 500)
T0 = 300  # Initial temperature

# Solve ODE
T_model = odeint(model, T0, t)
T_model = T_model.flatten()

# -------------------------------
# -------------------------------
# FAULT SCENARIO
# -------------------------------

h_fault = 20  # reduced cooling (fault)

def model_fault(T, t):
    Q_in = Q_gen(t)
    Q_cooling = h_fault * A * (T - T_coolant)
    return (Q_in - Q_cooling) / C

T_fault = odeint(model_fault, T0, t).flatten()

# measured = faulty system + noise
noise = np.random.normal(0, 1, len(T_fault))
T_measured = T_fault + noise



# -------------------------------plt.figure()
plt.plot(t, T_model, label="Normal System")
plt.plot(t, T_fault, label="Faulty System")
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.title("Effect of Cooling Failure")
plt.legend()
plt.grid()

error = T_measured - T_model
threshold = 3

fault_points = np.abs(error) > threshold

plt.figure()
plt.plot(t, error, label="Error")

plt.scatter(t[fault_points], error[fault_points], 
            color='red', label="Fault Detected", s=10)

plt.axhline(threshold, linestyle='--')
plt.axhline(-threshold, linestyle='--')

plt.xlabel("Time")
plt.ylabel("Error")
plt.title("Fault Detection with Highlighted Points")
plt.legend()
plt.grid()


# STEP 6: Plot model vs measured
# -------------------------------

plt.figure()
plt.plot(t, T_model, label="Model Prediction")
plt.plot(t, T_measured, '--', label="Measured Data")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.title("Digital Twin: Model vs Measured")
plt.legend()
plt.grid()
plt.show()

# -------------------------------
# STEP 7: Fault simulation
# -------------------------------

h_fault = 20  # reduced cooling

def model_fault(T, t):
    Q_in = Q_gen(t)
    Q_cooling = h_fault * A * (T - T_coolant)
    dTdt = (Q_in - Q_cooling) / C
    return dTdt

T_fault = odeint(model_fault, T0, t).flatten()

# -------------------------------
# STEP 8: Fault detection
# -------------------------------

error = T_measured - T_model

threshold = 5
fault_detected = np.abs(error) > threshold

# -------------------------------
# STEP 9: Plot fault detection
# -------------------------------

plt.figure()
plt.plot(t, error, label="Error")
plt.axhline(threshold, color='r', linestyle='--')
plt.axhline(-threshold, color='r', linestyle='--')
plt.xlabel("Time (s)")
plt.ylabel("Error (K)")
plt.title("Fault Detection")
plt.legend()
plt.grid()
plt.show()

# -------------------------------
# STEP 10: Compare normal vs fault
# -------------------------------

plt.figure()
plt.plot(t, T_model, label="Normal")
plt.plot(t, T_fault, label="Fault Condition")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.title("System Behavior Under Fault")
plt.legend()
plt.grid()

plt.savefig("digital_twin.png")
plt.savefig("fault_detection.png")
plt.show()