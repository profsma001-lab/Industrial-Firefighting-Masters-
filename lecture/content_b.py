# -*- coding: utf-8 -*-
"""IF 701 - Fire Dynamics. Part B: ignition parameters, stages, HRR, growth, smoke, plumes."""

S = []

def seg(**kw):
    S.append(kw)

# ----------------------------------------------------------------------------- 05 IGNITION PARAMETERS
seg(id="ign1", sec="05", kicker="05 · IGNITION PARAMETERS", title="Ignition Temperature and Piloted Ignition",
    sub="The surface temperature at which sustained flaming begins",
    layout="split",
    visual=("ignition_curve", {}),
    bullets=["Piloted ignition: a spark or flame provides the activation energy.",
             "Autoignition: the material self-heats until it ignites without a pilot.",
             "Ignition temperature falls as exposure time and heat flux rise.",
             "Thin, low-density fuels ignite faster: ratio of area to mass."],
    narr=("Ignition temperature is the temperature at which a material produces flammable vapours fast enough to sustain flaming combustion. "
          "There are two routes. In piloted ignition, an external source, a spark or a small flame, provides the activation energy at the moment "
          "the fuel-air mixture is within its flammable range. In autoignition, no pilot is needed: the material is heated until it self-ignites. "
          "In practice, ignition temperature is not a single fixed number. It depends on the heat flux, on how long the exposure lasts, "
          "and on the material's thermal inertia. Thin materials with a high surface-area-to-mass ratio, such as paper, cotton waste or polymer film, "
          "heat through quickly and ignite at lower temperatures than thick timber."),
    note="Introduce thermal inertia qualitatively: k-rho-c.")

seg(id="ign2", sec="05", kicker="05 · IGNITION PARAMETERS", title="Autoignition Temperature",
    sub="Why oily rags and lagging catch fire without a spark",
    layout="split",
    visual=("ait_table", {}),
    bullets=["AIT is a property of the material and its geometry, not a constant.",
             "Self-heating: slow oxidation generates heat faster than it is lost.",
             "Classic industrial causes: oil-soaked lagging, paint rags, coal, hay, dust layers.",
             "Hot work near combustible insulation is a leading ignition source."],
    narr=("Autoignition temperature is the temperature at which a material ignites spontaneously in air, without an external ignition source. "
          "Typical values are around two hundred and fifty to three hundred degrees for wood, about five hundred and forty for methane, "
          "and about five hundred and eighty-five for hydrogen. "
          "But the practically important mechanism is self-heating. A material that oxidises slowly, such as oil-soaked lagging, a pile of paint rags "
          "or a coal stockpile, generates heat throughout its volume while losing heat only from its surface. "
          "If the pile is large enough and insulated well enough, the core temperature climbs until autoignition occurs. "
          "This is the mechanism behind many fires attributed to 'spontaneous combustion', and it is why hot work near combustible insulation, "
          "and the storage of oily waste, are controlled so strictly."),
    note="Distinguish AIT from self-heating; state that self-heating is size-dependent.")

seg(id="ign3", sec="05", kicker="05 · IGNITION PARAMETERS", title="Flash Point, Fire Point and Flammable Range",
    sub="The language of liquid fuel hazard",
    layout="table",
    visual=("flash_table", {}),
    bullets=["Flash point: lowest temperature at which a vapour ignites momentarily.",
             "Fire point: temperature at which vapour burns continuously, usually 5–20 °C above flash point.",
             "Flammable range: between the lower and upper explosive limits.",
             "Below the flash point the liquid is, in practice, not a fire risk."],
    narr=("For liquids we use three linked concepts. The flash point is the lowest temperature at which the liquid gives off enough vapour "
          "to form an ignitable mixture, which flashes when a pilot is applied. The fire point is a few degrees higher, the temperature at which "
          "the vapour continues to burn once ignited. And the flammable range is the range of vapour concentration in air between the lower "
          "and upper explosive limits, within which ignition produces a flame or an explosion. "
          "Petrol has a flash point around minus forty-three degrees, so it is always producing flammable vapour at ambient temperature. "
          "Diesel has a flash point near sixty degrees, so in a temperate climate a spill is far less likely to produce a flammable atmosphere, "
          "but a heated diesel tank or a spill onto hot plant is a different problem entirely."),
    note="Emphasise temperature dependence of vapour pressure. Link to tank fires and vapour cloud formation.")

