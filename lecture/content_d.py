# -*- coding: utf-8 -*-
"""IF 701 - Fire Dynamics. Part D: calculations, case studies, demonstration, tools, assessment."""

S = []

def seg(**kw):
    S.append(kw)

# ----------------------------------------------------------------------------- 18 CALCULATIONS
seg(id="calc0", sec="18", kicker="18 · PRACTICAL CALCULATIONS", title="Five Calculations Every Officer Should Be Able to Do",
    sub="Order-of-magnitude engineering, done in your head or on a pad",
    layout="outcomes",
    visual=None,
    bullets=["1  Estimate fire growth and time to a given heat release rate (t² model).",
             "2  Estimate the maximum heat release rate set by ventilation (1 500 A√H).",
             "3  Estimate radiant flux contours — not safe stand-off distances.",
             "4  Estimate the heat release rate needed for flashover, and the time to reach it.",
             "5  Estimate the water flow required to absorb that energy.",
             "",
             "The purpose is not precision. It is to replace adjectives with numbers."],
    narr=('We now turn theory into arithmetic. Five calculations illustrate growth with the time-squared model, ventilation-limited heat release, radiant heat flux at a distance, flashover correlations and the energy that water can absorb. These are simplified planning exercises, not fireground forecasts with guaranteed accuracy. Their value is to make assumptions and orders of magnitude explicit. Their limitations matter just as much as their answers. None establishes a safe entry time, a safe stand-off distance or an adequate operational water supply. Use them alongside validated design methods, site information and competent incident command, never as a replacement for those safeguards.'),
    note="Set expectations: engineering estimates, ±30-50%.")

seg(id="calc1", sec="18", kicker="18 · WORKED EXAMPLE 1", title="Fire Growth: From Ignition to Flashover Conditions",
    sub="A rack fire in a distribution warehouse, fast growth, α = 0.0469 kW/s²",
    layout="worked",
    visual=("worked_t2", {}),
    bullets=["Q = α t²",
             "t = 60 s → Q = 169 kW",
             "t = 120 s → Q = 675 kW",
             "t = 146 s → Q = 1.0 MW",
             "t = 300 s → Q = 4.2 MW",
             "t = 450 s → Q = 9.5 MW",
             "Ventilation limit ≈ 14 MW at t ≈ 9.1 min"],
    narr=('Our first example estimates growth and interprets the curve. For an illustrative fast-growing warehouse fire, alpha equals zero point zero four six nine kilowatts per second squared. At sixty seconds, heat release is about one hundred and seventy kilowatts. At two minutes, six hundred and seventy-five kilowatts. At about two minutes twenty-six, one megawatt. At five minutes, four point two megawatts, and at seven and a half minutes, nine and a half megawatts. In this idealised model, power quadruples when time doubles. If we impose an illustrative ventilation limit of fourteen megawatts, the curve reaches that value at about nine point one minutes. A flat cap is only a modelling simplification. Real fires can fluctuate, spread, burn outside openings or change when ventilation changes; this curve is not a prediction of the incident clock.'),
    note="This is the core worked example. Walk the curve point by point.")

seg(id="calc2", sec="18", kicker="18 · WORKED EXAMPLE 2", title="Ventilation-Limited Burning",
    sub="A 200 m² workshop with two doorways, each 3 m² and 2.4 m high",
    layout="worked",
    visual=("worked_vent", {}),
    bullets=["A = 2 × 3 = 6 m², H = 2.4 m",
             "A√H = 6 × 1.55 = 9.3 m²·m^0.5",
             "Air flow ≈ 0.5 × 9.3 = 4.65 kg/s",
             "Q_max ≈ 1 500 × 9.3 ≈ 14 MW",
             "Check: 4.65 kg/s × 3.0 MJ/kg ≈ 14 MW ✓"],
    narr=('Second example: a two hundred square metre workshop with two doorways, each three square metres in area and two point four metres high. For equal-height openings, the total area is six square metres, and the square root of the height is one point five five. The opening factor is therefore about nine point three. The simplified air-flow correlation gives zero point five times that, or four point six five kilograms per second. Using about three megajoules per kilogram of air gives roughly fourteen megawatts. The shortcut, fifteen hundred times the opening factor, gives the same result because it uses the same underlying assumptions; this is a consistency check, not independent validation. The estimate applies to a simplified naturally ventilated compartment. Wind, additional openings and external burning can change the result. Opening a shutter can increase the potential burning rate, so ventilation changes require coordinated control.'),
    note="Cross-check is a professional habit worth teaching explicitly.")

