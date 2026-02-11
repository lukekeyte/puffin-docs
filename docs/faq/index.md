## Frequently Asked Questions

### Installation & Setup

#### How do I install PUFFIN?

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

#### What are the system requirements?

PUFFIN requires:
- Python 3.8 or higher
- numpy >= 1.20.0
- scipy >= 1.7.0
- matplotlib >= 3.3.0

The package has been fully tested on Mac/Linux, with limited testing on Windows.

#### I'm getting import errors. What's wrong?

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

### Model Selection & Usage

#### How do I choose the grid resolution (`n_points`)?

**Minimum requirement**: 200 grid points for 1D models and 1000x1000 grid points for 2D models (enforced)

**Recommended for most applications**: >1000 grid points

Increasing resolution improves accuracy but increases runtime, especially for 2D models.

NOTE: If you need a lower-resolution 2D model (e.g., for use as input to thermochemical calculations), first compute the `PUFFIN` model with at least 1000 grid points, and then regrid it to the desired resolution (see below).


#### What grid size should I use?

The default grid size is `min(8 × r_d, 800)` AU, which captures the disk and immediate wind region.

**Increase `gridsize` when**:
- Studying extended photoevaporative flows beyond 8×r_d
- The wind component dominates at large radii
- You need to match observations covering large angular extents

**Decrease `gridsize` when**:
- Focusing on the inner disk structure
- Wind structure is minimally extended

<br/>

***

<br/>

### Parameter Ranges & Validation

#### What happens if I use parameters outside the validated range?

`PUFFIN` will raise a `ValueError` if you attempt to use parameters outside these ranges:
- Stellar mass: 0.3 to 3.0 M☉
- Disk radius: 20 to 150 AU  
- Surface density: 10 to 10,000 g cm⁻²
- FUV field: 100 to 100,000 G₀

These limits reflect the calibration against the `FRIED` grid. Using parameters outside these ranges may produce physically unrealistic results.

#### Can I extrapolate beyond the validated ranges?

While you could technically modify the code to extrapolate, **this is strongly discouraged** unless you:

1. Carefully validate output structures against reasonable expectations
2. Have independent constraints (e.g., hydrodynamical simulations) to compare against
3. Clearly document that you're operating outside the validated regime

The parametric prescriptions were calibrated specifically for the validated parameter space and may not generalize well.

<br/>

***

<br/>

### Mass-Loss Rates

#### How is the mass-loss rate determined?

If you don't provide `m_dot` explicitly, `PUFFIN` interpolates from the `FRIED` grid (Haworth et al. 2018, 2023) using 4D linear interpolation across stellar mass, disk radius, surface density, and FUV field strength.

For 2D models, the interpolated value is scaled by a factor of 2 to account for systematic differences between 1D and 2D hydrodynamical simulations.

#### Can I specify my own mass-loss rate?

Yes! Simply pass the `m_dot` parameter (in M☉ yr⁻¹):

```python
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, FFUV_G0, m_dot=1e-7)
```

NOTE: If using a user-defined mass-loss rate, take care to ensure it is physically justified given the model input parameters.

<br/>

***

<br/>

### Output Interpretation & Usage

#### What do the output arrays represent?

**1D Model** returns:
- `radius`: Radial grid in AU (shape: `[n_points]`)
- `density`: Total midplane density in g cm⁻³ (shape: `[n_points]`)

**2D Model** returns:
- `r_array`: Radial grid in AU (shape: `[nr]`)
- `z_array`: Vertical grid in AU (shape: `[nz]`)
- `density`: Total gas density in g cm⁻³ (shape: `[nz, nr]`)

Both models also store component densities (disk, wind, transition) as instance attributes for diagnostic purposes.

#### Can I use the temperature arrays for chemical modeling?

**No.** This is explicitly stated in the documentation but bears repeating:

The temperature profiles computed during model construction are used **only** to establish the density structure through hydrostatic equilibrium. They do **not** represent self-consistent temperature fields for a given density distribution.

For chemical modeling or synthetic observations, you must:
1. Export `PUFFIN` density structures
2. Pass them to a dedicated radiative transfer code (e.g., `DALI`, `RADMC-3D`, `ProDiMo`)
3. Use the self-consistent temperature and radiation fields from that code

#### How do I convert PUFFIN output for use with other codes?

Most radiative transfer codes accept density grids in similar formats. An detailed example using PUFFIN with the `DALI` code is provided in the User Guide.

Consult your radiative transfer code's documentation for specific input requirements (units, grid orientation, format).

#### What units should I use?

`PUFFIN` uses the following units internally:
- **Length**: AU (radii) and cm (internal calculations)
- **Density**: g cm⁻³
- **Temperature**: K
- **Mass-loss rate**: M☉ yr⁻¹
- **FUV field**: G₀ (Habing units, 1.6 × 10⁻³ erg cm⁻² s⁻¹)

All outputs use these same units, so you may need to convert for specific applications.

<br/>

***

<br/>

### Troubleshooting & Performance

#### My 2D model is taking a very long time to run. Is this normal?