# ----------------------------------------------------------------------------- 06 STAGES
seg(id="stg1", sec="06", kicker="06 · STAGES OF FIRE DEVELOPMENT", title="The Four Stages",
    sub="Temperature and heat release rate through a compartment fire",
    layout="full",
    visual=("fire_stages_chart", {}),
    bullets=[],
    narr=("This curve is the backbone of the lecture. Plot temperature against time in a compartment fire and four stages appear. "
          "First, ignition and the incipient stage, where the fire is small and local. "
          "Second, growth, where heat release rises, often in proportion to the square of time, while the hot layer deepens and descends. "
          "Third, the fully developed stage, where the fire is limited either by fuel supply or by ventilation and temperatures peak. "
          "Fourth, decay, as fuel is consumed or oxygen is exhausted, temperatures fall, but the fire is not necessarily out. "
          "Every stage has a signature that you can observe, and each one allows different tactics. "
          "The transitions between stages, not the stages themselves, are where firefighters are injured."),
    note="Animate or progressively draw this curve later in the demo.")

seg(id="stg2", sec="06", kicker="06 · STAGES OF FIRE DEVELOPMENT", title="Stage 1 — Incipient",
    sub="The first minutes decide the outcome",
    layout="split",
    visual=("incipient_viz", {}),
    bullets=["Fuel-limited, localised, often smouldering or small flame.",
             "Plume rises; a thin smoke layer begins to form at the ceiling.",
             "Temperatures in the layer: 50–150 °C.",
             "Detection, first-aid firefighting and evacuation are still possible."],
    narr=("In the incipient stage the fire is small, localised, and usually fuel-limited. "
          "A plume rises from the burning object, strikes the ceiling and begins to spread as a thin layer. "
          "Upper-layer temperatures are modest, perhaps fifty to a hundred and fifty degrees, and the space below remains tenable. "
          "This is the stage in which automatic detection should operate, in which a trained occupant can use a portable extinguisher, "
          "and in which evacuation is straightforward. "
          "It is also the stage most often missed, because smoke production is small and the fire may be hidden inside a rack, a duct, "
          "a ceiling void or a piece of equipment. The most valuable fire dynamics skill in this stage is simply recognising that the fire exists."),
    note="Relate to detection design and to the value of early notification.")

seg(id="stg3", sec="06", kicker="06 · STAGES OF FIRE DEVELOPMENT", title="Stage 2 — Growth",
    sub="The stage that kills: exponential energy, descending smoke",
    layout="split",
    visual=("growth_viz", {}),
    bullets=["HRR rises approximately with the square of time.",
             "Ceiling jet spreads fire to distant combustibles.",
             "Hot layer descends, radiating down onto the fuel bed.",
             "Rollover appears; flashover conditions begin to build."],
    narr=("Growth is the dangerous stage, and it is dangerous because it is non-linear. Heat release rises roughly with the square of time, "
          "so the fire that took two minutes to reach half a megawatt takes four minutes to reach two megawatts, and eight minutes to reach eight. "
          "The ceiling jet carries hot gas across the ceiling and can ignite combustible material far from the original fire. "
          "The hot layer thickens and descends. As it descends, it radiates down onto the fuel bed, which increases the burning rate, "
          "which in turn produces more hot gas. This is a positive feedback loop. "
          "Its visible signature is rollover: tongues of flame running through the smoke layer overhead. Rollover is a warning, "
          "not a guarantee, that flashover is approaching."),
    note="Use doubling logic explicitly: 2 minutes to 500 kW, 4 to 2 MW, 8 to 8 MW.")

seg(id="stg4", sec="06", kicker="06 · STAGES OF FIRE DEVELOPMENT", title="Stage 3 — Fully Developed",
    sub="Peak energy, structural exposure, no survivable interior",
    layout="split",
    visual=("fully_dev_viz", {}),
    bullets=["Temperatures 800–1 200 °C in the gas phase.",
             "Burning rate controlled by ventilation or fuel, not by the fuel surface.",
             "Flames project from openings; structural steel is at risk.",
             "Interior operations are no longer survivable: defensive or transitional."],
    narr=("In the fully developed stage the entire compartment is involved. Gas temperatures reach eight hundred to twelve hundred degrees, "
          "and the fire is no longer controlled by the surface area of the fuel. It is controlled either by the rate at which fuel is available "
          "or by the rate at which air can enter. Flames project from the openings, radiating intensely to any exposure. "
          "Structural steel, unprotected, reaches its critical temperature of about five hundred and fifty degrees within ten to twenty minutes "
          "of full involvement. "
          "At this point interior operations are not survivable, whatever the protective equipment. The tactical question becomes one of "
          "protecting exposures, cooling structural members from outside, and preventing spread, not of extinguishing the fire room."),
    note="Be explicit that PPE does not make a fully developed compartment survivable.")