seg(id="calc3", sec="18", kicker="18 · WORKED EXAMPLE 3", title="Radiant Heat: Illustrative Flux Contours",
    sub="A 10 MW rack fire, 30 % of energy radiated",
    layout="worked",
    visual=("worked_radiation", {}),
    bullets=["q″ = χ_r Q / (4π r²)",
             "r = √(χ_r Q / 4π q″)",
             "20 kW/m² → 3.5 m",
             "12.5 kW/m² → 4.4 m",
             "4.7 kW/m² → 7.1 m",
             "2.5 kW/m² → 9.8 m"],
    narr=('Third example: radiation at a distance. A ten megawatt fire is assumed to radiate thirty per cent of its heat. In a point-source approximation, flux equals radiated power divided by four pi times distance squared. The calculated distances are about three point five metres for twenty kilowatts per square metre, four point four metres for twelve point five, seven point one metres for four point seven, and nine point eight metres for two point five. These are mathematical contours, not safe stand-off distances or exposure permissions. Injury depends on duration, clothing and other conditions. Near a large flame, the point-source approximation can be poor; flame geometry, smoke, shielding and wind also matter. Doubling heat release increases a given contour distance by the square root of two. Operational exclusion zones must additionally account for collapse, explosion and changing fire conditions.'),
    note="Emphasise inverse-square and the square-root consequence for standoff.")

seg(id="calc4", sec="18", kicker="18 · WORKED EXAMPLE 4", title="Flashover: How Much Energy, and How Soon?",
    sub="A 5 × 4 × 2.4 m room with a single 0.9 × 2.0 m door",
    layout="worked",
    visual=("worked_flashover", {}),
    bullets=["A = 1.8 m², H = 2.0 m → A√H = 2.55",
             "Thomas: Q_FO = 750 × 2.55 ≈ 1.9 MW",
             "McCaffrey: 610 (h_k A_T A√H)^0.5 ≈ 2.0 MW",
             "Medium growth: t = √(2 000/0.0117) ≈ 6.9 min",
             "Fast growth: t ≈ 3.4 min",
             "Ultra-fast: t ≈ 1.7 min"],
    narr=('Fourth example: flashover correlations for a room five by four metres, two point four metres high, with one door nine hundred millimetres wide and two metres high. The opening area is one point eight square metres and the opening factor is about two point five five. The simplified Thomas expression gives about one point nine megawatts. Using the stated effective heat-loss parameter, McCaffrey gives about two megawatts. That apparent agreement is specific to these assumptions, not a guarantee of accuracy. If we use two megawatts as an illustrative threshold, medium growth reaches it at about four hundred and thirteen seconds, or seven minutes; fast growth at about three and a half minutes; and ultra-fast growth at about one point seven minutes. These times start from the assumed growth origin. Actual ignition, fuel arrangement, ventilation, linings and suppression can change the outcome substantially. This exercise cannot provide a safe rescue or entry window.'),
    note="The practical conclusion: time to flashover is set by growth rate and ventilation, both assessable on arrival.")

seg(id="calc5", sec="18", kicker="18 · WORKED EXAMPLE 5", title="Water Flow: An Illustrative Energy Balance",
    sub="How much water absorbs 14 MW?",
    layout="worked",
    visual=("worked_water", {}),
    bullets=["Water: 4.18 kJ/kg·K, latent heat 2 257 kJ/kg",
             "20 → 100 °C plus evaporation ≈ 2.6 MJ per kg",
             "14 MW ÷ 2.6 MJ/kg ≈ 5.4 kg/s ≈ 324 L/min (theoretical)",
             "At an assumed 35 % utilisation ≈ 926 L/min",
             "Not an operational fire-flow or attack-sizing method.",
             "Use hazard-specific standards and competent assessment."],
    narr=('Fifth example: an energy balance for water. Heating one kilogram of water from twenty to a hundred degrees takes about three hundred and thirty-four kilojoules; evaporation adds two thousand two hundred and fifty-seven. Together that is about two point five nine megajoules per kilogram. Dividing fourteen megawatts by that value gives about five point four kilograms per second, or three hundred and twenty-four litres per minute, if every kilogram is fully heated and evaporated. With an assumed effective utilisation of thirty-five per cent, the arithmetic becomes about nine hundred and twenty-six litres per minute. Neither number is an operational fire-flow requirement. Real application involves incomplete evaporation, access, shielding, nozzle performance, cooling objectives and exposure protection. Water can also be unsuitable for some industrial hazards. Determine supplies and tactics using applicable standards, hazard-specific planning and competent assessment, not this energy balance alone.'),
    note="This calculation is the bridge from fire dynamics to logistics.")

