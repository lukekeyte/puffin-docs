## Quick Start

### 1D Model

```python
import puffin_disk

# Example input values
m_star    = 0.3       # M_sun
r_d       = 100       # AU
sigma_1au = 1000      # g cm^-2
F_FUV     = 1e3       # G_0

# Run PUFFIN
model = puffin_disk.DiskModel1D(m_star, r_d, sigma_1au, F_FUV)                                        
```

The model returns 1D arrays for radius and density. These can then be plotted:

```python
import matplotlib.pyplot as plt

r_array   = model[0]
rho_array = model[1]

plt.loglog(r_array, rho_array)
plt.show()                                       
```

![1D PUFFIN model radial density profile.](/_static/fig_1d_profile.png)


### 2D Model

```python
import puffin_disk

# Example input values
m_star    = 0.3       # M_sun
r_d       = 100       # AU
sigma_1au = 1000      # g cm^-2
F_FUV     = 1e3       # G_0

# Run PUFFIN
model = puffin_disk.DiskModel2D(m_star, r_d, sigma_1au, FFUV_G0, gamma=3.0)                                        
```

The model returns 1D arrays for radius and height, and a 2D density array. These can then be plotted:

```python
import matplotlib.pyplot as plt

r_array   = model[0]
z_array   = model[1]
rho_array = model[2]

plt.contourf(r_array, z_array, np.log10(rho_array), cmap='Spectral_r', levels=np.arange(-20, -11, 0.2), extend='both')
plt.show()                                       
```

![2D PUFFIN model density structure.](/_static/fig_2d_structure.png)


### Tweaking the Model

Both the 1D and 2D PUFFIN models include several optional parameters that allow you to customize the numerical grid and physical behavior. These parameters are passed directly to the `DiskModel1D` and `DiskModel2D` constructors and can be directly adjusted.

The available options are summarized below.

| Parameter | Type | Description |
|---------|------|-------------|
| `n_points` | `int`, optional | Number of grid points used in the radial (and vertical, for 2D) directions. Default is **1000**. Higher resolution (≥1000) is recommended for accurate hydrostatic equilibrium solutions. |
| `gridsize` | `float`, optional | Outer radius of the computational grid in AU. Default is `min(8 * r_d, 800)`. |
| `m_dot` | `float`, optional | Mass-loss rate in M\_☉ yr⁻¹. If `None`, the value is interpolated from the FRIED grid. For 2D models, a factor of 2 is applied to account for geometry. |
| `gamma` | `float`, optional | Exponential cutoff parameter for the surface density profile. If `None`, this is calculated using an internal scaling relation. |
| `p` | `float`, optional | Power-law index controlling the bowl transition associated with the disk radius (`r_d`). Default is **0.2**. |
| `q` | `float`, optional | Power-law index controlling the bowl transition associated with the external FUV field (`F_FUV`). Default is **0.4**. |
| `N_ITER` | `int`, optional | Number of hydrostatic equilibrium iterations. Default is **20**. Increasing this may improve convergence at the cost of runtime. |

In most cases, the default settings provide a good balance between accuracy and performance. Advanced users may wish to increase resolution or iteration count when exploring detailed vertical structure or testing convergence.

