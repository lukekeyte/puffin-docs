## Frequently Asked Questions

## Installation & Setup

### How do I install PUFFIN?

PUFFIN can be installed directly from PyPI using pip:

```bash
pip install puffin_disk
```

For development or local installation from source:

```bash
git clone https://github.com/lukekeyte/PUFFIN.git
cd PUFFIN
pip install -e .
```

### What are the system requirements?

PUFFIN requires:
- Python 3.8 or higher
- numpy >= 1.20.0
- scipy >= 1.7.0
- matplotlib >= 3.3.0

The package works on Windows, macOS, and Linux. Note that Windows users will see ASCII replacements for some Unicode characters in console output.

### I'm getting import errors. What's wrong?

First, ensure all dependencies are installed:

```bash
pip install numpy scipy matplotlib
```

If you're still experiencing issues, try updating your packages:

```bash
pip install --upgrade numpy scipy matplotlib
```

For development installations, make sure you're in the correct directory and using the `-e` flag.

<br/>

***

<br/>

## Model Selection & Usage

### Should I use the 1D or 2D model?

**Use the 1D model** (`DiskModel1D`) when:
- You only need midplane density profiles
- You're doing parameter surveys or sensitivity studies
- Computational speed is critical (1D models run in seconds)
- You're validating physical intuition about radial structure

**Use the 2D model** (`DiskModel2D`) when:
- You need full vertical structure
- You're generating inputs for 3D radiative transfer codes
- You want to study disk surface and wind launching regions
- You're investigating vertical temperature gradients and hydrostatic equilibrium

The 1D model is ~100× faster but provides less information. For most chemical modeling applications, the 2D model is recommended.

### How do I choose the grid resolution (`n_points`)?

**Minimum requirement**: 200 grid points (enforced by validation)

**Recommended for most applications**: 1000 grid points (default)

**Higher resolution (1500-2000)**: Use when:
- Studying sharp density gradients in the disk-wind transition
- Ensuring convergence in 2D hydrostatic equilibrium iterations
- Generating high-fidelity inputs for detailed radiative transfer

**Lower resolution (200-500)**: Acceptable for:
- Quick parameter space exploration
- 1D models where you'll regrid the output afterward

Note: Increasing resolution improves accuracy but increases runtime, especially for 2D models.

### What grid size should I use?

The default grid size is `min(8 × r_d, 800)` AU, which captures the disk and immediate wind region.

**Increase `gridsize` when**:
- Studying extended photoevaporative flows beyond 8×r_d
- The wind component dominates at large radii
- You need to match observations covering large angular extents

**Decrease `gridsize` when**:
- Focusing on the inner disk structure
- Computational memory is limited
- You're only interested in the disk interior

<br/>

***

<br/>

## Parameter Ranges & Validation

### What happens if I use parameters outside the validated range?

PUFFIN will raise a `ValueError` if you attempt to use parameters outside these ranges:
- Stellar mass: 0.3 to 3.0 M☉
- Disk radius: 20 to 150 AU  
- Surface density: 10 to 10,000 g cm⁻²
- FUV field: 100 to 100,000 G₀

These limits reflect the calibration against the FRIED grid. Using parameters outside these ranges may produce physically unrealistic results.

### Can I extrapolate beyond the validated ranges?

While PUFFIN won't prevent you from modifying the code to extrapolate, **this is strongly discouraged** unless you:

1. Carefully validate output structures against physical expectations
2. Have independent constraints (e.g., hydrodynamical simulations) to compare against
3. Clearly document that you're operating outside the validated regime

The parametric prescriptions (especially the γ scaling and plateau transitions) were calibrated specifically for the validated parameter space and may not generalize well.

### Why is my surface density at 1 AU so high/low?

The surface density normalization `sigma_1au` sets the overall disk mass scale. Typical values depend on your system:

- **Low-mass disks** (M_disk ~ 10⁻⁴ M☉): σ₁ₐᵤ ~ 10-100 g cm⁻²
- **Intermediate-mass disks** (M_disk ~ 10⁻³ M☉): σ₁ₐᵤ ~ 100-1000 g cm⁻²
- **Massive disks** (M_disk ~ 10⁻² M☉): σ₁ₐᵤ ~ 1000-10,000 g cm⁻²

