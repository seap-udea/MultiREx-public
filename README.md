# MultiREx
## Planetary transmission spectra generator

<!-- This are visual tags that you may add to your package at the beginning with useful information on your package --> 
[![version](https://img.shields.io/pypi/v/multirex?color=blue)](https://pypi.org/project/multirex/)
[![downloads](https://img.shields.io/pypi/dw/multirex)](https://pypi.org/project/multirex/)
[![license](https://img.shields.io/pypi/l/multirex)](https://pypi.org/project/multirex/)
[![implementation](https://img.shields.io/pypi/implementation/multirex)](https://pypi.org/project/multirex/)
[![pythonver](https://img.shields.io/pypi/pyversions/multirex)](https://pypi.org/project/multirex/)
<!-- 
[![arXiv](http://img.shields.io/badge/arXiv-2207.08636-orange.svg?style=flat)](http://arxiv.org/abs/2207.08636)
[![ascl](https://img.shields.io/badge/ascl-2205.016-blue.svg?colorB=262255)](https://ascl.net/2205.016)
-->

MultiREx is a Python library designed for generation of synthetic exoplanet transmission spectra. This tool extends the functionalities of the `Taurex` library (see below), reorganizing and enabling the massive generation of spectra and observations with noise.

For the science behind the model please refer to the following paper:

> David S. Duque-Castaño, Jorge I. Zuluaga, and Lauren Flor-Torres (2024), **Machine-assisted classification of potential biosignatures in earth-like exoplanets using low signal-to-noise ratio transmission spectra**, submitted to MNRAS.

<!--
[Astronomy and Computing 40 (2022) 100623](https://www.sciencedirect.com/science/article/pii/S2213133722000476), [arXiv:2207.08636](https://arxiv.org/abs/2207.08636).
-->

## Downloading and Installing `MultiREx` 

`PyLAR` is available at the `Python` package index and can be installed using:

```bash
$ sudo pip install multirex
```
as usual this command will install all dependencies and download some useful data, scripts and constants.

> **NOTE**: If you don't have access to `sudo`, you can install `MultiREx` in your local environmen (usually at `~/.local/`). In that case you need to add to your `PATH` environmental variable the location of the local python installation. Add to `~/.bashrc` the line `export PATH=$HOME/.local/bin:$PATH`

If you are a developer or want to work directly from the package source clone `MultiREx` from the `GitHub` repository:

```bash
$ git clone https://github.com/D4san/MultiREx-public
```

You may install the package from the sources using:

```bash
$ cd MultiREx-public
$ python3 setup.py install
```

## Key features of `MultiREx`

- **Planetary System Assembly**: Facilitates the combination of different planets, stars, and atmospheres to explore various stellar system configurations.

- **Customizable Atmospheres**: Allows the addition and configuration of varied atmospheric compositions for the planets.

- **Synthetic Spectrum Generation**: Produces realistic spectra based on the attributes and conditions of planetary systems.

- **Astronomical Observation Simulation**: Includes `randinstrument` to simulate spectral observations with noise levels determined by the signal-to-noise ratio (SNR).

- **Multiverse analysis**: Automates the generation of multiple spectra that randomly vary in specific parameters, providing a wide range of results for analysis.

## Quickstart

To start using `MultiREx` you must import the package:

```python
import multirex as mrex
```

To start with, we need to provide to `MultiREx` the properties of the three components of any transmission model: A star, a planet and a planetary atmosphere.


```python
star=mrex.Star(temperature=5777,radius=1,mass=1)
```

Radius and mass are in solar units.

The properties of the planet
```python
planet=mrex.Planet(radius=1,mass=1)
```

Radius and mass are in units of Earth properties. 

Now it's time to give the planet an atmosphere. This is a basic example of an N$_2$ atmosphere having 100 ppm of CO2 and 1 ppm of CH4:

```python
atmosphere=mrex.Atmosphere(
    temperature=288, # in K
    base_pressure=1e5, # in Pa
    top_pressure=1, # in Pa
    fill_gas="N2", # the gas that fills the atmosphere
    composition=dict(
        CO2=-4, # This is the log10(mix-ratio)
        CH4=-6,
    )
)
planet.set_atmosphere(atmosphere)
```

Now we can ensamble the system:

```python
system=mrex.System(star=star,planet=planet,sma=1)
```

Semimajor axis of the planeta (`sma`) is given in au (astronomical units).

Now, we are ready to see some spectrum. For this purpose we need to create a transmission model, i.e. a model that allows us to generate transmission spectra:

```python
system.make_tm()
```

Once initialized, we may plot the transmission spectra over a given grid of wavelengths:

```python
wns = mrex.Physics.wavenumber_grid(wl_min=0.6,wl_max=10,resolution=1000)
fig, ax = system.plot_contributions(wns,xscale='log')
```

<p align="center"><img src="https://github.com/D4san/MultiREx-public/blob/main/examples/resources/contributions-transmission-spectrum.png?raw=true" alt="Contributions in transmission spectra"/></p>

All of these functionalities are also available in `Taurex`. However, the interface to `MultiREx` is way more intuitive, but, more importantly, it is also best suited for the real superpower of the package: the capaciy to create large ensamble of random systems. 

For creating a random system we can use the command:

```python
system=mrex.System(
    star=mrex.Star(
        temperature=(4000,6000),
        radius=(0.5,1.5),
        mass=(0.8,1.2),
    ),
    planet=mrex.Planet(
        radius=(0.5,1.5),
        mass=(0.8,1.2),
        atmosphere=mrex.Atmosphere(
            temperature=(290,310), # in K
            base_pressure=(1e5,10e5), # in Pa
            top_pressure=(1,10), # in Pa
            fill_gas="N2", # the gas that fills the atmosphere
            composition=dict(
                CO2=(-5,-4), # This is the log10(mix-ratio)
                CH4=(-6,-5),
            )
        )
    ),
    sma=(0.5,1)
)
```

Here we assume that all key parameters are physically and statistically independent.

Using this template we may generate thousands of spectra that can be used for instance for training machine learning algorithms. In the figure below we show the resulting synthetic spectra.

<p align="center"><img src="https://github.com/D4san/MultiREx-public/blob/main/examples/resources/synthetic-transmission-spectra.png?raw=true" alt="Synthetic transmission spectra"/></p>

For a more in depth explanation of these commands are available in the [quick start guide](https://github.com/D4san/MultiREx-public/blob/main/examples/multirex-quickstart.ipynb).

## Further examples

For usage tutorials, access the `examples` folder. Specifically, this folder contains a subfolder named `examples/papers`, which demonstrates how MultiREx can be used in research that utilizes the generated data to train Machine Learning models.

### A note about `Taurex`

MultiREx is built on the spectral calculation capabilities and the basic structure of [Taurex](https://taurex3-public.readthedocs.io/en/latest/index.html). If you use `MultiREx` in your research or publications, please also cite Taurex as follows:

> A. F. Al-Refaie, Q. Changeat, I.P. Waldmann, and G. Tinetti **TauREx III: A fast, dynamic, and extendable framework for retrievals**,  arXiv e-prints." arXiv preprint arXiv:1912.07759 (2019).

It is necessary to load the opacities or cross-sections of the molecules used in the formats that Taurex utilizes, which can be obtained from:
- [ExoMol](https://www.exomol.com/data/search/)
- [ExoTransmit](https://github.com/elizakempton/Exo_Transmit/tree/master/Opac)

We have pre-downloaded some of these molecules, and others can be downloaded using the command `multirex.Util.get_gases()`

## What's new

For a detailed list of the newest characteristics of the code see the file [What's new](https://github.com/D4san/MultiREx-public/blob/master/WHATSNEW.md).

------------

This package has been designed and written by David Duque-Castaño and Jorge I. Zuluaga (C) 2024
