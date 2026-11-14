# IF 701 · Fire Dynamics — Worked Examples and Calculation Workbook

**Master in Industrial Firefighting · Triune Biblical University Global Extension, USA**

**Teaching only: these estimates do not establish safe-entry times, exposure limits or operational fire flows. Use applicable standards, validated methods and competent incident command.**

All calculations in this workbook are engineering estimates. They are intended to replace adjectives with numbers, not to produce legal-grade precision. State your assumptions, carry the units, and always cross-check by a second route.

---

## Constants and data used throughout

| Quantity | Symbol | Value |
|---|---|---|
| Stefan–Boltzmann constant | σ | 5.67 × 10⁻⁸ W/m²·K⁴ |
| Specific heat of water | c_p | 4.18 kJ/kg·K |
| Latent heat of vaporisation of water (100 °C) | L_v | 2 257 kJ/kg |
| Energy released per kg of oxygen consumed | ΔH_O₂ | 13.1 MJ/kg O₂ |
| Effective heat of combustion, wood | ΔH_c | ≈ 16 MJ/kg |
| Effective heat of combustion, petrol | ΔH_c | ≈ 44 MJ/kg |
| Energy released per kg of air consumed | — | ≈ 3.0 MJ/kg air |
| Standard air density at 20 °C | ρ∞ | 1.2 kg/m³ |

**Growth coefficients (t² fire):** slow α = 0.00293, medium α = 0.01172, fast α = 0.0469, ultra-fast α = 0.1876 kW/s².

---

## Example 1 — Fire growth and time to flashover conditions (required example)

**Problem.** A distribution warehouse stores cartons and plastic goods on six-tier racking. On arrival the officer classifies the commodity as **fast growth** (α = 0.0469 kW/s²). Ignition occurred 60 s before the alarm. The building's ventilation, with the doors closed and one roller shutter opened on arrival, limits burning to about **14 MW**.

**Model.** Q = α t².

| Time (s) | Time (min:s) | Q = α t² | Q (MW) |
|---|---|---|---|
| 30 | 0:30 | 0.0469 × 900 | 0.04 |
| 60 | 1:00 | 0.0469 × 3 600 | 0.17 |
| 120 | 2:00 | 0.0469 × 14 400 | 0.68 |
| 146 | 2:26 | 0.0469 × 21 316 | 1.00 |
| 240 | 4:00 | 0.0469 × 57 600 | 2.70 |
| 300 | 5:00 | 0.0469 × 90 000 | 4.22 |
| 450 | 7:30 | 0.0469 × 202 500 | 9.50 |
| 546 | 9:06 | assumed ventilation cap | ≈ 14 |

**Time to a given heat release rate.**

```
t = √(Q / α)
```

- To 1 MW: t = √(1 000 / 0.0469) = 146 s (2 min 26 s)
- To 4 MW: t = √(4 000 / 0.0469) = 292 s (4 min 52 s)
- To 14 MW: t = √(14 000 / 0.0469) = 546 s (9 min 06 s)

**Interpretation of the curve.** Power quadruples when time doubles in this idealised model. The 14 MW cap is an imposed assumption, not a validated warehouse prediction. Commodity description alone does not determine α. Ignition time, ventilation, suppression and spread may invalidate the curve. Do not use it to size an attack or predict a safe entry window.

**Common error.** Using the model beyond its validity. t² describes growth, not the plateau and not decay.

---

## Example 2 — Ventilation-limited heat release rate

**Problem.** A 200 m² workshop has two doorways, each 3.0 m² in area and 2.4 m high. Estimate the maximum heat release rate while these are the only openings.

**Step 1 — ventilation factor.**

```
A = 2 × 3.0 = 6.0 m²
√H = √2.4 = 1.55 m^0.5
A√H = 6.0 × 1.55 = 9.3 m²·m^0.5
```

**Step 2 — air mass flow.**

```
ṁ_air ≈ 0.5 A√H = 0.5 × 9.3 = 4.65 kg/s
```

**Step 3 — heat release rate.**

```
Q_max ≈ 1 500 A√H = 1 500 × 9.3 ≈ 14 000 kW = 14 MW
```

**Step 4 — cross-check by energy per kg of air.**

```
Q = ṁ_air × 3.0 MJ/kg = 4.65 × 3.0 = 13.9 MW  ✓
```

The two expressions share the same assumptions. Their agreement is a consistency check, not independent validation.