# ----------------------------------------------------------------------------- 19 CASE STUDIES
seg(id="case0", sec="19", kicker="19 · INDUSTRIAL CASE STUDIES", title="Three Fires That Teach Fire Dynamics",
    sub="Dust, liquid storage and combustible cladding",
    layout="case_intro",
    visual=("case_cards", {}),
    bullets=["West Pharmaceutical Services, USA, 2003 — combustible dust deflagration.",
             "Buncefield Oil Terminal, UK, 2005 — vapour cloud and multi-tank fire.",
             "Grenfell Tower, UK, 2017 — combustible cladding and vertical spread.",
             "Each case isolates one mechanism and shows its consequences."],
    narr=('We will examine three incidents, each chosen because it isolates one mechanism. West Pharmaceutical Services in two thousand and three, for a combustible dust deflagration inside a manufacturing building. Buncefield Oil Terminal in two thousand and five, for the formation of a vapour cloud and the escalation to a multi-tank fire. And Grenfell Tower in two thousand and seventeen, for vertical fire spread involving a combustible external wall system. It offers lessons for industrial facade and panel systems, although their construction and behaviour are not identical. In each case identify the physical mechanism and then the organisational conditions that allowed the hazard to develop. Separate investigation findings from inference, and use the published investigation rather than this short summary as the authoritative account.'),
    note="Case studies are analysed, not narrated as stories.")

seg(id="case1", sec="19", kicker="19 · CASE STUDY 1", title="West Pharmaceutical Services, Kinston, USA — 2003",
    sub="Combustible polyethylene dust: a deflagration that propagated through a building",
    layout="case",
    visual=("case_west", {}),
    bullets=["29 January 2003. Six fatalities, dozens injured. Plant destroyed.",
             "Accumulated polyethylene dust on surfaces, beams and above a suspended ceiling.",
             "Primary deflagration in a production area; secondary explosions propagated through the building.",
             "Dust layers were the fuel; the building geometry was the propagation path.",
             "Lesson: dust is a fuel load, and a layer is a fuse."],
    narr=('On the twenty-ninth of January, two thousand and three, an explosion and fire occurred at West Pharmaceutical Services in Kinston, North Carolina. Six workers died and dozens were injured. The Chemical Safety Board investigation identified combustible polyethylene dust generated in the manufacturing process. Dust had accumulated above a suspended ceiling and on other elevated surfaces. The initial event dispersed accumulated dust, enabling further combustion and severe damage. The exact initiating ignition source was not conclusively established. The lesson is that hidden dust deposits are a serious distributed fuel hazard. Disturbance can suspend them in air, allowing a deflagration to propagate beyond the original location. Dust hazard assessment must include concealed spaces, effective collection, suitable housekeeping and ignition control. A clean-looking occupied floor does not demonstrate that overhead spaces are safe.'),
    note="Emphasise layer-to-cloud transition and propagation through openings.")

seg(id="case2", sec="19", kicker="19 · CASE STUDY 2", title="Buncefield Oil Terminal, UK — 2005",
    sub="Overfill, a vapour cloud, and the escalation of a tank farm fire",
    layout="case",
    visual=("case_buncefield", {}),
    bullets=["11 December 2005. Tank 912 overfilled with petrol; cascading fuel formed a flammable aerosol/vapour cloud.",
             "Vapour cloud explosion caused widespread blast damage; 43 injuries, no direct fatalities.",
             "Fire involved more than 20 tanks and burned for several days.",
             "Mechanisms: flash point, vapour dispersion, confinement, radiation between tanks, bunds and foam.",
             "Lesson: the most dangerous fire is sometimes the one that has not started yet."],
    narr=('On the eleventh of December, two thousand and five, tank nine hundred and twelve at the Buncefield oil terminal in England overfilled with petrol. Cascading fuel generated a large flammable vapour cloud in calm atmospheric conditions. The cloud ignited and a major explosion caused widespread damage. Forty-three people were injured; there were no fatalities. The subsequent fires involved more than twenty tanks and burned for several days. The investigations identified failures in level measurement, independent overfill protection and management systems. Vapour generation, dispersion and the interaction of flame with obstacles and site geometry are central to understanding the explosion, but this short account does not resolve every detail of its mechanism. The operational lesson is that a major flammable release can create an extreme hazard before visible fire appears. Prevention, detection, isolation and appropriate exclusion are critical.'),
    note="Tie back to flash point, flammable range and radiation between tanks.")