seg(id="stg5", sec="06", kicker="06 · STAGES OF FIRE DEVELOPMENT", title="Stage 4 — Decay and Its Traps",
    sub="A falling temperature is not an extinguished fire",
    layout="split",
    visual=("decay_viz", {}),
    bullets=["Decay follows fuel consumption or oxygen depletion.",
             "Smouldering, hot embers and pyrolysis continue.",
             "Air entering a decayed, fuel-rich compartment can cause backdraft or reignition.",
             "Overhaul and atmospheric monitoring are fire dynamics tasks."],
    narr=("Decay arrives in two forms. If fuel is consumed, the fire simply runs out of material and temperatures fall steadily. "
          "If oxygen is depleted first, the compartment becomes fuel-rich and the visible flame may die back, while the interior remains extremely hot "
          "and full of unburnt pyrolysis gases. "
          "That second form is a trap. A quiet, smoke-stained compartment with no visible flame may be ready to reignite violently the moment air enters. "
          "This is the physical basis of backdraft, which we will examine shortly. "
          "Decay is therefore not the end of the incident but a change of hazard, from heat and flame to toxic atmosphere, structural weakness "
          "and explosive reignition. Overhaul is a fire dynamics operation, not a tidying-up exercise."),
    note="Bridge to backdraft in section 12.")

# ----------------------------------------------------------------------------- 07 HRR
seg(id="hrr1", sec="07", kicker="07 · HEAT RELEASE RATE", title="Typical Heat Release Rates",
    sub="Orders of magnitude every officer should carry in memory",
    layout="bar_chart",
    visual=("hrr_bars", {}),
    bullets=["Fire size spans six orders of magnitude.",
             "Warehouse rack fires: 5–30 MW per rack, higher with high-piled storage.",
             "Tank fires: 100 MW to several GW depending on diameter.",
             "Sprinkler and water supply design is based on these values."],
    narr=("Fire size spans an enormous range. A wastebasket might peak at twenty to a hundred kilowatts. An upholstered armchair, "
          "two hundred to four hundred kilowatts. A passenger car, one and a half to five megawatts. A single retail rack of mixed goods, "
          "five to thirty megawatts. A large warehouse fire, fifty to a hundred megawatts or more. An open hydrocarbon tank fire, "
          "hundreds of megawatts to gigawatts depending on diameter. "
          "These figures are not academic. They determine sprinkler design, water supply, foam application rates and safe standoff distances. "
          "When an officer says the fire is 'big', a fire dynamics officer asks: how big, in megawatts, and what does that imply for the water we have?"),
    note="Have students memorise the table; it underpins every calculation later.")

seg(id="hrr2", sec="07", kicker="07 · HEAT RELEASE RATE", title="How HRR Is Measured",
    sub="Oxygen consumption calorimetry: fire science's most robust instrument",
    layout="split",
    visual=("calorimetry", {}),
    bullets=["Principle: 13.1 MJ is released per kg of oxygen consumed, for most fuels.",
             "Cone calorimeter: 100 × 100 mm samples at controlled heat flux.",
             "Furniture and room calorimeters: full-scale items, up to 10 MW.",
             "Field estimate: HRR from flame length, smoke volume or water flow."],
    narr=("We measure heat release rate by measuring oxygen consumption. For almost all organic fuels, thirteen point one megajoules of energy "
          "are released per kilogram of oxygen consumed. So if we capture the effluent from a burning object, measure its flow and its oxygen "
          "concentration, and compare that with the incoming air, we can calculate the heat release rate directly. "
          "The cone calorimeter does this on small samples at a controlled heat flux. Furniture calorimeters do it on complete items. "
          "Large industrial calorimeters can measure ten megawatts or more. "
          "In the field we cannot measure oxygen consumption, so we estimate from observable proxies: flame length, smoke volume and density, "
          "the size of the burning area, and the water flow required to control it."),
    note="13.1 MJ/kg O2 is worth memorising; it links combustion stoichiometry to calorimetry.")

