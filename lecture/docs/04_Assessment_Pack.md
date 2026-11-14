# IF 701 · Fire Dynamics — Postgraduate Assessment Pack

**Master in Industrial Firefighting · Triune Biblical University Global Extension, USA**

The assessment has three components: a written examination (essay and calculation), a practical prediction exercise in the simulation laboratory, and a case-study analysis. Weighting: written 50 %, practical 30 %, case study 20 %.

Candidates are graded on **mechanism, quantification and stated uncertainty**. Descriptive answers that do not engage with the physics cannot exceed a pass mark.

---

## Part A — Essay and calculation questions (70 marks)

**A1 (10 marks).** Derive the conditions for flashover using both the Thomas and the McCaffrey correlations. Compare the assumptions each makes about heat loss from the compartment, and explain why they converge for a typical small room but diverge for a large, well-insulated space.

**A2 (10 marks).** A 300 m² hall has two openings, each 8 m² in area and 3 m high. Estimate the ventilation-limited heat release rate. State every assumption, and discuss the uncertainty in your answer if the openings are partially blocked by falling debris.

**A3 (8 marks).** Explain why a fuel-controlled fire and a ventilation-controlled fire require different attack strategies. Support your answer with observations a crew can make at the doorway within the first sixty seconds.

**A4 (10 marks).** For a 6 MW fire with an assumed radiative fraction of 30%, calculate point-source flux contour distances at 4.7 and 12.5 kW/m². Explain why neither contour establishes a safe exposure or minimum operational stand-off distance. State the limitations of the model.

**A5 (10 marks).** Critically evaluate the t² fire growth model for a high-piled storage fire. Where is it useful, where does it fail, and what would you use instead once the fire becomes ventilation-controlled?

**A6 (8 marks).** Using one case study from the lecture, identify the precise moment at which fire dynamics knowledge would have changed the operational outcome, and justify your choice with quantitative reasoning.

**A7 (8 marks).** "Ventilation is the most powerful tactical variable in industrial firefighting." Discuss, with reference to the heat release rate, the neutral plane and the risk of backdraft.

**A8 (6 marks).** Explain how a combustible sandwich panel defeats conventional compartmentation, and describe the evidence you would look for on arrival at a cold-store fire.

---

## Part B — Practical prediction exercise (30 marks)

Candidates are given a scenario in the simulator (or a written data set) and 20 minutes to prepare a prediction brief. The brief must contain:

1. A classified growth rate (α) with justification from the fuel description.
2. A heat release rate curve from ignition to 15 minutes, annotated with the ventilation limit and the moment of transition.
3. Predicted layer depth at 3, 6 and 9 minutes, and the corresponding neutral plane height at the main opening.
4. Predicted tenability at working level: temperature, visibility and CO.
5. Three tactical trigger points, each expressed as an observable threshold and an action.
6. A statement of the two largest uncertainties in the prediction and how they would be resolved on scene.

| Criterion | Marks |
|---|---|
| Correct physical model and α classification | 6 |
| Quantitative prediction with units | 8 |
| Interpretation of the curve (plateau, transition) | 6 |
| Trigger points that are observable and actionable | 6 |
| Honest treatment of uncertainty | 4 |

---

## Part C — Case study analysis (20 marks)

Using the nine-point structured template in the case-study document, analyse one incident. Maximum 2 000 words. Diagrams are encouraged and are not counted in the word limit. Marks are awarded for mechanism and for the quality of the "decision points" analysis.

---

## Short-answer bank (for revision or viva)

