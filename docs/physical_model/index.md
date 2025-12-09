# Physical Model

The physical model in `PUFFIN` uses a parametric framework to efficiently generate density structures of externally irradiated protoplanetary disks with photoevaporative winds. Rather than solving full radiation-hydrodynamic equations, the model constructs physically motivated density profiles by combining three components: the disk interior, a smooth transition region, and a spherically diverging photoevaporative wind.

The approach is based on extensive calibration against the FRIED grid of hydrodynamical simulations ([Haworth et al. 2018](https://ui.adsabs.harvard.edu/abs/2018MNRAS.481..452H/abstract), [2023](https://ui.adsabs.harvard.edu/abs/2023MNRAS.526.4315H/abstract)) and reproduces key structural features with typical factor-of-two accuracy while reducing computational time from weeks/months to seconds/minutes.

<br/>

## 1D Model Formulation

The one-dimensional model extends from $r = 0$ to $r = R_{\rm out}$ and consists of three distinct regions that are smoothly connected through a "maximum density" prescription.

### Disk Interior

The disk surface density follows a power-law profile with an exponential taper beyond the nominal disk edge:

$$
\Sigma(r) = \Sigma_{1\,\rm au} \left(\frac{r}{\rm au}\right)^{-1} \exp\left[-\left(\frac{r}{r_d}\right)^\gamma\right]
$$

where $\Sigma_{1\,\rm au}$ is the surface density at 1 au, $r_d$ is the disk outer radius, and the taper steepness $\gamma$ scales with physical parameters:

$$
\gamma = A \left(\frac{M_*}{M_\odot}\right)^\alpha \left(\frac{r_d}{\rm au}\right)^\beta \left(\frac{F_{\rm FUV}}{100\,G_0}\right)^\varepsilon
$$

where $A = 0.77$, $\alpha = 0.10$, $\beta = 0.78$, and $\varepsilon = 0.07$ are empirically calibrated parameters. This scaling ensures that more massive stars (which bind material more tightly) and stronger FUV fields produce steeper tapers.

The midplane temperature assumes a power-law dependence:

$$
T_{\rm mid} = T_{1\,\rm au} \left(\frac{r}{\rm au}\right)^{-1/2}
$$

where $T_{1\,\rm au} = 150 \cdot (M_*/M_\odot)^{1/4}$ K. The midplane density is derived from hydrostatic equilibrium:

$$
\rho_{\rm disk}(r) = \frac{1}{\sqrt{2\pi}} \frac{\Sigma(r)}{h(r)}
$$

where $h = c_s/\Omega$ is the pressure scale height, $c_s$ is the sound speed, and $\Omega = \sqrt{GM_*/r^3}$ is the Keplerian angular velocity.

### Spherically Diverging Wind

For $r \geq r_d$, a spherically diverging wind component is computed from the mass-loss rate:

$$
\rho_{\rm wind}(r) = \frac{\dot{M}}{4\pi r^2 \mathcal{F} v_R}
$$

where $\dot{M}$ is the mass-loss rate (user-specified or interpolated from FRIED), $\mathcal{F} = h_d/\sqrt{h_d^2 + r_d^2}$ represents the solid angle fraction subtended by the disk outer edge, and $v_R \approx c_{s,\rm wind}$ is the flow velocity.

The wind temperature scales with external FUV field strength:

$$
T_{\rm PDR} = T_0 \left(\frac{F_{\rm FUV}}{1000\,G_0}\right)^{0.2}
$$

with $T_0 = 200$ K, bounded between 10 K and 3000 K. This shallower scaling prioritizes matching temperatures at the shielded wind base rather than the directly irradiated surface.

### Transition Region

For weaker external FUV fields ($\lesssim 1000$ G₀), hydrodynamical models show an extended plateau region where density decreases more gradually than the exponential taper alone would predict. This is captured through an interpolation prescription:

$$
\rho_{\rm plateau}(r) = \rho_{\rm disk}(r_d) \left(\frac{\rho_{\rm wind}(r)}{\rho_{\rm disk}(r_d)}\right)^{f(r)}
$$

where the blending function varies smoothly in logarithmic space:

$$
f(r) = \frac{1 - \exp[-\lambda \log_{10}(r/r_d)]}{1 - \exp(-\lambda)}
$$

The parameter $\lambda$ controls the transition rate:

$$
\lambda = r_d^p + \left(\frac{F_{\rm FUV}}{1000\,G_0}\right)^q
$$

with $p = 0.2$ and $q = 0.4$. At weak fields, $\lambda$ is small (gradual transition); at strong fields, $\lambda$ is large (sharp transition).

### Final Density Profile

The density at each radius is determined by selecting the maximum value:

$$
\rho(r) = \begin{cases}
\rho_{\rm disk}(r) & \text{if } r < r_d \\
\max[\rho_{\rm disk}(r), \rho_{\rm wind}(r), \rho_{\rm plateau}(r)] & \text{if } r \geq r_d
\end{cases}
$$

This ensures physically consistent behavior: the disk dominates in the interior, the taper and plateau govern the transition, and the wind describes the outer spherical flow.

<br/>

***

<br/>

## 2D Model Extension

The two-dimensional model extends the 1D framework with full vertical structure, realistic temperature profiles, and a geometrically motivated wind implementation.

### Disk Component with Hydrostatic Equilibrium

The disk initially assumes a Gaussian vertical profile:

$$
\rho_{\rm disk} = \rho_0 \exp\left(-z^2/2h^2\right)
$$

where $z$ is height above the midplane and $\rho_0 = \Sigma(r)/(\sqrt{2\pi}h)$ is the midplane density.

However, under strong external irradiation, this isothermal approximation breaks down. The model solves for hydrostatic equilibrium iteratively by:

1. **Computing the FUV radiation field**: The total FUV field combines stellar and external contributions. The optical depth is calculated along three paths (vertically downward, radially inward, radially outward) and the minimum value is taken. Different opacities are used for the dust-depleted wind ($\sigma_{\rm FUV} = 2.7 \times 10^{-23}$ cm², $\mu = 1.3$) versus the dust-rich disk ($\sigma_{\rm FUV} = 8 \times 10^{-22}$ cm², $\mu = 2.3$).

2. **Establishing the temperature structure**: The disk surface is defined at $\tau_{\rm FUV} = 1$. Above this surface, the gas is directly heated to $T_{\rm PDR}$. Below the surface, temperature transitions smoothly to the midplane value:

$$
T = T_{\rm mid} + (T_{\rm PDR} - T_{\rm mid}) \times \beta
$$

where the transition function is:

$$
\beta = \frac{1}{2}\left[1 + \tanh\left(k\left(\frac{z}{z_{\rm surface}} - \frac{1}{2}\right)\right)\right]
$$

3. **Solving hydrostatic equilibrium**: The vertical density gradient is governed by:

$$
\frac{d\ln\rho}{dz} = -\frac{\Omega^2 z}{c_s^2} - \frac{1}{T}\frac{dT}{dz}
$$

This is integrated upward from the midplane, then renormalized to conserve the surface density $\Sigma(r)$.

These three steps are iterated until the density structure converges (typically ~20 iterations).

### Spherically Diverging Wind

The wind diverges spherically from a focal point located at $r_{\rm focal} \approx 0.5 r_d$ on the midplane, motivated by streamline analysis of hydrodynamical simulations:

$$
\rho_{\rm wind}(d) = \frac{\dot{M}}{4\pi d^2 v_{\rm gas}}
$$

where $d$ is the distance from the focal point and $v_{\rm gas} = c_s$ (Equation from 1D model). The mass-loss rate can be user-specified or interpolated from FRIED with a factor-of-2 scaling to account for systematic differences between 1D and 2D simulations.

At small radii ($r \lesssim r_d$), the wind is suppressed using a smooth tapering function:

$$
f_{\rm taper}(r,z) = 1 - \frac{\cos[\pi(r/r_{\rm edge})^2]}{2}
$$

where the tapering region extends to $r_{\rm edge}(z) = r_d$ for $z \geq r_{\rm focal}$ and $r_{\rm edge} = r_d \cdot (z/r_{\rm focal})$ for $z < r_{\rm focal}$. This prevents unphysical wind densities in gravitationally bound regions near the midplane.

### Disk-Wind Transition ("Halo")

In 2D, external irradiation produces an extended "halo-like" disk atmosphere that naturally bridges the dense interior and tenuous wind. This is implemented by:

1. Defining the disk surface as the $\tau_{\rm FUV} = 1$ contour
2. Extending normal to this surface into the wind
3. Applying the 1D transition prescription (exponential taper + plateau) along these normals

This creates a smooth density bridge where material gradually transitions from the bound disk to the expanding wind, following the geometry of the irradiated disk surface.

### Final Density Structure

The density at any point $(r, z)$ is determined by taking the maximum of all three components:

$$
\rho(r,z) = \max[\rho_{\rm disk}(r,z), \rho_{\rm halo}(r,z), \rho_{\rm wind}(r,z)]
$$

This allows the physically relevant prescription to naturally emerge at each location depending on local conditions.

<br/>

***

<br/>

## Key Physical Parameters

### Model Inputs

- **$M_*$**: Stellar mass (0.3–3.0 $M_\odot$ validated range)
- **$r_d$**: Disk outer radius (20–150 au validated range)
- **$\Sigma_{1\,\rm au}$**: Surface density normalization (10¹–10⁴ g cm⁻² validated range)
- **$F_{\rm FUV}$**: External FUV field strength (10²–10⁵ $G_0$ validated range)
- **$\dot{M}$**: Mass-loss rate (optional; interpolated from FRIED if not provided)

### Tunable Parameters

- **$\gamma$**: Taper steepness (default: empirical scaling; can be set manually)
- **$k$**: Vertical temperature gradient steepness (default: standard value)
- **$r_{\rm focal}$**: Wind focal point location (default: 0.5 $r_d$)

### Physical Constants

- **$G_0 = 1.6 \times 10^{-3}$ erg cm⁻² s⁻¹**: Habing unit for FUV field strength
- **$N_{\rm ss} = 8 \times 10^{14}$ cm⁻²**: Surface site density (used in some contexts)
- **$\mu_{\rm wind} = 1.3$**: Mean molecular weight in dust-depleted wind
- **$\mu_{\rm disk} = 2.3$**: Mean molecular weight in disk

<br/>

***

<br/>

## Model Validation

The parametric prescriptions have been calibrated against:

- **600+ 1D hydrodynamical models** from the FRIED grid spanning the full parameter space
- **4 representative 2D simulations** at different FUV field strengths (100–5000 $G_0$)

Typical agreement is within a factor of ~2 across ≥98% of the validated parameter space, with larger deviations confined to localized regions near sharp density gradients in the disk-wind interface.

<br/>

***

<br/>

## Important Notes

**Temperature and Radiation Fields**: The temperature profiles and FUV fields computed during model construction are used *only* to establish the density structure through hydrostatic equilibrium. These should **never** be used directly for chemical modeling or synthetic observations. Instead, the density structures should serve as inputs to dedicated radiative transfer codes (e.g., DALI, RADMC-3D) that compute self-consistent temperature and radiation fields.

**Model Scope**: PUFFIN focuses exclusively on FUV-driven external photoevaporation. The model does not include:
- External EUV radiation
- Internal photoevaporation from the central star
- Magnetic fields or MHD effects
- Dynamical evolution or time-dependent effects

**Validated Range**: Best results are obtained within the validated parameter ranges. Extrapolation beyond these ranges should be done cautiously with careful checking of output structures.