seg(id="case3", sec="19", kicker="19 · CASE STUDY 3", title="Grenfell Tower, UK — 2017",
    sub="Combustible cladding, cavity chimneys and vertical spread",
    layout="case",
    visual=("case_grenfell", {}),
    bullets=['14 June 2017; 72 people died.', 'Polyethylene-cored ACM cladding drove rapid external spread.', 'Insulation and external wall details also contributed.', 'Industrial panels require system-specific assessment, not direct equivalence.', 'Lesson: establish actual construction and tested performance.'],
    narr=('On the fourteenth of June, two thousand and seventeen, a fire originating in a fourth-floor flat spread rapidly over the external wall of Grenfell Tower in London. Seventy-two people died. The Grenfell Tower Inquiry identified the polyethylene-cored aluminium composite cladding as the principal reason for the rapid external spread. Combustible insulation and details of the external wall system also contributed. This was a system failure involving materials, interfaces, cavities and construction details, not simply a generic chimney effect. Industrial buildings with combustible panels can also present concealed spread hazards, but sandwich panels and ventilated rainscreen facades are not interchangeable systems. Their behaviour depends on the actual products, joints, supports and installation. The transferable lesson is to establish the external wall construction and its tested performance before an incident, rather than inferring safety from metal facings or appearance.'),
    note="Do not speculate on legal matters; focus on the physical mechanism.")

seg(id="case4", sec="19", kicker="19 · CASE SYNTHESIS", title="What the Three Cases Have in Common",
    sub="Mechanisms, not just mistakes",
    layout="table",
    visual=("case_compare", {}),
    bullets=['Distributed fuel can be hidden or underestimated.', 'Geometry influences different hazards in different ways.', 'Dust, vapour-cloud explosions and facade fires are distinct mechanisms.', 'Prevention and reliable protection matter before response.'],
    narr=('The three cases share important themes without having identical mechanisms. Fuel was distributed in ways that were easy to underestimate: dust on concealed surfaces, petrol vapour across a site, and combustible materials across an external wall. Geometry influenced how the hazard developed, but in different ways. Dust dispersion enabled further deflagration; a large vapour cloud produced a damaging explosion; an external wall system allowed rapid fire spread. Do not assume all three required confinement or can be explained by one simple model. Their investigations also show why prevention, reliable protection, competent design and management matter before the fire service arrives. Fire dynamics helps explain the physical possibilities; effective safeguards determine whether those possibilities become a disaster.'),
    note="Transition to the demonstration.")

# ----------------------------------------------------------------------------- 20 DEMONSTRATION
seg(id="dem1", sec="20", kicker="20 · ILLUSTRATIVE WAREHOUSE SCENARIO", title="The Scenario",
    sub='Scripted teaching scenario — not a validated fire simulation',
    layout="full",
    visual=("demo_setup", {}),
    bullets=[],
    narr=('We now use an illustrative warehouse scenario to connect the ideas. This is a scripted teaching animation, not a validated CFD simulation or a prediction of a real incident. The assumed building is sixty metres long, thirty metres wide and nine metres high, with lightweight steel construction and six-tier racks containing cartons and plastic goods. For the exercise we assign a fast time-squared growth curve to a fire near the base of a rack. That growth rate is an assumption, not something determined by the commodity description alone. Doors and roof vents begin closed. We initially omit sprinkler suppression to explore an unsuppressed scenario, not because sprinklers should be disabled. Actual smoke movement and fire growth would depend on leakage, fuel details, ventilation, detection and the protection system.'),
    note="State assumptions explicitly: this is a physics demonstration, not a validated simulation.")

