
# coding: utf-8

# Importar MultiREx

# In[1]:


import multirex as mrex

print(mrex.version)


# In[2]:


mrex.xsec_path


# In[3]:


# Crear un planeta con propiedades específicas
trappis1e = mrex.Planet(radius=0.920, mass=0.692)
trappis1e.set_atmosphere(mrex.Atmosphere(temperature=289,
                                         base_pressure=1e5,
                                         top_pressure=1e-3,
                                         composition={"H2O": -2, "CO2": -1,
                                                      "CH4": (-10, -1), "O3": (-10, -1)},
                                         fill_gas="N2"))


# In[4]:



# Configurar una estrella
trappist1 = mrex.Star(temperature=2566, radius=0.1192, mass=0.1192)


# In[5]:


# Crear un sistema que incluye el planeta y la estrella
systemtrappist1 = mrex.System(trappis1e, 
                              trappist1,
                              sma=0.02925, 
                              )


# In[6]:


systemtrappist1.get_params()

# In[8]:


systemtrappist1.make_transmission_model()
# In[7]:


wn_grid=mrex.wavenumber_grid(0.5,6,100)


# Uso de explore_multiverse para generar datos
spec, obs = systemtrappist1.explore_multiverse(wn_grid=wn_grid,
                                   snr=3,
                                   n_iter=3,
                                   labels=[["O3"],["CH4"]],
                                   header=True, 
                                   n_observations=2,
                                   spectra=True,
                                   observations=True)




# In[10]:


systemtrappist1.plot_full_spectrum(wn_grid,title="Trappist-1 e")


# In[12]:

print("Spectra Dataframe")
print(spec.describe())
print("Observations Dataframe")
print(obs.describe())