seg(id="hrr3", sec="07", kicker="07 · HEAT RELEASE RATE", title="Why One Number Explains So Much",
    sub="Scaling relationships that follow from HRR",
    layout="split",
    visual=("scaling_tree", {}),
    bullets=["Flame length grows with HRR to the power 2/5.",
             "Plume mass flow grows with the cube root of convective HRR.",
             "Smoke production is proportional to HRR and soot yield.",
             "Radiant flux at a distance falls with the square of distance."],
    narr=("The reason we treat heat release rate as the master variable is that so many other quantities scale from it. "
          "Flame length grows with heat release rate to the power two-fifths. "
          "The mass flow in the plume grows with the cube root of the convective heat release rate. "
          "Smoke production is proportional to heat release rate and to the soot yield of the fuel. "
          "Radiant heat flux at a given distance falls with the square of that distance. "
          "Put together, these relationships let you go from one measurement or estimate to a whole set of predictions: "
          "how high the flames will be, how much smoke will be produced, how hot the ceiling will get, and how far away a person must stand. "
          "That is the analytical core of fireground forecasting."),
    note="Preview the worked calculations in section 18.")

# ----------------------------------------------------------------------------- 08 GROWTH
seg(id="grw1", sec="08", kicker="08 · FIRE GROWTH", title="The Time-Squared Fire",
    sub="A single parameter that describes the growth phase",
    layout="equation",
    visual=("alpha_table", {}),
    bullets=["Q = α t², where α is the growth coefficient (kW/s²).",
             "Slow 0.00293 · Medium 0.01172 · Fast 0.0469 · Ultra-fast 0.1876",
             "Time to 1 055 kW: 600 s · 300 s · 150 s · 75 s.",
             "α is a property of the fuel package and its arrangement."],
    narr=("The growth phase is commonly described by a single equation: heat release rate equals the growth coefficient alpha, "
          "multiplied by the square of time since ignition. Alpha has units of kilowatts per second squared, and standard values are used "
          "for design: slow, zero point zero zero two nine three; medium, zero point zero one one seven two; fast, zero point zero four six nine; "
          "and ultra-fast, zero point one eight seven six. "
          "The conventional benchmark is the time to reach one thousand and fifty-five kilowatts, which is one megawatt in British thermal units per second. "
          "That takes six hundred seconds for a slow fire, three hundred for medium, one hundred and fifty for fast and seventy-five for ultra-fast. "
          "Note what alpha really describes: not the material alone, but the fuel package, its arrangement and its ability to draw air."),
    note="Alpha is empirical, not fundamental. Emphasise arrangement and airflow.")

seg(id="grw2", sec="08", kicker="08 · FIRE GROWTH", title="Reading the Growth Curve",
    sub="What the four curves tell a commander",
    layout="chart",
    visual=("alpha_chart", {}),
    bullets=["Doubling time quadruples heat release.",
             "A fast fire reaches 4 MW in about five minutes.",
             "Ultra-fast fires reach flashover conditions before many crews are dressed.",
             "Classify the fuel package on arrival, not after the fire is out."],
    narr=("Look at how the curves separate. After five minutes, a slow fire is still under half a megawatt, a medium fire is about one and three-quarter megawatts, "
          "a fast fire is about seven megawatts, and an ultra-fast fire is approaching thirty. "
          "This is why pre-planning matters. If you can classify the fuel package on arrival, you can place the fire on one of these curves "
          "and predict, within a factor, what it will be doing in the next five minutes. "
          "That prediction is what determines whether you commit crews to an interior attack or set up master streams. "
          "The classification is not about the label on the material safety data sheet; it is about how the fuel is arranged, "
          "how much surface area is exposed and how much air it can reach."),
    note="Ask students to classify: palletised cartons, racked polymer, foam mattress storage, LPG.")

seg(id="grw3", sec="08", kicker="08 · FIRE GROWTH", title="Where the t-Squared Model Fails",
    sub="Use it for growth, not for the whole fire",
    layout="split",
    visual=("model_limits", {}),
    bullets=["It ignores ventilation: real fires stall or surge when openings change.",
             "It ignores fuel burnout and decay.",
             "It assumes unlimited fuel and air.",
             "At large HRR, flame radiation and oxygen limitation dominate."],
    narr=("The time-squared model is a design tool, and like every model it has a domain of validity. "
          "It assumes unlimited fuel and unlimited air, so it describes the growth phase only. "
          "It cannot represent a fire that becomes ventilation-limited and flattens out, or one that surges when a window fails. "
          "It does not describe decay, and it does not describe the very large fires in which radiation from the flame zone controls spread, "
          "and in which the burning rate per unit area becomes independent of the fuel arrangement. "
          "For a warehouse or a process plant, the practical approach is to use time-squared for the first few minutes, then switch to a "
          "ventilation-based estimate of the maximum heat release rate. "
          "We will do exactly that in the worked examples."),
    note="Critical thinking about models; good postgraduate material.")