seg(id="dem2", sec="20", kicker="20 · ILLUSTRATIVE WAREHOUSE SCENARIO", title="t = 0 to 3 min — Growth and the First Layer",
    sub='Assumed fast growth; smoke geometry is illustrative, not calculated',
    layout="demo",
    visual=("demo_anim", {"t0": 0, "t1": 180, "phase": "growth"}),
    bullets=['Assigned t² curve gives ≈ 1.5 MW at 3 min.', 'Smoke can travel beyond visible flames.', 'Depicted layer depth and temperature are not validated outputs.', 'TIC does not establish gas temperature or a safe layer boundary.'],
    narr=('The early frames illustrate a plume rising to the ceiling and a ceiling jet spreading outward. Hot gases can travel well beyond the visible flames. With the assigned fast-growth curve, the heat release rate at three minutes is about one point five megawatts. The depicted smoke depth and temperatures are illustrative; they have not been calculated by a validated smoke-filling model. A high ceiling can temporarily leave clearer air below the layer, but that appearance does not establish a tenable atmosphere or structural safety. A thermal camera may show hot surfaces and contrasts in the scene. It does not reliably map gas temperature or prove that the underside of a visible layer is a safe boundary. Use atmospheric monitoring, appropriate protective procedures and incident command assessment rather than interpreting the animation as an entry guide.'),
    note="Point out that the far end fills with smoke first, which is why early warning matters.")

seg(id="dem3", sec="20", kicker="20 · ILLUSTRATIVE WAREHOUSE SCENARIO", title="t = 3 to 6 min — Layer Descent and Lateral Spread",
    sub='Possible escalation routes; no predicted ignition time',
    layout="demo",
    visual=("demo_anim", {"t0": 180, "t1": 360, "phase": "spread"}),
    bullets=['Assigned growth curve gives ≈ 4.2 MW at 5 min.', 'Flames, radiation and hot gases can promote spread.', 'Rack ignition depends on exposure, geometry and protection.', 'No calculated aisle flux or structural temperature is implied.'],
    narr=('Between three and six minutes, the animation illustrates possible escalation within racking. The assigned growth curve reaches about four point two megawatts at five minutes. Hot gases, flame extension and radiation can preheat nearby commodities and promote spread, especially through rack flue spaces. Whether another rack ignites depends on exposure, duration, packaging, geometry and protection; the animation does not calculate that event. No particular heat flux at twelve metres or structural temperature should be inferred from these frames. In real warehouses, suppression can alter the trajectory substantially, and concealed or shielded burning complicates access. The teaching point is to assess multiple spread routes and the potential for escalation, not to conclude that layer cooling alone will control a rack fire. Tactical selection requires trained crews, appropriate systems and incident-specific assessment.'),
    note="This is the slide to emphasise radiation-driven spread.")

seg(id="dem4", sec="20", kicker="20 · ILLUSTRATIVE WAREHOUSE SCENARIO", title="t = 6 to 9 min — Ventilation Changes Everything",
    sub='Conceptual ventilation comparison — no guaranteed safe outcome',
    layout="compare_demo",
    visual=("demo_vent_compare", {}),
    bullets=['Opening doors can intensify burning and alter flow paths.', 'Roof venting can also increase hazards; cooler conditions are not guaranteed.', 'No validated warehouse HRR or safe-advance prediction is shown.', 'Coordinate ventilation with suppression and incident command.'],
    narr=('The next frames contrast two ventilation sequences conceptually. Opening a shutter can supply oxygen, alter the flow path and intensify burning in an under-ventilated fire. It does not automatically produce a particular heat release rate; fourteen megawatts is an illustrative limit from a separate simplified opening calculation, not a validated result for this warehouse. Opening a roof vent can also change burning and expose crews along new flow paths. It does not guarantee a lifted smoke layer, cooler working conditions or safe advance, even with charged lines present. Roof operations introduce additional fall and collapse hazards. The comparison therefore illustrates why ventilation must be coordinated with suppression and command, not a preferred universal sequence. Any ventilation action requires trained personnel, a hazard assessment and continuing evaluation of its actual effects.'),
    note="Use this as the tactical centrepiece.")

