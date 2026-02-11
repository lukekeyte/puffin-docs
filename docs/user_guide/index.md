## User Guide

This comprehensive guide provides detailed tutorials, advanced usage examples, and best practices for using `PUFFIN` to model externally irradiated protoplanetary disks with photoevaporative winds.

<br/>

***

<br/>

## Tutorial 1: Basic 1D Model

### Overview

The 1D model computes the radial density structure along the midplane. This is the simplest and fastest option, ideal for quick parameter studies.

### Basic Usage

```python
import puffin_disk
import numpy as np
import matplotlib.pyplot as plt

# Define physical parameters
m_star    = 1.0      # Stellar mass (M_sun)
r_d       = 100.0    # Disk outer radius (AU)
sigma_1au = 100.0    # Surface density at 1 AU (g cm^-2)
F_FUV     = 1000.0   # External FUV field (G_0)

# Create and compute model
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV)
r_array, rho_array = model.compute()

# Plot the result
plt.figure(figsize=(8, 6))
plt.loglog(r_array, rho_array, linewidth=2, color='#2E86AB')
plt.xlabel('Radius (AU)', fontsize=14)
plt.ylabel(r'Midplane Density (g cm$^{-3}$)', fontsize=14)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('density_1d.png', dpi=300)
plt.show()
```

### Understanding the Output

The `compute()` method returns two arrays:
- **`r_array`**: Radial grid in AU (default: 200 logarithmically-spaced points)
- **`rho_array`**: Gas density at the midplane in g cmâ»Â³

The model automatically combines three components:
1. **Disk interior**: Power-law surface density with exponential taper
2. **Photoevaporative wind**: Spherically diverging outflow
3. **Transition region**: Smooth connection using 'plateau' prescription (see Keyte & Haworth 2026)

You can also access individual components:
```python
rho_disk    = model.rho_disk      # Disk component only
rho_wind    = model.rho_wind      # Wind component only
rho_plateau = model.rho_plateau   # Transition region
```

### Key Features

**Automatic mass-loss rate interpolation**: If you don't specify `m_dot`, `PUFFIN` automatically interpolates from the `FRIED` grid based on your input parameters:

```python
# Mass-loss rate interpolated automatically
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV)
r_array, rho_array = model.compute()

# Check what was used
print(f"Interpolated mass-loss rate: {model.m_dot:.2e} M_sun/yr")
```

**Console output**: By default, PUFFIN prints a formatted table showing all model parameters:

```
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ INITIALIZATION ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

 > Model initialized
 ┌────────────────────┬───────────────┬──────────┐
 │ Parameter          │ Value         │ Unit     │
 ├────────────────────┼───────────────┼──────────┤
 │ Stellar mass       │ 1.00          │ M_sun    │
 │ Disk radius        │ 100.0         │ AU       │
 │ Sigma (1AU)        │ 100.0         │ g cm⁻²   │
 │ FUV field          │ 1.00 × 10³    │ G0       │
 │ N grid cells       │ 200           │          │
 │ Grid size          │ 800.0         │ AU       │
 │ Mass-loss rate     │ 1.23 × 10⁻⁸   │ M_sun/yr │
 │ Gamma              │ 2.45          │          │
 │ p                  │ 0.20          │          │
 │ q                  │ 0.40          │          │
 └────────────────────┴───────────────┴──────────┘
```

To disable console output:
```python
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, verbose=False)
```

<br/>

***

<br/>

## Tutorial 2: Basic 2D Model

### Overview

The 2D model expands the framework by incorporating the disk’s vertical structure under hydrostatic equilibrium, the photoevaporative wind, and a transition region that smoothly links the disk to the wind.

### Basic Usage

