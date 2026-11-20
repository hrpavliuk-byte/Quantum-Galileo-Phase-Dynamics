import os
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Fundamental Physical Constants (CODATA 2018 / 2022)
# -----------------------------------------------------------------------------
G = 6.67430e-11           # m^3 / (kg * s^2)
hbar = 1.054571817e-34     # J * s
c = 299792458.0            # m / s
amu = 1.66053906660e-27    # kg
g_acc = 9.80665            # m / s^2 (standard Earth surface gravity)

# Target: Rubidium-87 atom
m_Rb = 86.9091805 * amu   # 1.4432e-25 kg

# Master-functional localization radius in Unified Phase Dynamics (UPD)
r_loc = 2.05e-13           # m

# Target time in Science Advances experiment
T_exp = 1.22e-3            # s (1.22 ms)
phi_exp = 80.0             # rad

# -----------------------------------------------------------------------------
# Plotting Configuration (Academic Quality, 300 DPI)
# -----------------------------------------------------------------------------
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8.5,
    'figure.titlesize': 13,
    'lines.linewidth': 1.8,
    'axes.grid': True,
    'grid.alpha': 0.35,
    'grid.linestyle': '--'
})

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# -----------------------------------------------------------------------------
# Panel A: Gravitational Cubic Phase Shift vs Separation Time T
# -----------------------------------------------------------------------------
ax1 = axes[0, 0]
T_arr = np.linspace(0.1e-3, 3.0e-3, 500) # 0.1 to 3.0 ms
# Theoretical cubic phase in UPD: Delta Phi = (m * g^2 * T^3) / (3 * hbar)
phi_arr = (m_Rb * (g_acc**2) * (T_arr**3)) / (3.0 * hbar)

ax1.plot(T_arr * 1e3, phi_arr, color='#1e3a8a', label=r'UPD Prediction: $\Delta\Phi = \frac{m g^2 T^3}{3\hbar}$')
ax1.scatter([T_exp * 1e3], [phi_exp], color='#dc2626', s=70, zorder=5, 
            label=rf'Experiment (Folman, Penrose et al.): $\approx {phi_exp:.0f}$ rad at $1.22$ ms')
ax1.axvline(x=T_exp * 1e3, color='#dc2626', linestyle=':', alpha=0.6)
ax1.axhline(y=phi_exp, color='#dc2626', linestyle=':', alpha=0.6)

ax1.set_xlabel('Interferometer Evolution Time $T$ (ms)')
ax1.set_ylabel(r'Accumulated Phase Shift $\Delta\Phi$ (radians)')
ax1.set_title('(A) Gravitational Cubic Phase Shift of Split Atomic Wave Packet', weight='bold')
ax1.legend(loc='upper left', framealpha=0.9)
ax1.set_xlim(0.1, 3.0)
ax1.set_ylim(0, 1200)

# -----------------------------------------------------------------------------
# Panel B: Spatial Wave Packet Trajectories in Laboratory Frame
# -----------------------------------------------------------------------------
ax2 = axes[0, 1]
t_traj = np.linspace(0, 2.5e-3, 500)
z_held = np.zeros_like(t_traj)
z_fall = -0.5 * g_acc * (t_traj**2) * 1e6 # in micrometers

ax2.plot(t_traj * 1e3, z_held, color='#047857', linestyle='-', label=r'Held Branch (Atom Chip Trap): $z_{\mathrm{held}}(t) \equiv 0$')
ax2.plot(t_traj * 1e3, z_fall, color='#b91c1c', linestyle='-', label=r'Free-Fall Branch: $z_{\mathrm{fall}}(t) = -\frac{1}{2}g t^2$')
ax2.scatter([T_exp * 1e3], [-0.5 * g_acc * (T_exp**2) * 1e6], color='#1e3a8a', s=60, zorder=5,
            label=rf'Recombination: $\Delta z \approx 7.30\ \mu\mathrm{{m}}$ at $1.22$ ms')

ax2.set_xlabel('Time $t$ (ms)')
ax2.set_ylabel(r'Vertical Displacement $z$ ($\mu\mathrm{m}$)')
ax2.set_title('(B) Spatial Split of Wave Packet in Earth\'s Gravity', weight='bold')
ax2.legend(loc='lower left', framealpha=0.9)
ax2.set_xlim(0, 2.5)

# -----------------------------------------------------------------------------
# Panel C: Gravitational Decoherence Lifetime tau(M) Across 18 Orders of Mass
# -----------------------------------------------------------------------------
ax3 = axes[1, 0]
# Mass range from 10^-26 kg to 10^-8 kg
mass_range = np.logspace(-26, -14, 500)
# Gamma_UPD = (6 * G * M^2) / (5 * hbar * r_loc)
gamma_upd = (6.0 * G * (mass_range**2)) / (5.0 * hbar * r_loc)
tau_upd = 1.0 / gamma_upd