seg(id="dem5", sec="20", kicker="20 · ILLUSTRATIVE WAREHOUSE SCENARIO", title="t = 9 to 12 min — Decisions Under Uncertainty",
    sub='Continuous assessment, explicit uncertainty and incident command',
    layout="flow",
    visual=("decision_matrix", {}),
    bullets=['Consider conditions, suppression effectiveness, life risk and structure.', 'No universal layer-height or steel-temperature withdrawal threshold.', 'Establish incident-specific withdrawal criteria and exclusion zones.', 'Communicate observed trends without unsupported countdowns.'],
    narr=('At the closing stage, ask what evidence supports continuing, changing or ending the current strategy. Layer descent, flow at openings, smoke changes, suppression effectiveness, water supply, missing persons and structural condition all matter. None provides a reliable universal countdown to flashover or collapse. A thermal-camera reading on steel is not a direct measure of structural capacity, and four hundred degrees is not a general withdrawal threshold. Collapse can occur without visible warning. Decisions about offensive, transitional or defensive operations belong within the incident command system and applicable procedures. Establish explicit withdrawal criteria, accountability, communications, escape arrangements and exclusion zones. Communicate observed trends and uncertainty: for example, that conditions are deteriorating despite suppression. Do not convert a smoke-layer observation into an unsupported claim that flashover will occur in three minutes.'),
    note="Emphasise explicit trigger points and predictive communication.")

# ----------------------------------------------------------------------------- 21 TOOLS
seg(id="tool1", sec="21", kicker="21 · TOOLS FOR FIRE DYNAMICS ASSESSMENT", title="Reading the Fire Through Instruments",
    sub="Thermal imaging, smoke observation, modelling and monitoring",
    layout="tool_grid",
    visual=("tools_grid", {}),
    bullets=['TIC: apparent surface temperatures; emissivity and reflections matter.', 'Smoke: interpret multiple signs with ventilation and other evidence.', 'Modelling: planning and training, not safe-entry certification.', 'Monitoring: understand instrument limits and incomplete coverage.'],
    narr=('Four families of tools support assessment. Thermal imaging cameras show apparent surface temperatures and thermal contrasts within their operating limits. They cannot see through opaque walls or metal skins, and reflections, emissivity, smoke, water and viewing angle can mislead. They do not measure hidden gas temperature or certify structural safety. Smoke observation provides clues about movement, pressure and changing conditions, but colour alone cannot identify fuel, temperature or toxicity. Velocity, density, direction and pulsing must be interpreted together with ventilation and other evidence; no single sign diagnoses the fire regime reliably. Modelling supports pre-planning, design and training with stated uncertainty. Monitoring, including suitable gas detection and remote imagery, adds information but has coverage and instrument limitations. All these tools support competent judgement; none provides a standalone safe-entry indication.'),
    note="Be critical about TIC limitations: emissivity, reflections, range.")

seg(id="tool2", sec="21", kicker="21 · TOOLS FOR FIRE DYNAMICS ASSESSMENT", title="A Size-Up Sequence Built on Physics",
    sub="What to look at, in what order, and what each observation means",
    layout="table",
    visual=("sizeup_table", {}),
    bullets=['Building: construction, openings and concealed spaces.', 'Fuel: commodity, arrangement, dust, vapour and reactivity.', 'Smoke: observe trends; single signs are not diagnostic.', 'Heat: use instruments within limits; do not approach to feel flux.', 'Air: assess changing ventilation and flow paths.', 'Assessment: communicate uncertainty; continually reassess.'],
    narr=('A physics-informed size-up considers the building, fuel, smoke, heat and air movement, then records a provisional assessment. Identify construction, openings, concealed spaces and potentially combustible panels. Establish commodity hazards, storage arrangement and the possibility of dust, vapour or reactive materials. Observe smoke movement and changing conditions without treating colour or layer height as a definitive diagnosis. Use thermal imaging within its limitations and do not approach closer simply to feel radiant heat. Consider ventilation flow paths, suppression systems, water supplies, life risks and structural hazards. Communicate what is known, what is uncertain and what changes would trigger reassessment or withdrawal. Size-up is continuous, not a ninety-second test that guarantees safety for the rest of an incident. Apply local procedures and competent incident command throughout.'),
    note="This is the operational summary of the whole lecture.")