Typical runtimes depend on resolution:
- **1000 grid points**: ~2-3 minutes
- **1500 grid points**: ~5-10 minutes
- **2000 grid points**: ~15-30 minutes

If your model is taking significantly longer:

1. **Check your grid resolution**: Is `n_points` unnecessarily high?
2. **Verify convergence**: Look for console messages about iteration progress

#### The model returned an error message. What does it mean?

Common error messages:

**"Stellar mass must be between 0.3 to 3.0 M_sun"**: Your `m_star` parameter is outside the validated range.

**"Need at least 200 grid points"**: Increase `n_points` to ensure numerical accuracy.

**"Grid size must be larger than disk radius"**: Your `gridsize` is too small; increase it or use the default.

**"ABORTED: Disk mass < 1e-5 M_sun"**: The disk is too low-mass for the model to handle reliably. Increase `sigma_1au` or `r_d`.

**"Hydrostatic equilibrium did not converge"**: The iterative solver failed. Try:
   - Increasing `N_ITER` (default: 20)
   - Adjusting the temperature gradient parameter `k` (default: 1.75)
   - Checking for extreme parameter combinations


#### How do I access individual density components?

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

### Physical Model & Limitations

#### What physics is included in PUFFIN?

`PUFFIN` models:
- Power-law disk surface density with exponential tapering
- Vertical hydrostatic equilibrium (2D model)
- FUV heating in photodissociation region (PDR)
- Spherically diverging photoevaporative wind
- Smooth disk-wind transition regions

#### What physics is NOT included?

`PUFFIN` does **not** model:
- Internal photoevaporation from the central star
- External EUV radiation
- Magnetic fields or MHD effects
- Time evolution or dynamical changes
- Dust dynamics (assumes well-mixed gas and dust for temperature structure only)
- Detailed chemical networks (use radiative transfer codes for this)
- Lots of other things!

If these effects are important for your system, you'll need hydrodynamical simulations or specialized codes.

#### How accurate are the density structures?

`PUFFIN` reproduces hydrodynamical simulations with typical factor-of-a-few accuracy across ≥98% of the validated parameter space. Larger deviations can occur:
- Near sharp density gradients in the disk-wind interface
- In regions with strong FUV irradiation gradients
- At the edges of the validated parameter space

For most chemical modeling applications, this accuracy is sufficient given other uncertainties in disk properties.


#### What is the `gamma` parameter and when should I change it?

The `gamma` parameter controls the steepness of the exponential disk taper:

Σ(r) ∝ exp[−(r/r_d)^γ]

By default, `PUFFIN` calculates γ using:

γ = 0.77 × (M_*/M☉)^0.10 × (r_d/AU)^0.78 × (F_FUV/100 G₀)^0.07

where the coefficients were obtained using MCMC fitting to the `FRIED` grid of hydrodynamical simulations.

`PUFFIN` also allows for user-defined values of `gamma`.

<br/>

***

<br/>

### Best Practices & Recommendations

#### What's the recommended workflow for a chemical modeling project?

1. **Define your disk parameters** based on observations or theoretical expectations
2. **Generate the density structure** using PUFFIN 2D model
3. **Validate the structure** by plotting and checking for physical reasonableness
4. **Export to radiative transfer** (e.g., `DALI`, `ProDiMo`) for self-consistent temperature/radiation
5. **Run chemistry** on the full 2D structure with proper temperature/radiation fields
6. **Generate observables** and compare with data

#### How do I cite PUFFIN in my research?

If you use `PUFFIN`, please cite:

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


#### Where can I get help or report bugs?

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

### Advanced Usage

#### Can I modify the source code for my specific application?

Yes! PUFFIN is open-source under the MIT License. You're welcome to:
- Modify prescriptions for your specific needs
- Add new physical components
- Integrate with your own codes

If you make improvements that might benefit the community, please consider contributing them back via a pull request.

#### How do I run PUFFIN in batch mode for parameter surveys?

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


#### How do I interpolate PUFFIN output onto a different grid?

Use `scipy` interpolation tools:

```python
from scipy.interpolate import RegularGridInterpolator

# Define lower resolution grid 200x200)
n_r_new = 200
n_z_new = 200

# Create grid
r_array = np.logspace(np.log10(r_array_highres[0]), np.log10(r_array_highres[-1]), n_r_new)
z_min = 1e-2  # Small offset to avoid log(0)
z_array_log = np.logspace(np.log10(z_min), np.log10(z_array_highres[-1]), n_z_new - 1)
z_array = np.concatenate([[0.0], z_array_log])  # z needs to start at 0

# Create interpolator for high-resolution density
interpolator = RegularGridInterpolator(
    (r_array_highres, z_array_highres), 
    rho_highres.T,  # Transpose to (nr, nz) for interpolator
    method='linear',
    bounds_error=False,
    fill_value=1e-30
)

# Interpolate to DALI grid
rho_new = np.zeros((n_z_new, n_r_new))
for i in range(n_r_new):
    for j in range(n_z_new):
        rho_new[j, i] = interpolator([r_array[i], z_array[j]])
```

#### Can I access the FRIED grid data directly?

Yes! The `FRIED` data is available at https://github.com/thaworth-qmul/FRIEDgrid