```python
import puffin_disk
import numpy as np
import matplotlib.pyplot as plt

# Define physical parameters (same as 1D)
m_star    = 0.5      # Stellar mass (M_sun)
r_d       = 100.0    # Disk outer radius (AU)
sigma_1au = 1000.0   # Surface density at 1 AU (g cm^-2)
F_FUV     = 3000.0   # External FUV field (G_0)

# Create and compute 2D model
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, F_FUV)
r_array, z_array, rho_array = model.compute()

# Create contour plot
fig, ax = plt.subplots(figsize=(10, 6))
levels = np.arange(-20, -11, 0.2)
contour = ax.contourf(r_array, z_array, np.log10(rho_array), 
                      levels=levels, cmap='Spectral_r', extend='both')
ax.set_xlabel('Radius (AU)', fontsize=14)
ax.set_ylabel('Height (AU)', fontsize=14)
cbar = plt.colorbar(contour, ax=ax, label=r'log$_{10}$ Density (g cm$^{-3}$)')
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig('density_2d.png', dpi=300)
plt.show()
```

### Understanding the Output

The `compute()` method returns three arrays:
- **`r_array`**: Radial grid in AU (default: 1000 points)
- **`z_array`**: Vertical grid in AU (default: 1000 points)
- **`rho_array`**: 2D gas density array in g cm⁻³ with shape `(nz, nr)`

**Important**: The density array uses row ordering where the first dimension is vertical (z) and the second is radial (r). When plotting, use `contourf(r_array, z_array, rho_array)`.

Access model components:
```python
rho_disk = model.rho_disk        # Disk component with hydrostatic structure
rho_wind = model.rho_wind        # Combined wind (spherical + transition)
```

The typical runtime for a 2D model with n_points=1000 is ~2-3 minutes on a standard laptop.

<br/>

***

<br/>

## Tutorial 3: Customizing Model Parameters

### Grid Resolution

**1D models**: Default is 200 points. Higher resolution is recommended for capturing sharper density gradients:

```python
# Standard resolution
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, n_points=200)

# High resolution for detailed structure
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, n_points=1000)
```

**2D models**: Default is 1000×1000. Resolution ≥1000 is required for accurate hydrostatic equilibrium:

```python
# Standard resolution
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, F_FUV, n_points=1000)

# High resolution for detailed structure
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, n_points=2000)
```

If you need a lower-resolution model (e.g., for use as input to thermochemical calculations), first compute the PUFFIN model with at least 1000 grid points, and then regrid it to the desired resolution.

### Grid Size

The computational domain extends from 0 to `gridsize` (in AU). Default is `min(8 × r_d, 800)` AU. Generally, `8 × r_d` is required to capture the full extent of dense photoevaporative winds.

```python
# Modify the gidsize (in AU)
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, gridsize=1500)
```

### Mass-Loss Rate

Override automatic interpolation with your own value:

```python
# Specify mass-loss rate directly (M_sun/yr)
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, m_dot=1e-8)

# For 2D models, note that PUFFIN applies 2× scaling internally
# to match systematic differences in 2D hydrodynamical simulations
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, F_FUV, m_dot=1e-8)
```

### Taper Parameter (γ)

The exponential tapering parameter `gamma` controls how steeply the disk truncates. PUFFIN uses an empirical scaling by default, but you can override it:

```python
# Use default empirical prescription
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV)

# Sharper cutoff (higher gamma)
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, gamma=4.0)

# Gentler cutoff (lower gamma)
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, gamma=2.0)
```

Typical values: 1.5–4.0. Higher values create more abrupt disk truncation.

### Transition Region Parameters

Fine-tune the disk-wind transition:

```python
# Standard transition (default)
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, p=0.2, q=0.4)

# Slower transition (more extended plateau)
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, p=0.1, q=0.2)

# Faster transition (sharper disk-wind interface)
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, p=0.3, q=0.6)
```

### Temperature Gradient Steepness (2D only)

Control the vertical temperature transition sharpness with parameter `k`:

```python
# Standard gradient (default)
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, F_FUV, k=1.75)

# Sharper temperature gradient
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, F_FUV, k=3.0)

# Gentler gradient
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, F_FUV, k=1.0)
```

### Hydrostatic Equilibrium Iterations (2D only)

Increase iterations if the model fails to converge:

```python
# Standard iteration count (default: 20)
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, F_FUV, N_ITER=20)

# More iterations for better convergence
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, F_FUV, N_ITER=50)
```

Most models converge within the default 20 iterations.

<br/>

***

<br/>

## Tutorial 4: Parameter Space Exploration

### Systematic Parameter Scans

Efficiently explore how disk properties vary across parameter space:

```python
import puffin_disk
import numpy as np
import matplotlib.pyplot as plt

# Define parameter grid
masses = [0.3, 0.7, 2.0]       # M_sun
FUV_fields = [1e2, 1e3, 1e4]   # G_0

# Fixed parameters
r_d = 100.0
sigma_1au = 100.0

# Storage for results
results = {}

# Loop over parameter combinations
for m_star in masses:
    for F_FUV in FUV_fields:
        key = f"M{m_star}_F{F_FUV:.0e}"
        
        # Compute model (use verbose=False to reduce output)
        model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV, 
                                        verbose=False)
        r, rho = model.compute()
        
        results[key] = {
            'radius': r,
            'density': rho,
            'm_star': m_star,
            'F_FUV': F_FUV,
            'm_dot': model.m_dot
        }

# Plot family of density profiles
fig, ax = plt.subplots(figsize=(10, 6))

for key, data in results.items():
    label = f"M={data['m_star']} M☉, F={data['F_FUV']:.0e} G₀"
    ax.loglog(data['radius'], data['density'], label=label, linewidth=2)

ax.set_xlabel('Radius (AU)', fontsize=14)
ax.set_ylabel(r'Density (g cm$^{-3}$)', fontsize=14)
ax.legend(fontsize=10)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('parameter_scan.png', dpi=300)
plt.show()
```

<br/>

***

<br/>

## Tutorial 5: Integration with Chemical Models

### Using `PUFFIN` density structure as input to `DALI` chemical model

`DALI` (Bruderer et al. 2012, 2013) requires a specific `setup_grid.dat` file format that includes not only the gas density structure, but also grid cell boundaries, gas-to-dust ratios, and dust settling prescriptions. 

Because PUFFIN computes only the gas density structure, converting PUFFIN outputs to DALI format requires you to specify additional disk properties:
- Gas-to-dust ratio in the shielded disk interior
- Gas-to-dust ratio in the dust-depleted wind
- Dust settling parameters (scale height and grain size distribution)
- Physical criterion for the disk-wind boundary (e.g., optical depth threshold, density threshold)

This tutorial demonstrates an example workflow based on the implementation in Keyte & Haworth (2025), where the transition from disk to wind is defined using an arbitrary density threshold n=10⁸ cm⁻³. Note that these properties are science choices that depend on your specific research questions—there are no universal "correct" values.

#### Step 1: Save PUFFIN Output

First, run `PUFFIN` and save the density structure:

```python
import puffin_disk
import numpy as np
from scipy.interpolate import RegularGridInterpolator

# Generate 2D model at high resolution
m_star = 1.0
r_d = 100.0
sigma_1au = 1000.0
F_FUV = 1000.0

# Compute at high resolution for accuracy
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, F_FUV, n_points=1000)
r_array_hr, z_array_hr, rho_array_hr = model.compute()

# Convert density to number density
mu = 1.4  # Mean molecular weight
m_p = 1.67262192e-24  # Proton mass in g
n_gas_hr = rho_array_hr / (mu * m_p)

# ========================================================================
# REGRID TO LOWER RESOLUTION FOR DALI
# ========================================================================

# Define lower resolution grid for DALI (200x200)
n_r_dali = 200
n_z_dali = 200

# Create grid
r_array = np.logspace(np.log10(r_array_hr[0]), np.log10(r_array_hr[-1]), n_r_dali)
z_min = 1e-2  # Small offset to avoid log(0)
z_array_log = np.logspace(np.log10(z_min), np.log10(z_array_hr[-1]), n_z_dali - 1)
z_array = np.concatenate([[0.0], z_array_log])  # z needs to start at 0 in DALI

# Create interpolator for high-resolution density
interpolator = RegularGridInterpolator(
    (r_array_hr, z_array_hr), 
    n_gas_hr.T,  # Transpose to (nr, nz) for interpolator
    method='linear',
    bounds_error=False,
    fill_value=1e-30
)

# Interpolate to DALI grid
n_gas = np.zeros((n_z_dali, n_r_dali))
for i in range(n_r_dali):
    for j in range(n_z_dali):
        n_gas[j, i] = interpolator([r_array[i], z_array[j]])

print(f"Regridded from {len(r_array_hr)}x{len(z_array_hr)} to {n_r_dali}x{n_z_dali}")

# ========================================================================

# Define disk-wind boundary using density threshold
# Cells above this threshold are "disk", below are "wind"
n_threshold = 1e8  # cm^-3 (typical disk-wind boundary)

# Flatten arrays for saving
n_r, n_z = len(r_array), len(z_array)
r_flat = []
z_flat = []
n_flat = []

for i in range(n_r):
    for j in range(n_z):
        r_flat.append(r_array[i])
        z_flat.append(z_array[j])
        n_flat.append(n_gas[j, i])

# Save to file
output_file = 'puffin_outputs.dat'
np.savetxt(output_file, 
           np.column_stack([r_flat, z_flat, n_flat]),
           header=f'r(AU) z(AU) n_gas(cm^-3) | Grid: {n_r}x{n_z} | n_threshold={n_threshold:.1e} cm^-3',
           fmt='%.6e')

print(f"PUFFIN output saved to {output_file}")
print(f"Grid dimensions: {n_r} x {n_z}")
print(f"Disk-wind boundary set at n = {n_threshold:.1e} cm^-3")
```

