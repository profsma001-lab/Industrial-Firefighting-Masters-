# IF 701 · Fire Dynamics — Quick Reference Card

**Master in Industrial Firefighting · Triune Biblical University Global Extension, USA**

*Teaching reference only — not an operational decision card. No value below establishes safe entry, safe exposure or structural stability.*

---

## 1. Equations

| Quantity | Relationship | Notes |
|---|---|---|
| Heat release rate | Q = ṁ · ΔH_c · χ | ṁ in kg/s, ΔH_c in kJ/kg, Q in kW |
| Fire growth | Q = α t² | α in kW/s², t from assumed growth origin |
| Time to a given HRR | t = √(Q / α) | |
| Ventilation factor | A√H | A opening area (m²), H height (m) |
| Air mass flow | ṁ_air ≈ 0.5 A√H | kg/s |
| Ventilation-limited HRR | Q_max ≈ 1 500 A√H | kW; cross-check ṁ_air × 3.0 MJ/kg |
| Conduction | q = k A ΔT / L | Fourier |
| Convection | q = h A ΔT | Newton |
| Radiation | q″ = ε σ (T₁⁴ − T₂⁴) | σ = 5.67 × 10⁻⁸ W/m²K⁴ |
| Point-source radiation | q″ = χ_r Q / (4π r²) | χ_r typically 0.2–0.4 |
| Distance for a flux | r = √(χ_r Q / (4π q″)) | |
| Flashover (Thomas) | Q_FO ≈ 750 A√H | kW |
| Flashover (McCaffrey) | Q_FO ≈ 610 (h_k A_T A√H)^0.5 | h_k ≈ 0.07 kW/m²K |
| Flame height (Heskestad) | L = 0.235 Q^(2/5) − 1.02 D | m, kW |
| Plume mass flow | ṁ_p = 0.071 Q_c^(1/3)(z − z₀)^(5/3) | Q_c ≈ 0.7 Q |
| Ceiling jet (Alpert) | ΔT = 16.9 Q^(2/3) / H^(5/3) | near plume |
| Water absorbed | q = ṁ_w (c_p ΔT + L_v) | ≈ 2.59 MJ/kg from 20 °C |
| Standard fire (ISO 834) | T = 345 log₁₀(8t + 1) + 20 | °C, t in minutes |
| Characteristic fire diameter | D* = (Q / (ρ∞ c_p T∞ √g))^(2/5) | mesh sensitivity and relevant validation required |

---

## 2. Numbers worth memorising

**Growth classes**

| Class | α (kW/s²) | Time to 1.055 MW |
|---|---|---|
| Slow | 0.00293 | 600 s (10 min) |
| Medium | 0.01172 | 300 s (5 min) |
| Fast | 0.0469 | 150 s (2.5 min) |
| Ultra-fast | 0.1876 | 75 s (1.25 min) |

**Illustrative radiant flux values — not exposure permissions**

| Flux | Effect |
|---|---|
| 2.5 kW/m² | exposure-dependent injury hazard; no safe-work permission |
| 4.7 kW/m² | not a universal skin-exposure limit |
| 12.5 kW/m² | not a universal PPE exposure limit |
| 20 kW/m² | commonly cited flashover-scale flux; not a PPE limit |

**Temperatures**

| Item | Value |
|---|---|
| Incipient layer | 50–150 °C |
| Growth layer | 300–600 °C |
| Flashover criterion | ≈ 500–600 °C layer gas |
| Fully developed gas | 800–1 200 °C |
| Steel strength loss | substantial around 550–600 °C; no universal collapse temperature |
| Smoke layer in a developed fire | 300–700 °C |

**Typical peak heat release rates**

| Item | MW |
|---|---|
| Wastebasket | 0.02–0.1 |
| Armchair | 0.2–0.4 |
| Car | 1.5–5 |
| Retail rack | 5–30 |
| Warehouse | 50–100+ |
| 20 m petrol tank fire | 900–1 500 |

**Oxygen and smoke**

| Parameter | Value |
|---|---|
| Air oxygen | 20.9 % by volume |
| Flaming limit | ≈ 14–15 % O₂ |
| Smouldering limit | ≈ 5–8 % O₂ |
| Enrichment hazard | > 23.5 % O₂ |
| Smoke expansion | ≈ 3 × air volume consumed |
| Tenability visibility | ≥ 10 m (design), 5 m critical |

---

## 3. Assessment reminders

- Interpret smoke signs together with ventilation, fuel, suppression and instrument evidence. Colour alone does not diagnose temperature, toxicity or regime.
- Layer descent and flames in smoke can indicate deterioration, but there is no reliable universal countdown to flashover.
- TICs show apparent surface temperature and contrasts, not reliable hidden gas temperature or structural capacity. Emissivity, reflections and obscuration matter.
- Suspected under-ventilated fire requires trained, coordinated command; do not open or vent solely on the basis of this card.
- Deflection, cracking and falling debris are serious warnings. Collapse can also occur without warning. No universal steel-temperature withdrawal trigger applies.
- Establish incident-specific withdrawal criteria, accountability, communications, escape routes and exclusion zones using applicable procedures.
- Size-up is continuous: building, fuel, smoke, heat, ventilation, life risk, water supply, protection systems and uncertainty. Do not approach to feel heat or infer a safe-entry window from a layer height.

---

## 4. Five sentences to remember

1. Fire is a rate process; the clock, not the flame, governs the outcome.
2. Heat release rate is the master variable.
3. The compartment is part of the combustion system.
4. Ventilation changes can alter burning and flow paths.
5. Models and observations support competent judgement within their limits.