# ----------------------------------------------------------------------------- 22 ASSESSMENT & CLOSE
seg(id="asm1", sec="22", kicker="22 · ASSESSMENT", title="Postgraduate Assessment Questions",
    sub="Answer with reference to physical mechanisms, calculations and evidence",
    layout="assessment",
    visual=("assessment_list", {}),
    bullets=["1  Derive the conditions for flashover using Thomas and McCaffrey. Compare their assumptions.",
             "2  A 300 m² hall has two openings of 8 m² each, both 3 m high. Estimate the ventilation-limited HRR and discuss uncertainty.",
             "3  Explain why a fuel-controlled fire and a ventilation-controlled fire require different attack strategies.",
             "4  A warehouse fire is at 6 MW. Calculate illustrative radiation contours; explain why they are not safe exposure limits.",
             "5  Critically evaluate the t² model for a high-piled storage fire.",
             "6  Using one case study, identify the point at which fire dynamics knowledge would have changed the outcome.",
             "7  Discuss the claim: 'ventilation is the most powerful tactical variable in industrial firefighting'.",
             "8  Explain how a combustible sandwich panel defeats conventional compartmentation."],
    narr=('The assessment asks you to reason from mechanisms, calculations and evidence, with explicit assumptions. Compare the flashover correlations and their treatment of heat loss. For the ventilation example, use the stated opening dimensions and discuss the limits of the simplified estimate. Explain how the burning regime affects hazards without prescribing a universal tactic. For a six megawatt fire, calculate illustrative radiation contours using a stated radiative fraction, then explain why these do not establish safe distances for unprotected people. Critically evaluate the time-squared growth model. Use an investigation to distinguish physical mechanisms from organisational failures. Evaluate the role and hazards of ventilation, and explain concealed spread in a specified panel system. In the practical exercise, justify your assessment, identify missing information and show how uncertainty changes your conclusions. Marks reward sound reasoning, not confident predictions unsupported by evidence.'),
    note="Assessment should reward the ability to state assumptions and uncertainty.")

seg(id="close1", sec="22", kicker="22 · PROFESSIONAL LESSONS", title="Ten Lessons to Carry",
    sub="The lecture in ten sentences",
    layout="lessons",
    visual=None,
    bullets=["1  Fire development depends on rates and time, not appearance alone.",
             "2  HRR is central; geometry and ventilation also matter.",
             "3  The compartment is part of the combustion system.",
             "4  Ventilation can alter burning and flow paths.",
             "5  The hot layer is a radiator, a reservoir and a fuse.",
             "6  Smoke is the transport system for heat, fuel and toxicity.",
             "7  Rapid transitions and apparently steady conditions can both be dangerous.",
             "8  Conduction and concealed cavities defeat visible compartmentation.",
             "9  Models and instruments support judgement within their limits.",
             "10 Preparation, protection, water and coordinated command matter."],
    narr=('Ten lessons to carry forward. First, fire development depends on rates and time, not appearance alone. Second, heat release rate is a central variable, but geometry and ventilation also matter. Third, the compartment is part of the fire system. Fourth, ventilation changes can alter both burning and flow paths. Fifth, the hot layer stores and transfers energy. Sixth, smoke transports heat, toxic products and sometimes unburned fuel. Seventh, rapid transitions are dangerous, and apparently steady conditions can be dangerous too. Eighth, conduction and concealed combustible construction can bypass visible barriers. Ninth, models and instruments support judgement only within their limits. Tenth, effective response depends on preparation, protection systems, water, communications and coordinated command. None of these lessons creates a safe-entry guarantee. Their purpose is to improve the questions you ask, the uncertainties you recognise and the decisions you can justify.'),
    note="Close firmly; connect to the programme's professional standards.")

seg(id="close2", sec="22", kicker="22 · CLOSING", title="Reading Fire, Not Watching It",
    sub="IF 701 · Fire Dynamics · Master in Industrial Firefighting",
    layout="closing",
    visual=("hero_ember", {}),
    bullets=["Next session: fire chemistry, material behaviour and toxic effluents.",
             "Reading: SFPE Handbook, chapters on fire dynamics and compartment fires.",
             "Prepare: the calculation set and one case-study analysis."],
    narr=('Fire dynamics helps explain how fires develop, but it does not remove uncertainty or replace operational training. Understanding heat release, smoke movement and ventilation helps an officer form better assessments and recognise when assumptions are failing. It does not make the next transition predictable with certainty. Apply these ideas through site-specific planning, competent supervision and the procedures of your organisation. In the next session we examine fire chemistry, material behaviour and toxic effluents in more depth. Before then, complete the calculation set, read the assigned fire dynamics and compartment-fire chapters of the SFPE Handbook, and prepare one case-study analysis using its published investigation. Thank you for your attention. Bring your questions, your assumptions and the evidence that supports them.'),
    note="End with clear next steps.")