#### Step 2: Create DALI Setup File

Now create the DALI `setup_grid.dat` file. This includes additional physics choices about dust properties:

```python
import numpy as np

# Load PUFFIN output
data = np.loadtxt('puffin_outputs.dat', unpack=True)

# Grid dimensions (200x200 after regridding)
n_r = 200  # Number of radial grid points
n_z = 200  # Number of vertical grid points

# Reshape to 2D grids
rr = np.reshape(data[0], (n_r, n_z))
zz = np.reshape(data[1], (n_r, n_z))
ngas = np.reshape(data[2], (n_r, n_z))

# ========================================================================
# DUST PARAMETERS - These are user choices based on your science goals
# ========================================================================

gd_disk = 100        # Gas-to-dust ratio in disk (standard ISM value)
gd_wind = 1/3e-4     # Gas-to-dust in wind (dust-depleted, only small grains)
chi = 0.2            # Scale height parameter for settling
f = 0.9              # Fraction of large grains at midplane
n_threshold = 1e8    # Density threshold for disk-wind boundary (cm^-3)

# ========================================================================

# Create DALI setup_grid.dat file
outfile = 'setup_grid.dat'

with open(outfile, "w") as f_new:
    # Write header
    f_new.write("# number of cells in r-direction \n")
    f_new.write("%i \n" % (n_r - 1))
    f_new.write("# number of cells in z-direction \n")
    f_new.write("%i \n" % (n_z - 1))
    f_new.write("#  i_r    i_z               ra               rb               za               zb            n_gas      gas-to-dust             f_ls region \n")
    
    # Loop over grid cells
    for i in range(n_r - 1):
        
        # Calculate scale height at this radius
        # (defined where density drops to 1/sqrt(e) of midplane value)
        max_dens = np.max(ngas[i, :])
        try:
            scaleheight_idx = np.where(ngas[i, :] < max_dens * np.exp(-0.5))[0][0]
            scaleheight_au = zz[i, scaleheight_idx]
        except:
            scaleheight_idx = 0
            scaleheight_au = zz[i, 0]
        
        for j in range(n_z - 1):
            
            # Cell boundaries
            ra = rr[i][j]
            rb = rr[i+1][j]
            
            if j == 0:
                za = 0.0
                zb = zz[i][j+1]
            else:
                za = zz[i][j]
                zb = zz[i][j+1]
            
            # Cell midpoints
            r_mid = 0.5 * (ra + rb)
            z_mid = max(0.5 * (za + zb), 1e-10)  # Avoid division by zero
            
            # Current cell density
            n_gas = ngas[i][j]
            
            # ===============================================
            # DISK vs WIND: Use density threshold
            # ===============================================
            
            is_disk = (n_gas > n_threshold)
            
            # ===============================================
            # LARGE GRAIN FRACTION (f_ls) - Dust Settling
            # ===============================================
            
            # Scale height angle and polar angle
            h = np.arctan(scaleheight_au / r_mid)
            h = np.maximum(h, 1e-12)
            theta = np.arctan(r_mid / z_mid)  # Polar angle from z-axis
            
            if is_disk:
                # Inside dense disk: calculate settling
                prefactor = f / ((1 - f) * chi)
                term1 = -0.5 * (((np.pi/2) - theta) / (chi * h))**2
                term2 = 0.5 * (((np.pi/2) - theta) / h)**2
                expo = np.exp(term1 + term2)
                
                # f_ls = fraction of large grains
                X_ratio = prefactor * expo
                f_ls = X_ratio / (1.0 + X_ratio)
                f_ls = np.maximum(1e-10, f_ls)
            else:
                # Wind region: no large grains
                f_ls = 1e-10
            
            # ===============================================
            # GAS-TO-DUST RATIO
            # ===============================================
            
            if is_disk:
                gtd = gd_disk  # Dense disk
            else:
                gtd = gd_wind  # Tenuous wind (dust-depleted)
            
            # Region identifier (typically 1 for entire disk)
            region = 1
            
            # Write row
            f_new.write("%6i %6i %15.10e %15.10e %15.10e %15.10e %15.10e %15.10e %15.10e %6i \n" 
                       % (i+1, j+1, ra, rb, za, zb, n_gas, gtd, f_ls, region))

print(f"DALI setup file created: {outfile}")
print(f"Grid dimensions: {n_r-1} x {n_z-1} cells")
print(f"Disk-wind boundary: n > {n_threshold:.1e} cm^-3")
print("Ready to run DALI with this grid")
```