**Sensitivity.** If both opening areas remain fixed but both heights change from 2.4 to 4.8 m, the simplified opening factor increases by √2, giving about 19.7 MW. If only one opening changes height, sum each A_i√H_i: 3√2.4 + 3√4.8 ≈ 11.22, or 16.8 MW. These algebraic sensitivities do not model roof ventilation or establish a safe ventilation tactic.

---

## Example 3 — Radiant heat flux and illustrative contours

**Problem.** A rack fire is releasing 10 MW. Assume 30 % of the energy is radiated (χ_r = 0.30). Estimate the radiant flux at a given distance, and the distances corresponding to four illustrative flux levels.

**Model (point source).**

```
q″ = χ_r Q / (4 π r²)
r  = √( χ_r Q / (4 π q″) )
```

With χ_r Q = 0.30 × 10 000 kW = 3 000 kW:

| Threshold q″ | Meaning | Distance r |
|---|---|---|
| 20 kW/m² | flashover-level flux at floor; immediate danger | 3.5 m |
| 12.5 kW/m² | illustrative contour; not an exposure permission | 4.4 m |
| 4.7 kW/m² | illustrative contour; injury depends on duration | 7.1 m |
| 2.5 kW/m² | illustrative contour; not a safe-work limit | 9.8 m |

**Worked line for 12.5 kW/m².**

```
r = √(3 000 / (4π × 12.5)) = √19.1 = 4.4 m
```

**Interpretation and limits.** For a fixed flux, contour distance increases as √Q; doubling Q increases distance by √2. These contours do not establish safe distances. Near a large flame the point-source approximation may be poor, with no guaranteed conservative error. Flame geometry, wind, shielding and hot-layer radiation need appropriate modelling. Exposure duration, PPE, collapse and explosion hazards need separate assessment.

---

## Example 4 — Flashover: how much energy, and how soon

**Problem.** A room 5.0 × 4.0 × 2.4 m has a single door 0.9 m wide × 2.0 m high. Estimate the heat release rate required for flashover and the time to reach it for medium, fast and ultra-fast growth.

**Step 1 — opening and enclosure data.**

```
A_o = 0.9 × 2.0 = 1.8 m²;   √H = √2.0 = 1.414
A√H = 1.8 × 1.414 = 2.55 m²·m^0.5
A_T = 2 × (5 + 4) × 2.4 + (5 × 4) = 43.2 + 20 = 63.2 m²
```

**Step 2 — Thomas correlation.**

```
Q_FO ≈ 750 A√H = 750 × 2.55 ≈ 1 910 kW ≈ 1.9 MW
```

**Step 3 — McCaffrey correlation** (h_k = 0.07 kW/m²·K for a typical lining):

```
Q_FO ≈ 610 (h_k A_T A√H)^0.5
     = 610 (0.07 × 63.2 × 2.55)^0.5
     = 610 × 3.36 ≈ 2 050 kW ≈ 2.1 MW
```

Both give about 2.0 MW; adopt 2.0 MW and state the range 1.9–2.1 MW.

**Step 4 — time to flashover** (t = √(Q/α)):

- Medium α = 0.01172: t = √(2 000 / 0.01172) = **413 s ≈ 6.9 min**
- Fast α = 0.0469: t = √(2 000 / 0.0469) = **206 s ≈ 3.4 min**
- Ultra-fast α = 0.1876: t = √(2 000 / 0.1876) = **103 s ≈ 1.7 min**

**Interpretation.** These are times from an assumed growth origin to an assumed 2 MW threshold. They cannot establish a rescue or entry window. The effective heat-loss parameter and area convention must be stated; 63.2 m² here is a selected walls-plus-ceiling area, not the full six-surface enclosure area (83.2 m² before subtracting openings). A different convention requires consistent recalculation. Correlations have substantial uncertainty.

---

## Example 5 — Water flow: illustrative energy balance

**Problem.** Calculate the ideal water flow that would absorb 14 MW under stated heating and evaporation assumptions. Do not interpret it as an operational fire-flow requirement.

**Step 1 — energy absorbed per kilogram of water.** Heating from 20 °C to 100 °C plus evaporation:

```
q = c_p ΔT + L_v = 4.18 × 80 + 2 257 = 334 + 2 257 ≈ 2 591 kJ/kg ≈ 2.59 MJ/kg
```

**Step 2 — theoretical mass flow.**

```
ṁ = 14 000 kW / 2 591 kJ/kg = 5.4 kg/s
```

**Step 3 — convert to litres per minute** (1 kg water ≈ 1 L):

```
5.4 kg/s × 60 = 324 L/min
```

**Step 4 — apply contact efficiency.** In practice much of the water does not evaporate in the fire zone:

| Contact efficiency | Required flow |
|---|---|
| 100 % (theoretical) | 324 L/min |
| 35 % (assumed utilisation only) | ≈ 925 L/min |
| 18 % (assumed utilisation only) | ≈ 1 800 L/min |

**Interpretation.** These energy-balance values are not attack-flow requirements or hose-line counts. Real performance depends on evaporation, application, access, shielding, fuel hazards, cooling objectives and exposure protection. Use applicable design standards, hazard-specific planning and competent assessment; some industrial materials are incompatible with water.

---

## Example 6 — Smoke layer radiation and preheating

**Problem.** The underside of a hot layer is at 500 °C. Estimate idealised incident flux to a cool target with unit view factor.

```
T = 500 + 273 = 773 K
q″ = ε σ T⁴ = 0.9 × 5.67e-8 × 773⁴ ≈ 18 kW/m²
```

That is within the flashover band (20 kW/m²). At 600 °C (873 K) the flux is 29 kW/m². This is about a 1.6-fold increase in the calculated flux, not a quantified increase in danger. View factor, emissivity and target heat losses matter.

---

## Example 7 — Plume mass flow and ceiling jet temperature (extension)

**Problem.** A 2 MW fire with a 2 m diameter in a 6 m high space. Estimate flame height, plume mass flow at the ceiling, and the ceiling temperature rise near the plume.

**Flame height (Heskestad):**

```
L = 0.235 Q^(2/5) − 1.02 D
Q^(2/5) = 2 000^0.4 = 20.9
L = 0.235 × 20.9 − 1.02 × 2 = 4.91 − 2.04 ≈ 2.9 m
```

**Plume mass flow at height z = 6 m** (virtual origin z₀ ≈ −0.3 m, Q_c = 0.7 Q):

```
ṁ_p = 0.071 Q_c^(1/3) (z − z₀)^(5/3)
    = 0.071 × 11.2 × 6.3^1.667
    ≈ 0.071 × 11.2 × 21.5 ≈ 17 kg/s
```

**Ceiling temperature rise near the plume (Alpert):**

```
ΔT = 16.9 Q^(2/3) / H^(5/3)
Q^(2/3) = 2 000^0.667 = 159
H^(5/3) = 6^1.667 = 19.9
ΔT ≈ 16.9 × 159 / 19.9 ≈ 135 K
```

Sprinkler activation also depends on the temperature rating, response-time index, gas velocity, location and heat losses. This steady correlation alone does not predict activation time or tenability.

---

## Practice set (with answers)

1. **A fire follows fast growth. What is its heat release rate at 4 minutes?**  
   *Answer:* Q = 0.0469 × 240² = 2.7 MW.

2. **A compartment has one opening of 4 m² and 3 m high. Estimate the ventilation-limited HRR.**  
   *Answer:* A√H = 4 × 1.73 = 6.9; Q ≈ 1 500 × 6.9 ≈ 10.4 MW.

3. **A 5 MW fire radiates 30 % of its energy. What is the flux at 6 m?**  
   *Answer:* q″ = 0.3 × 5 000 / (4π × 36) = 3.3 kW/m².

4. **At what distance does a 20 MW fire deliver 12.5 kW/m² (χ_r = 0.3)?**  
   *Answer:* r = √(6 000/(4π × 12.5)) = 6.2 m.

5. **A room reaches 2.5 MW with a medium growth rate. When did it start?**  
   *Answer:* t = √(2 500/0.01172) = 462 s ≈ 7.7 min.

6. **How much water is needed to absorb 8 MW at 30 % efficiency?**  
   *Answer:* 8 000/2 591 = 3.1 kg/s theoretical → 185 L/min → ≈ 620 L/min at 30 %.

7. **A layer at 400 °C: what is the radiant flux to the floor (ε = 0.9)?**  
   *Answer:* T = 673 K; q″ = 0.9 × 5.67e-8 × 673⁴ ≈ 10.4 kW/m².

8. **Estimate the ISO 834 standard fire temperature at 30 minutes.**  
   *Answer:* T = 345 log₁₀(8 × 30 + 1) + 20 ≈ 842 °C (t in minutes) (standard curve, not a real fire).

---

## Marking guidance for calculation questions

| Criterion | Weight |
|---|---|
| Correct model selected and named | 20 % |
| Substitution with units shown | 25 % |
| Arithmetic and unit conversion | 20 % |
| Assumptions stated (χ_r, α, efficiency, geometry) | 20 % |
| Interpretation and cross-check | 15 % |

A numerically correct answer with no stated assumptions should not score above 60 %.