Remember that σ ∝ r⁻¹ with exponential tapering, so the normalization at 1 AU propagates throughout the disk. If you know your desired disk mass, you can use `helpers.calculate_disk_mass()` to iterate toward the correct normalization.

<br/>

***

<br/>

## Mass-Loss Rates

### How is the mass-loss rate determined?

If you don't provide `m_dot` explicitly, PUFFIN interpolates from the FRIED grid (Haworth et al. 2018, 2023) using 4D linear interpolation across stellar mass, disk radius, surface density, and FUV field strength.

For 2D models, the interpolated value is scaled by a factor of 2 to account for systematic differences between 1D and 2D hydrodynamical simulations.

### Can I specify my own mass-loss rate?

Yes! Simply pass the `m_dot` parameter (in M☉ yr⁻¹):

```python
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, FFUV_G0, m_dot=1e-7)
```

This is useful when:
- You have mass-loss rates from your own hydrodynamical simulations
- You want to explore variations around the FRIED grid predictions
- You're modeling systems with additional physics (e.g., magnetic fields) not captured in FRIED

### What if interpolation fails or returns NaN?

This occurs when your requested parameters fall outside the FRIED grid's interpolation domain. Possible solutions:

1. Check that your parameters are within the validated ranges
2. Explicitly provide `m_dot` based on physical estimates or scaling relations
3. Adjust parameters slightly to move into the interpolation domain

A warning message will indicate when interpolation fails.

<br/>

***

<br/>

## Output Interpretation & Usage

### What do the output arrays represent?

**1D Model** returns:
- `radius`: Radial grid in AU (shape: `[n_points]`)
- `density`: Total midplane density in g cm⁻³ (shape: `[n_points]`)

**2D Model** returns:
- `r_array`: Radial grid in AU (shape: `[nr]`)
- `z_array`: Vertical grid in AU (shape: `[nz]`)
- `density`: Total gas density in g cm⁻³ (shape: `[nz, nr]`)

Both models also store component densities (disk, wind, plateau/bowl) as instance attributes for diagnostic purposes.

### Can I use the temperature arrays for chemical modeling?

**No.** This is explicitly stated in the documentation but bears repeating:

The temperature profiles computed during model construction are used **only** to establish the density structure through hydrostatic equilibrium. They do **not** represent self-consistent temperature fields for a given density distribution.

For chemical modeling or synthetic observations, you must:
1. Export PUFFIN density structures
2. Pass them to a dedicated radiative transfer code (e.g., DALI, RADMC-3D, ProDiMo)
3. Use the self-consistent temperature and radiation fields from that code

### How do I convert PUFFIN output for use with other codes?

Most radiative transfer codes accept density grids in similar formats. Typical workflow:

```python
# Generate PUFFIN model
r, z, rho = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, FFUV_G0).compute()

# Convert to code-specific format (example for DALI)
np.savetxt('density_structure.dat', 
           np.column_stack([r_grid.ravel(), z_grid.ravel(), rho.ravel()]))
```

Consult your radiative transfer code's documentation for specific input requirements (units, grid orientation, format).

### What units should I use?

PUFFIN uses the following units internally:
- **Length**: AU (radii) and cm (internal calculations)
- **Density**: g cm⁻³
- **Temperature**: K
- **Mass**: M☉
- **Mass-loss rate**: M☉ yr⁻¹
- **FUV field**: G₀ (Habing units, 1.6 × 10⁻³ erg cm⁻² s⁻¹)

All outputs use these same units, so you may need to convert for specific applications.

<br/>

***

<br/>

## Troubleshooting & Performance

### My 2D model is taking a very long time to run. Is this normal?

Typical runtimes depend on resolution:
- **1000 grid points**: ~1-3 minutes
- **1500 grid points**: ~5-10 minutes
- **2000 grid points**: ~15-30 minutes

If your model is taking significantly longer:

1. **Check your grid resolution**: Is `n_points` unnecessarily high?
2. **Verify convergence**: Look for console messages about iteration progress
3. **Check parameter values**: Extreme FUV fields or small disk radii can slow convergence
4. **Monitor memory usage**: Very high resolution can cause swapping on systems with limited RAM

### The model returned an error message. What does it mean?

Common error messages:

**"Stellar mass must be between 0.3 to 3.0 M_sun"**: Your `m_star` parameter is outside the validated range.

**"Need at least 200 grid points"**: Increase `n_points` to ensure numerical accuracy.

**"Grid size must be larger than disk radius"**: Your `gridsize` is too small; increase it or use the default.

**"ABORTED: Disk mass < 1e-5 M_sun"**: The disk is too low-mass for the model to handle reliably. Increase `sigma_1au` or `r_d`.

**"Hydrostatic equilibrium did not converge"**: The iterative solver failed. Try:
   - Increasing `N_ITER` (default: 20)
   - Adjusting the temperature gradient parameter `k` (default: 1.75)
   - Checking for extreme parameter combinations

### Why do I see different Unicode characters on Windows vs Mac/Linux?

PUFFIN detects your operating system and uses ASCII replacements for Unicode box-drawing characters and superscripts on Windows to ensure compatibility. This is purely cosmetic and doesn't affect model calculations.

You can suppress console output entirely with `verbose=False`:

```python
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, FFUV_G0, verbose=False)
```

### How do I access individual density components?

After running the model, you can access:

**1D model**:
- `model.rho_disk`: Disk component
- `model.rho_wind`: Wind component  
- `model.rho_plateau`: Plateau transition component

**2D model**:
- `model.rho_disk`: Disk component with hydrostatic equilibrium
- `model.rho_wind_sph`: Spherical wind component
- `model.rho_bowl`: Disk-wind transition ("halo") component
- `model.rho_wind`: Combined wind (max of spherical and bowl)

These are useful for understanding which component dominates in different regions.

<br/>

***

<br/>

## Physical Model & Limitations

### What physics is included in PUFFIN?

PUFFIN models:
- Power-law disk surface density with exponential tapering
- Vertical hydrostatic equilibrium (2D model)
- FUV heating in photodissociation regions (PDRs)
- Spherically diverging photoevaporative wind
- Smooth disk-wind transition regions

### What physics is NOT included?

PUFFIN does **not** model:
- Internal photoevaporation from the central star
- External EUV radiation
- Magnetic fields or MHD effects
- Time evolution or dynamical changes
- Dust dynamics (assumes well-mixed gas and dust for temperature structure only)
- Detailed chemical networks (use radiative transfer codes for this)

If these effects are important for your system, you'll need hydrodynamical simulations or specialized codes.

### How accurate are the density structures?

PUFFIN reproduces hydrodynamical simulations with typical factor-of-2 accuracy across ≥98% of the validated parameter space. Larger deviations can occur:
- Near sharp density gradients in the disk-wind interface
- In regions with strong FUV irradiation gradients
- At the edges of the validated parameter space

For most chemical modeling applications, this accuracy is sufficient given other uncertainties in disk properties.

### Why does the plateau parameter λ depend on r_d and F_FUV?

The plateau region represents an extended disk atmosphere produced by external FUV irradiation. Its extent depends on:
- **Disk radius** (`r_d`): Larger disks have more extended plateaus
- **FUV field strength**: Stronger fields produce sharper disk-wind transitions

The parametrization `λ = r_d^p + (F_FUV/100)^q` with p=0.2 and q=0.4 was empirically calibrated to match hydrodynamical simulations. You can adjust `p` and `q` if you have specific constraints, but the defaults are recommended.

### What is the `gamma` parameter and when should I change it?

The `gamma` parameter controls the steepness of the exponential disk taper:

Σ(r) ∝ exp[−(r/r_d)^γ]

By default, PUFFIN calculates γ using:

γ = 0.77 × (M_*/M☉)^0.10 × (r_d/AU)^0.78 × (F_FUV/100 G₀)^0.07

This ensures physically motivated tapering. You should only override this if:
- You have specific observational constraints on the outer disk profile
- You're testing sensitivity to the taper steepness
- You're matching a specific hydrodynamical model