# ----------------------------------------------------------------------------- 09 SMOKE
seg(id="smk1", sec="09", kicker="09 · SMOKE", title="What Smoke Is Made Of",
    sub="A toxic, hot, optically dense aerosol — and the main killer",
    layout="split",
    visual=("smoke_composition", {}),
    bullets=["Particulates: soot, ash, condensed hydrocarbons.",
             "Asphyxiants: carbon monoxide, hydrogen cyanide.",
             "Irritants: hydrogen chloride, acrolein, sulphur dioxide, nitrogen oxides.",
             "Water vapour and unburnt fuel; temperature 300–700 °C in the layer."],
    narr=("Smoke is not a single substance. It is an aerosol of solid particles, liquid droplets and gases. "
          "The particles are mainly soot, and soot is what makes smoke optically dense and what radiates heat so effectively. "
          "The gases include the asphyxiants carbon monoxide and hydrogen cyanide, the irritants hydrogen chloride, acrolein, "
          "sulphur dioxide and the nitrogen oxides, plus water vapour and unburnt fuel. "
          "In a compartment fire, most deaths are caused by inhalation of these gases, not by burns. "
          "Carbon monoxide binds to haemoglobin some two hundred and forty times more strongly than oxygen, and hydrogen cyanide "
          "blocks cellular respiration. Together they are synergistic: the combination is far more lethal than either alone."),
    note="Justify smoke as a fire dynamics topic, not just a health and safety topic.")

seg(id="smk2", sec="09", kicker="09 · SMOKE", title="Why Smoke Rises and Spreads",
    sub="Buoyancy, expansion, and the paths of least resistance",
    layout="split",
    visual=("smoke_drivers", {}),
    bullets=["Buoyancy: hot gas is less dense; the driving force is temperature difference.",
             "Expansion: smoke volume is roughly three times the air consumed.",
             "Drivers: stack effect, wind, HVAC, lift shafts, service risers.",
             "Leakage paths determine where smoke actually goes."],
    narr=("Smoke rises because it is hot and therefore less dense than the surrounding air. The driving force is proportional to the temperature "
          "difference between the smoke and the ambient air, so a hotter fire produces a stronger plume. "
          "Second, combustion expands the gas. Burning one cubic metre of air produces roughly three cubic metres of smoke at flame temperature, "
          "so a fire acts as a pump, pushing gas out through every available opening. "
          "Third, the building imposes its own driving forces: stack effect in tall spaces, wind pressure on the facade, mechanical ventilation, "
          "and the buoyancy of hot gas in shafts and risers. "
          "The practical implication is that smoke finds the paths we forgot: cable penetrations, lift shafts, ceiling voids, "
          "and the gaps around poorly fitted fire doors."),
    note="Stack effect and leakage: link to smoke control design.")

seg(id="smk3", sec="09", kicker="09 · SMOKE", title="Stratification, the Smoke Layer and the Neutral Plane",
    sub="Three terms that explain what you see at a doorway",
    layout="full",
    visual=("smoke_layer", {}),
    bullets=[],
    narr=("In a compartment, hot smoke collects under the ceiling and forms a layer. Because hot gas is buoyant, it tends to stay above cooler air, "
          "and the boundary between the two is the interface. In an ideal two-layer model, above the interface it is hot and toxic; below it, "
          "the air remains relatively cool and clear. "
          "At an opening, such as a door, the pressure difference produces a two-way flow: hot gas flows out at the top, and fresh air flows in at the bottom. "
          "The height at which the flow reverses is the neutral plane. "
          "Reading the neutral plane is a direct measurement of fire conditions. A high neutral plane with a thin smoke layer means a small fire. "
          "A neutral plane near the floor means the compartment is full of hot gas, and the fire is either large or ventilation-limited and fuel-rich."),
    note="Ask: what does a neutral plane at head height tell you? Answers: significant fire, layer deep.")