1. Define fire, combustion and flame, and distinguish smouldering from flaming combustion.
2. State the four elements of the fire tetrahedron and give one extinguishing method that removes each.
3. Why do solids and liquids burn as gases? What is pyrolysis?
4. Write Fourier's law and explain each term. Give two industrial fire spread paths that depend on conduction.
5. Write the Stefan–Boltzmann law. Why is the fourth power important for firefighting?
6. Define flash point, fire point and autoignition temperature. Give one industrial fuel for each extreme.
7. What is the difference between a flash fire and a vapour cloud explosion?
8. Sketch the four stages of compartment fire development and label the transition points.
9. What is the heat release rate, and why is it called the master variable?
10. State the t² equation and the four standard α values with their time to 1 MW.
11. What are the limitations of the t² model?
12. Define the ventilation factor and state the two correlations that use it.
13. Explain the two-layer model and the neutral plane.
14. What are the three standard criteria for flashover?
15. Describe the physical sequence of a backdraft and the four warning signs.
16. What is a boilover, and how does it differ from a slopover?
17. Define a BLEVE and explain the role of flame impingement on the vapour space.
18. What is a dust deflagration, and why are secondary explosions often worse than the first?
19. Explain the difference between reaction-to-fire classification and fire resistance.
20. Why is grid resolution important in a CFD fire model? What is D*?
21. What is the purpose of a zone model such as CFAST?
22. Give three reasons why a model must never override a fireground observation.
23. Estimate the water flow required to absorb 10 MW at 35 % efficiency (show working).
24. What tenability limits would you use for visibility, temperature and CO?
25. Describe the size-up sequence and the question each observation answers.

---

## Model answer guidance (selected)

**A1.** Thomas: Q_FO ≈ 750 A√H, derived from the observation that flashover occurs when the energy release per unit opening area exceeds a threshold; it implicitly assumes heat losses scale with the ventilation factor. McCaffrey: Q_FO ≈ 610 (h_k A_T A√H)^0.5, which explicitly includes the total enclosure area and an effective heat transfer coefficient, so it responds to insulation. For a small room the two agree within about 10 % because A_T/A√H is of order 20–25. For a large, well-insulated space, h_k falls and A_T rises, and the McCaffrey form predicts a lower flashover HRR — correctly reflecting that less energy escapes through the linings. Credit should be given for discussing that both are correlations fitted to compartment fire data, both assume a single opening and a well-mixed upper layer, and both carry uncertainty of the order of ±30–50 %.

**A2.** A = 16 m², H = 3 m, √H = 1.73, A√H = 27.7; Q ≈ 1 500 × 27.7 ≈ 41.5 MW. Assumptions: two openings act as a single ventilation source; no wind; fully developed burning; typical fuel with ≈3 MJ per kg of air; no mechanical ventilation. If debris blocks half the area, A√H halves, and Q falls to about 21 MW — but the *fire* does not obey instantly: the compartment will become under-ventilated, CO production will rise, and the hazard of a backdraft or smoke explosion increases even as the heat release rate falls. This is the point most candidates miss.

**A4.** Radiated power = 1 800 kW. Using r = √[1 800/(4πq″)] gives 5.52 m at 4.7 kW/m² and 3.39 m at 12.5 kW/m². These are mathematical contours, not exposure permissions or safe stand-off distances. The model neglects extended flame geometry, hot-layer radiation, shielding and wind; near-field error is not reliably one-sided. Duration, PPE, collapse and explosion hazards require separate assessment. Do not accept a different numerical distance without a stated, justified alternative model.

**A5.** A good answer will note: t² fits the early growth of a free-burning fuel package; it fits high-piled storage poorly once the fire involves multiple rack faces and a deep hot layer, because the burning rate becomes limited by air entering the aisle and by radiation from the layer, not by the fuel surface. It cannot represent a plateau, a ventilation-induced surge, or decay. Better tools: the ventilation factor for the maximum, a McCaffrey-type plume/rack correlation for flame height, and a zone or CFD model for the layer.

**A7.** A good answer will structure the argument: ventilation sets the maximum heat release rate (1 500 A√H); it controls the neutral plane and therefore the working environment; it determines whether the fire is efficient (low CO) or fuel-rich (high CO, backdraft potential); and it is the variable most under the incident commander's control, through doors, windows, roof vents and PPV. Counter-arguments should acknowledge that ventilation cannot exceed the fuel's capability, and that uncoordinated ventilation is a hazard rather than a control.

---

## Marking rubric (generic)

| Band | Descriptor |
|---|---|
| Distinction (70+) | Correct mechanism, quantified with stated assumptions, uncertainty discussed, tactical implications drawn. |
| Merit (60–69) | Correct mechanism, sound calculation with minor errors, limited discussion of uncertainty. |
| Pass (50–59) | Describes the phenomenon but does not quantify, or quantifies without interpreting. |
| Fail (<50) | Confuses mechanisms (e.g., flashover with backdraft), or presents numbers without units or assumptions. |