Typical values range from γ ~ 2-4, with higher values producing sharper cutoffs.

<br/>

***

<br/>

## Best Practices & Recommendations

### How do I cite PUFFIN in my research?

If you use PUFFIN, please cite:

**Primary reference:**
```
Keyte & Haworth (2026), arXiv:2602.02011
"A parametric model for externally irradiated protoplanetary disks with photoevaporative winds"
```

**For mass-loss rates from FRIED:**
```
Haworth et al. (2018), MNRAS, 481, 452
Haworth et al. (2023), MNRAS, 526, 4315
```

### What's the recommended workflow for a chemical modeling project?

1. **Define your disk parameters** based on observations or theoretical expectations
2. **Generate the density structure** using PUFFIN 2D model
3. **Validate the structure** by plotting and checking for physical reasonableness
4. **Export to radiative transfer** (e.g., DALI, RADMC-3D) for self-consistent temperature/radiation
5. **Run chemistry** on the full 3D structure with proper temperature/radiation fields
6. **Generate observables** and compare with data

Never skip step 4—using PUFFIN temperatures directly for chemistry will give incorrect results.

### How often should I expect to update PUFFIN?

Check the GitHub repository and PyPI for updates. Significant changes will be announced in release notes. For critical research, pin your version:

```bash
pip install puffin_disk==1.0.0
```

This ensures reproducibility across your project.

### Where can I get help or report bugs?

- **Documentation**: [https://puffin.readthedocs.io](https://puffin.readthedocs.io)
- **GitHub Issues**: [https://github.com/lukekeyte/PUFFIN](https://github.com/lukekeyte/PUFFIN)
- **Email**: l.keyte@qmul.ac.uk

When reporting issues, please include:
- Your operating system and Python version
- The complete error message
- A minimal example that reproduces the problem
- Your parameter values

<br/>

***

<br/>

## Advanced Usage

### Can I modify the source code for my specific application?

Yes! PUFFIN is open-source under the MIT License. You're welcome to:
- Modify prescriptions for your specific needs
- Add new physical components
- Integrate with your own codes

If you make improvements that might benefit the community, please consider contributing them back via a pull request.

### How do I run PUFFIN in batch mode for parameter surveys?

Suppress verbose output and wrap in a loop:

```python
import puffin_disk
import numpy as np

# Parameter ranges
masses = np.linspace(0.3, 3.0, 10)
fuv_fields = np.logspace(2, 5, 10)

results = []
for m_star in masses:
    for FFUV_G0 in fuv_fields:
        model = puffin_disk.DiskModel1D(
            m_star, r_d=100, sigma_1au=1000, FFUV_G0=FFUV_G0,
            verbose=False
        )
        r, rho = model.compute()
        results.append((m_star, FFUV_G0, r, rho))
```

For large surveys, consider parallelization with `multiprocessing` or `joblib`.

### How do I interpolate PUFFIN output onto a different grid?

Use scipy's interpolation tools:

```python
from scipy.interpolate import interp1d

# 1D example
f = interp1d(r_array, rho_array, kind='linear', bounds_error=False, fill_value=0)
new_r = np.linspace(0.1, 800, 2000)
new_rho = f(new_r)

# 2D example
from scipy.interpolate import griddata
points = np.array([[r, z] for z_idx, z in enumerate(z_array) 
                            for r_idx, r in enumerate(r_array)])
values = density.ravel()
new_rho_2d = griddata(points, values, (new_r_grid, new_z_grid), method='linear')
```

### Can I access the FRIED grid data directly?

The FRIED lookup table is included with PUFFIN in the package data. You can access it using:

```python
from pathlib import Path
import numpy as np

# Find package directory
import puffin_disk
package_dir = Path(puffin_disk.__file__).parent

# Load FRIED data
data_file = package_dir / 'data' / 'FRIEDV2_ALL_fPAH1p0_growth.dat'
data = np.loadtxt(data_file)

# Columns: m_star, r_d, sigma_1au, _, F_FUV, log_mdot
```

This can be useful for plotting mass-loss rate trends or implementing your own interpolation schemes.