seg(id="smk4", sec="09", kicker="09 · SMOKE", title="Smoke and Visibility: The Practical Currency",
    sub="Optical density, visibility distance and tenability limits",
    layout="split",
    visual=("visibility_chart", {}),
    bullets=["Visibility in smoke: 3–10 m is typical in a developed fire.",
             "Tenability: 10 m visibility is a common design target.",
             "Smoke logged at 5 m means crews cannot find the fire or a exit.",
             "Thermal imaging restores some capability, but not all."],
    narr=("For firefighters, the practical measure of smoke is visibility. Visibility depends on the optical density of the smoke, which depends on "
          "soot concentration. In a developed compartment fire, visibility of three to ten metres is typical; in a large volume with high soot yield, "
          "it can be less. Design guidance often uses ten metres as the minimum for a space to remain tenable. "
          "Below five metres, a crew cannot reliably find the seat of the fire, cannot see a casualty, and cannot confirm a exit. "
          "Thermal imaging cameras help, because they see through smoke to temperature differences, but they do not restore spatial orientation "
          "and they do not measure toxicity. "
          "This is why smoke conditions, not flame, usually set the pace of an interior attack."),
    note="Prepare for the TIC discussion in section 20.")

# ----------------------------------------------------------------------------- 10 PLUMES AND CEILING JETS
seg(id="plm1", sec="10", kicker="10 · PLUMES & CEILING JETS", title="Anatomy of a Fire Plume",
    sub="Where the heat, the smoke and the danger actually go",
    layout="full",
    visual=("plume_zones", {}),
    bullets=[],
    narr=("A fire plume is the column of hot gas rising above the burning fuel. It has three regions. "
          "Directly above the fuel is the continuous flame zone, where the reaction is still completing. "
          "Above that is the intermittent flame zone, where flaming tongues appear and disappear, and where the temperature fluctuates violently. "
          "Above that is the buoyant plume, where the gas is hot but no longer burning, and where entrainment of surrounding air dominates. "
          "The plume entrains air continuously, so its mass flow increases with height, and its temperature decreases. "
          "The height of the flame, according to Heskestad, is zero point two three five times the heat release rate to the power two-fifths, minus about one diameter. "
          "Standing in a plume is never acceptable, even at ceiling level, because temperatures there can exceed six hundred degrees."),
    note="Heskestad flame height equation; give a numeric example verbally: 2 MW, 2 m diameter → ~4.5 m.")

seg(id="plm2", sec="10", kicker="10 · PLUMES & CEILING JETS", title="The Ceiling Jet",
    sub="How a fire reaches the far end of a hall in seconds",
    layout="split",
    visual=("ceiling_jet", {}),
    bullets=["Plume hits the ceiling and turns radially outward.",
             "Ceiling jet velocity and temperature decay with radius.",
             "Alpert: ΔT = 16.9 Q^(2/3) / H^(5/3) near the plume.",
             "Sprinklers and detectors are actuated by the ceiling jet."],
    narr=("When the plume strikes a ceiling it cannot continue upward, so it turns and spreads radially as a ceiling jet. "
          "This jet is thin, fast and hot. Near the plume, Alpert's correlation gives the temperature rise as sixteen point nine, "
          "times heat release rate to the two-thirds, divided by the height to the five-thirds. "
          "Further out, the temperature rise falls as the two-thirds power of heat release rate divided by radius. "
          "The velocity follows a similar form. "
          "The ceiling jet is the reason a fire can activate a detector twenty metres away within a minute, and it is also the reason the "
          "first sprinkler to operate may be well away from the fire. In large-volume buildings the jet can travel a hundred metres or more, "
          "cooling and thickening as it goes, and creating the smoke reservoir that determines how fast the space fills."),
    note="Give the Alpert formula verbally; the equation card appears in section 18.")

seg(id="plm3", sec="10", kicker="10 · PLUMES & CEILING JETS", title="Building a Hot Layer",
    sub="The feedback loop that leads to flashover",
    layout="full",
    visual=("layer_build", {}),
    bullets=[],
    narr=("Now watch the layer build. The ceiling jet spreads, cools against the walls and the ceiling, and begins to descend. "
          "As the layer thickens, its underside radiates heat downward onto everything below: the fuel bed, the furniture, the racks, the people. "
          "That radiant feedback increases the rate of pyrolysis at the fuel surface, which increases the heat release rate, "
          "which produces more hot gas, which deepens the layer further. "
          "The layer also stores energy, so its temperature climbs. A layer at three hundred degrees radiates about five kilowatts per square metre "
          "to the floor; at six hundred degrees, about twenty. "
          "That number, twenty kilowatts per square metre at floor level, is one of the standard criteria for flashover. "
          "The layer is therefore not a consequence of the fire; it is part of the mechanism."),
    note="Quantify the layer's radiative feedback with the Stefan-Boltzmann estimate.")