#### Understanding the DALI Format

The `setup_grid.dat` file has the following structure:

**Header:**
- Number of radial cells
- Number of vertical cells  
- Column descriptions

**Data columns (for each cell):**
1. **i_r**: Radial cell index
2. **i_z**: Vertical cell index
3. **ra**: Inner radial boundary (AU)
4. **rb**: Outer radial boundary (AU)
5. **za**: Lower vertical boundary (AU)
6. **zb**: Upper vertical boundary (AU)
7. **n_gas**: Gas number density (cm⁻³)
8. **gas-to-dust**: Gas-to-dust mass ratio
9. **f_ls**: Large grain fraction (0-1)
10. **region**: Region identifier (typically 1)

#### Key Physics Choices

When creating DALI input, you must specify dust parameters based on your science goals:

**Gas-to-Dust Ratio:**
- **`gd_disk`** (e.g., 100): Standard ISM value for shielded disk interior
- **`gd_wind`** (e.g., 3000 or higher): Dust-depleted wind where grains have settled/been lost (eg. Facchini et al. 2016)
- Transition based on density threshold (eg. Keyte & Haworth 2025) or optical depth τ = 1 threshold (eg. Keyte & Haworth 2026)

**Dust Settling Parameters:**
- **`f`** (e.g., 0.9): Fraction of large grains at the midplane
- **`chi`** (e.g., 0.2): Ratio of dust scale height to gas scale height
- These control vertical stratification of grain sizes

The **f_ls** (large grain fraction) calculation implements a settling prescription where:
- Large grains settle toward the midplane
- Small grains remain well-mixed
- The vertical distribution depends on the local scale height angle

**Important Notes:**

1. **Temperature fields**: As always, do NOT use `PUFFIN` temperatures. DALI will compute self-consistent temperatures through radiative transfer.

2. **Dust choices are yours**: The gas-to-dust ratios and settling parameters shown here are examples. Adjust based on your specific disk model and science questions.

#### Verification

After creating the setup file, verify it looks correct:

```python
# Quick visual check
import matplotlib.pyplot as plt

# Load the created setup file
setup_data = np.loadtxt('setup_grid.dat', skiprows=4, unpack=True)

# Reshape to 2D (note: n_r-1 and n_z-1 cells)
n_cells_r = n_r - 1
n_cells_z = n_z - 1

setup_r = np.reshape(setup_data[2], (n_cells_r, n_cells_z))  # rb values
setup_z = np.reshape(setup_data[4], (n_cells_z, n_cells_z))  # zb values  
setup_ngas = np.reshape(setup_data[6], (n_cells_r, n_cells_z))
setup_fls = np.reshape(setup_data[8], (n_cells_r, n_cells_z))

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Plot density
levels = np.arange(2, 14, 0.2)
im1 = axes[0].contourf(setup_r, setup_z, np.log10(setup_ngas), 
                       levels=levels, cmap='Spectral_r', extend='both')
axes[0].set_xlabel('Radius (AU)')
axes[0].set_ylabel('Height (AU)')
axes[0].set_title('Gas Number Density')
plt.colorbar(im1, ax=axes[0], label='log₁₀ n (cm⁻³)')

# Plot settling
im2 = axes[1].contourf(setup_r, setup_z, setup_fls,
                       levels=np.arange(0, 1, 0.1), cmap='Spectral_r', extend='both')
axes[1].set_xlabel('Radius (AU)')
axes[1].set_ylabel('Height (AU)')
axes[1].set_title('Large Grain Fraction')
plt.colorbar(im2, ax=axes[1], label='f_ls')

plt.tight_layout()
plt.savefig('dali_setup_verification.png', dpi=200)
plt.show()
```

<br/>

***

<br/>

## Best Practices

### Temperature and Radition Fields: Critical Warning

**⚠️ NEVER use PUFFIN temperature/radiation fields directly for chemistry or radiative transfer.**

The temperatures computed by `PUFFIN` are used *only* to establish the density structure through hydrostatic equilibrium. They are not self-consistent with the radiation field and should not be trusted for any downstream analysis.

**Always:**
1. Use PUFFIN to generate density structures only
2. Input these densities into proper radiative transfer codes (`DALI`, `RADMC-3D`, `ProDiMo`)
3. Use the self-consistent temperatures and radiation fields from radiative transfer for chemistry

<br/>

***

<br/>

## Troubleshooting

### Common Issues

**Issue**: "Disk mass < 1e-5 M_sun" abort message

**Cause**: Surface density too low or disk radius too small

**Solution**: Increase `sigma_1au` or `r_d`

---

**Issue**: 2D model produces unusual structure

**Cause**: Grid resolution too low or parameters produce extreme conditions

**Solutions**:
- Increase `n_points` to >>1000
- Increase `N_ITER` for better convergence
- Check parameters are within validated range
- Vary `k` parameter for gentler/steeper temperature gradients
- Manually specify `gamma`, `p`, and `q` to adjust disk-wind transition

---

**Issue**: Wind densities seem too high/low

**Cause**: Mass-loss rate interpolation or manual specification

**Solutions**:
- Check interpolated m_dot value: `print(model.m_dot)`
- Manually specify m_dot if needed
- For 2D, remember the 2× internal scaling factor
- Verify you're within `FRIED` grid coverage

---

**Issue**: Unexpected density jumps or discontinuities

**Cause**: Insufficient grid resolution or numerical artifacts

**Solutions**:
- Increase `n_points`
- Adjust `gamma` parameter for smoother taper
- Modify `p` and `q` for gentler transition

---

**Issue**: Results don't match hydrodynamical simulations exactly

**Expected**: PUFFIN is a parametric approximation with typical factor-of-a-few accuracy

**When to worry**: Deviations >5× suggest:
- Parameters outside validated range
- Unusual physics not captured by parametric model
- Need for full hydrodynamical simulation

<br/>

***

<br/>


## Further Resources

### Code Repository
- GitHub: [https://github.com/lukekeyte/PUFFIN](https://github.com/lukekeyte/PUFFIN)
- Report bugs, request features, or contribute improvements

### Documentation
- Full documentation: [https://puffin.readthedocs.io](https://puffin.readthedocs.io)
- Physical model details: See "Physical Model" section
- API reference: See source code docstrings

### Key References

**PUFFIN framework:**
- Keyte & Haworth (2026), arXiv:2602.02011

**FRIED hydrodynamical grid:**
- Haworth et al. (2018), MNRAS 481, 452
- Haworth et al. (2023), MNRAS 526, 4315

### Getting Help

1. **Check the documentation**: Most questions answered in Physical Model and FAQ sections
2. **Email support**: l.keyte@qmul.ac.uk for technical questions
3. **GitHub Issues**: For bug reports and feature requests

For questions or support, please contact **l.keyte@qmul.ac.uk** or open an issue on [GitHub](https://github.com/lukekeyte/PUFFIN).