ax3.loglog(mass_range, tau_upd, color='#7c3aed', label=r'UPD Master-Functional Lifetime: $\tau \propto M^{-2}$')

# Specific landmarks
landmarks = [
    (m_Rb, r'$^{87}\mathrm{Rb}$ (Atom Chip, $4.1\times 10^5$ yr)', '#1e3a8a', (-15, 15)),
    (720 * amu, r'$\mathrm{C}_{60}$ ($5.9\times 10^3$ yr)', '#059669', (-15, -25)),
    (1e7 * amu, r'Virion ($16$ min)', '#d97706', (15, 10)),
    (5.204e-18, r'Exp. Crucis 1 ($\tau = 10$ ms)', '#dc2626', (15, 15)),
    (5.2e-16, r'Water Droplet ($1\ \mu$s)', '#475569', (-60, -25)),
]

for m_val, label, col, offset in landmarks:
    g_val = (6.0 * G * (m_val**2)) / (5.0 * hbar * r_loc)
    t_val = 1.0 / g_val
    ax3.scatter([m_val], [t_val], color=col, s=50, zorder=5)
    ax3.annotate(label, (m_val, t_val), textcoords="offset points", xytext=offset,
                 fontsize=7.5, color=col, weight='bold')

# Shaded experimental zones
ax3.axhspan(1e-4, 1e-1, color='#fee2e2', alpha=0.35, label=r'Optomechanical Measurement Window (100 $\mu$s - 100 ms)')
ax3.axhline(y=T_exp, color='#0284c7', linestyle=':', label='Atom Interferometer Duration ($T = 1.22$ ms)')

ax3.set_xlabel('Superposition Mass $M$ (kg)')
ax3.set_ylabel(r'Gravitational Coherence Lifetime $\tau$ (s)')
ax3.set_title('(C) Transition from Pure Quantum Waves to Macroscopic Classicality', weight='bold')
ax3.legend(loc='lower left', framealpha=0.9, fontsize=8)
ax3.set_xlim(1e-26, 1e-14)
ax3.set_ylim(1e-8, 1e16)

# -----------------------------------------------------------------------------
# Panel D: Discrimination of Mass-Scaling Exponents alpha (Gamma propto M^alpha)
# -----------------------------------------------------------------------------
ax4 = axes[1, 1]
m_norm = np.logspace(-20, -16, 300)
ref_m = 5.204e-18 # Exp Crucis 1 mass
ref_gamma = 100.33 # 1 / 10 ms

# Scaling models
gamma_upd_norm = ref_gamma * (m_norm / ref_m)**2.00     # alpha = 2.00
gamma_dp_norm = ref_gamma * (m_norm / ref_m)**1.67      # alpha = 1.67 (Diosi-Penrose)
gamma_gas_norm = ref_gamma * (m_norm / ref_m)**0.67     # alpha = 0.67 (Gas scattering)
gamma_rad_norm = ref_gamma * (m_norm / ref_m)**1.00     # alpha = 1.00 (Radiation)

ax4.loglog(m_norm / amu, gamma_upd_norm, color='#7c3aed', label=r'UPD Master Functional: $\Gamma \propto M^{2.00}$')
ax4.loglog(m_norm / amu, gamma_dp_norm, color='#2563eb', linestyle='--', label=r'Diósi--Penrose Model: $\Gamma \propto M^{1.67}$')
ax4.loglog(m_norm / amu, gamma_rad_norm, color='#f59e0b', linestyle='-.', label=r'Thermal Radiation: $\Gamma \propto M^{1.00}$')
ax4.loglog(m_norm / amu, gamma_gas_norm, color='#10b981', linestyle=':', label=r'Collisional Decoherence: $\Gamma \propto M^{0.67}$')

ax4.scatter([ref_m / amu], [ref_gamma], color='#dc2626', s=70, zorder=5, 
            label=r'Benchmark ($M_{\mathrm{crit}} = 3.13\times 10^{12}$ amu, $\Gamma = 100\ \mathrm{s}^{-1}$)')

ax4.set_xlabel('Superposition Mass $M$ (amu)')
ax4.set_ylabel(r'Decoherence Rate $\Gamma$ ($\mathrm{s}^{-1}$)')
ax4.set_title(r'(D) Power-Law Mass-Scaling Discrimination ($\Gamma \propto M^\alpha$)', weight='bold')
ax4.legend(loc='upper left', framealpha=0.9, fontsize=8)
ax4.set_xlim(1e7, 1e14)

plt.tight_layout()

output_path = r"C:\Users\я\Desktop\Quantum_Galileo_Phase_Dynamics\quantum_galileo_phase_dynamics.png"
plt.savefig(output_path, dpi=300)
print(f"Figure successfully saved to: {output_path}")
