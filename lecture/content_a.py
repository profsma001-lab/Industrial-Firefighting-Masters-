# -*- coding: utf-8 -*-
"""IF 701 - Fire Dynamics. Part A of the lecture content (opening to fire growth)."""

S = []

def seg(**kw):
    S.append(kw)

# ----------------------------------------------------------------------------- 00 OPENING
seg(id="open1", sec="00", kicker="OPENING", title="Understanding Fire Dynamics",
    sub="Heat Transfer, Combustion, Smoke Movement and Industrial Fire Development",
    layout="title",
    visual=("hero_ember", {}),
    bullets=[],
    narr=("Welcome to this lecture in the Master of Industrial Firefighting programme. "
          "Our course is IF 701, Fire Dynamics, and the title of this session is Understanding Fire Dynamics: "
          "heat transfer, combustion, smoke movement and industrial fire development. "
          "Over the next hour we will treat fire not as chaos, but as a physical process that obeys rules. "
          "Once you can read those rules, you can predict what a fire will do next, and prediction is the foundation "
          "of every safe decision a fire officer makes."),
    note="Open deliberately. State the promise of the lecture: prediction, not description.")

seg(id="open2", sec="00", kicker="WHY THIS MATTERS", title="A Fire Is a Physics Problem With a Deadline",
    sub="Every tactical decision is a prediction about fire behaviour",
    layout="split",
    visual=("key_figures", {"items": [
        ("~1 MW", "heat released by a small upholstered chair at 5 minutes", "ember"),
        ("20 MW", "a growing rack of stored goods in a warehouse", "amber"),
        ("500 °C", "typical upper-layer temperature at flashover", "red"),
        ("1 kg", "of air supports roughly 3 MJ of combustion", "teal")]}),
    bullets=["Fire behaviour is predictable in principle.",
             "Predictions are uncertain in practice.",
             "Good officers manage that uncertainty with observation."],
    narr=("Consider a fire in a storage warehouse. Within three minutes it may be releasing one megawatt, "
          "the thermal equivalent of a thousand one-bar electric heaters. Within eight minutes the same fire can pass "
          "twenty megawatts, and by then the building itself is part of the fuel package. "
          "Nothing about that escalation is random. It is driven by heat transfer, by the geometry of the building, "
          "and by the air we allow in. A firefighter who understands fire dynamics is not guessing; "
          "he or she is reading a physical system and anticipating its next state."),
    note="Frame the lecture around time: fire grows exponentially, decisions are made in minutes.")

# ----------------------------------------------------------------------------- 01 INTRODUCTION
seg(id="intro1", sec="01", kicker="01 · INTRODUCTION TO FIRE DYNAMICS", title="What Fire Dynamics Actually Studies",
    sub="The physics and chemistry of fire, and of fire in an enclosure",
    layout="bullets",
    visual=("process_ring", {"items": ["Ignition", "Combustion", "Heat release", "Heat transfer", "Smoke & gases", "Enclosure response"]}),
    bullets=["Ignition and the conditions for sustained burning",
             "The rate at which fuel releases energy",
             "How that energy moves by conduction, convection and radiation",
             "How smoke and hot gases move, stratify and fill a space",
             "How the building, its ventilation and its contents feed back on the fire"],
    narr=("Fire dynamics is the study of fire as a physical and chemical phenomenon. It asks four questions. "
          "First, how does a material begin to burn, and what keeps it burning? Second, at what rate is energy released? "
          "Third, how does that energy travel to other objects? And fourth, how do the products of combustion, the smoke "
          "and the hot gases, move through the space and change the fire itself? "
          "Fire dynamics is therefore a system science. The flame, the fuel, the air and the building all influence one another. "
          "Change one of them, and the fire changes."),
    note="Emphasise feedback: the enclosure is part of the combustion system, not a passive container.")

seg(id="intro2", sec="01", kicker="01 · INTRODUCTION TO FIRE DYNAMICS", title="Why Industrial Firefighting Demands This Knowledge",
    sub="Scale, fuel chemistry, process equipment and escalation",
    layout="split",
    visual=("compare_panels", {"left": ("DOMESTIC", ["Compartment 20–60 m²", "Cellulosic fuel", "1–5 MW peak", "Flashover 5–10 min"]),
                                "right": ("INDUSTRIAL", ["Volume 5 000–100 000 m³", "Hydrocarbons, polymers, dusts", "50–500 MW peak", "Escalation in seconds"])}),
    bullets=["Industrial fuel loads are dense, mixed and often reactive.",
             "Open volumes delay flashover but produce enormous smoke production.",
             "Process equipment introduces pressure, chemicals and explosion hazard.",
             "Escalation, not the first flame, is the real threat."],
    narr=("Industrial firefighting is not domestic firefighting at a larger scale. The physical regimes differ. "
          "A dwelling gives us a small compartment, a predictable fuel load, and flashover within five to ten minutes. "
          "A warehouse, a refinery or a manufacturing hall gives us enormous volumes, dense and chemically varied fuel, "
          "and process equipment that can fail under fire exposure. "
          "In an industrial setting the fire may never flash over in the domestic sense, yet it can release hundreds of megawatts, "
          "destroy structural steel, and escalate from a single ignition point to a site-wide emergency. "
          "That is why this course exists."),
    note="Contrast regimes, not just size.")

seg(id="intro3", sec="01", kicker="01 · INTRODUCTION TO FIRE DYNAMICS", title="Learning Outcomes for This Lecture",
    sub="By the end of the hour you should be able to",
    layout="outcomes",
    visual=None,
    bullets=["1  Define fire, combustion, ignition and heat release rate precisely.",
             "2  Apply the fire tetrahedron to explain extinction and re-ignition.",
             "3  Quantify conduction, convection and radiation in fire situations.",
             "4  Describe the four stages of fire development and recognise each.",
             "5  Use the t-squared model to estimate growth, and explain its limits.",
             "6  Predict smoke movement, stratification and hot-layer behaviour.",
             "7  Explain flashover, backdraft and ventilation-controlled burning.",
             "8  Analyse fire spread in industrial buildings and storage.",
             "9  Perform practical calculations of HRR, heat flux and fire growth.",
             "10 Interpret modelling output and select evidence-based tactics."],
    narr=("Here is what you should be able to do when we finish. Define fire, combustion and heat release rate precisely, "
          "and use the fire tetrahedron to explain why a fire goes out. Quantify the three modes of heat transfer. "
          "Recognise each of the four stages of fire development from the evidence available on the fireground. "
          "Estimate growth with the time-squared model and, just as importantly, explain where that model fails. "
          "Predict smoke movement and hot-layer behaviour. Explain flashover, backdraft and ventilation-controlled burning. "
          "Analyse fire spread in industrial buildings, carry out practical calculations, and finally, read a computer "
          "fire model critically and turn it into a tactical decision."),
    note="Outcomes frame the assessment at the end.")

# ----------------------------------------------------------------------------- 02 DEFINITIONS
seg(id="def1", sec="02", kicker="02 · DEFINITIONS", title="Fire, Combustion and Flame",
    sub="Three words that are not interchangeable",
    layout="definitions",
    visual=("def_cards", {"items": [
        ("COMBUSTION", "A self-sustaining exothermic chemical reaction, usually oxidation, producing heat and light."),
        ("FLAME", "The visible, luminous zone of gas-phase reaction where fuel vapour and oxygen meet and burn."),
        ("FIRE", "The whole phenomenon: combustion plus its heat, flame, smoke, gases and their effects.")]}),
    bullets=[],
    narr=("Let us be precise from the start, because these three words are often used loosely. "
          "Combustion is a self-sustaining exothermic chemical reaction, usually between a fuel and oxygen, "
          "that releases heat and light. Self-sustaining is the key phrase: the reaction supplies the energy needed to keep itself going. "
          "A flame is the visible, luminous zone of that reaction in the gas phase, where fuel vapour and oxygen meet and burn. "
          "And fire is the whole phenomenon: the combustion, the flame, the heat, the smoke, the toxic gases and their effects on people and structures. "
          "So a material can combust without a visible flame, as in smouldering charcoal, and a fire can exist as an entire system."),
    note="Insist on the distinction: smouldering combustion has no flame.")

seg(id="def2", sec="02", kicker="02 · DEFINITIONS", title="Heat, Temperature and Thermal Energy",
    sub="The most common conceptual error in firefighting",
    layout="split",
    visual=("compare_units", {"rows": [
        ("Temperature", "°C or K", "How hot something is — average molecular kinetic energy"),
        ("Heat", "J or kJ", "Quantity of thermal energy transferred or stored"),
        ("Heat flux", "kW/m²", "Rate of heat arriving per square metre — what ignites things"),
        ("Heat release rate", "kW or MW", "Rate at which the fire releases chemical energy as heat")]}),
    bullets=["Temperature tells you how hot; heat flux tells you how dangerous.",
             "A steel beam at 500 °C stores far more heat than a spark at 1 500 °C.",
             "Ignition depends on heat flux and time, not temperature alone.",
             "Water absorbs heat, not temperature."],
    narr=("Temperature and heat are not the same thing. Temperature measures how hot a body is, effectively the average kinetic energy of its molecules. "
          "Heat is a quantity of energy, measured in joules. Heat flux is the rate at which heat arrives at a surface, in kilowatts per square metre, "
          "and it is heat flux, together with exposure time, that determines whether something ignites. "
          "A spark at fifteen hundred degrees carries almost no energy, while a steel column at five hundred degrees stores megajoules. "
          "This distinction explains a practical fact: water cools because it absorbs heat, roughly two point four megajoules per kilogram when it turns to steam, "
          "not because it lowers temperature directly."),
    note="Use the spark versus beam analogy; it lands well with practitioners.")

seg(id="def3", sec="02", kicker="02 · DEFINITIONS", title="Heat Release Rate: The Master Variable",
    sub="Energy per second, and the number that governs everything else",
    layout="equation",
    visual=("eq_card", {"title": "Heat release rate of a burning fuel package",
                         "eq": "Q  =  m  ×  ΔHc  ×  χ",
                         "terms": ["Q — heat release rate, kW",
                                   "m — mass loss rate of fuel, kg/s",
                                   "ΔHc — effective heat of combustion, kJ/kg",
                                   "χ — combustion efficiency, 0 to 1"]}),
    bullets=["1 kg of wood ≈ 16 MJ; 1 kg of petrol ≈ 44 MJ.",
             "A fire is characterised by its HRR curve, not by its size.",
             "HRR drives temperature, smoke production, flame length and heat flux.",
             "Design and tactics are both sized to HRR."],
    narr=("The heat release rate, written Q-dot and measured in kilowatts, is the single most important quantity in fire dynamics. "
          "It is simply the mass of fuel burning each second, multiplied by the energy released per kilogram of fuel, "
          "multiplied by a combustion efficiency that accounts for incomplete burning. "
          "One kilogram of wood releases about sixteen megajoules; one kilogram of petrol, about forty-four. "
          "Everything else we care about follows from the heat release rate: the temperature of the hot layer, the volume of smoke, "
          "the length of the flames, the heat flux to a neighbouring building, and the water flow required to control it. "
          "If you know the heat release rate, you can estimate the rest. If you do not, you are estimating blind."),
    note="Signpost that HRR returns in section 7 with real values.")

# ----------------------------------------------------------------------------- 03 TETRAHEDRON
seg(id="tetra1", sec="03", kicker="03 · THE FIRE TETRAHEDRON", title="From the Triangle to the Tetrahedron",
    sub="Four elements must be present together for flaming combustion",
    layout="full",
    visual=("tetrahedron", {}),
    bullets=[],
    narr=("For most of the twentieth century we taught the fire triangle: fuel, oxygen and heat. "
          "The triangle explained smouldering and simple burning, and it still explains why we cool, smother and starve a fire. "
          "But it could not explain why some fires continued to burn in conditions where fuel, oxygen and heat were all present. "
          "The answer is the fourth element: the chemical chain reaction. Flaming combustion proceeds through fast radical reactions, "
          "in which highly reactive fragments such as hydrogen and hydroxyl radicals propagate the flame. "
          "Add that fourth element and the triangle becomes a tetrahedron: fuel, oxygen, heat and chain reaction, each one a face, "
          "and all four required at once."),
    note="Explain radical chain branching simply: molecular fragments that keep the reaction going.")

seg(id="tetra2", sec="03", kicker="03 · THE FIRE TETRAHEDRON", title="Fuel: What Actually Burns",
    sub="Almost all fuels burn as gases or vapours, not as solids",
    layout="split",
    visual=("fuel_classes", {}),
    bullets=["Solids pyrolyse: heat breaks them into flammable vapours.",
             "Liquids burn as their vapour above the surface.",
             "Gases are already fuel; they only need mixing.",
             "Industrial fuels: polymers, hydrocarbons, dusts, metals, cable compounds."],
    narr=("Here is a point that surprises many recruits: with very few exceptions, solids and liquids do not burn. "
          "What burns is the gas above them. A log of wood is heated until pyrolysis breaks its polymers into flammable vapours, "
          "and those vapours burn. Petrol in a tray is not on fire; the vapour layer above the liquid is. "
          "This is why a liquid below its flash point is relatively safe, and why a solid that chars can keep producing fuel long after the flame is out. "
          "In industry the fuels are polymers such as polyethylene and polyurethane, hydrocarbons, combustible dusts, and in special cases metals. "
          "Each behaves differently, and each produces different smoke."),
    note="Pyrolysis is the concept to stress. Link forward to flash point.")

seg(id="tetra3", sec="03", kicker="03 · THE FIRE TETRAHEDRON", title="Oxygen, Oxidisers and Radical Inhibition",
    sub="Air is 21 per cent oxygen; combustion needs far less, and warns us at both extremes",
    layout="split",
    visual=("oxygen_gauge", {}),
    bullets=["Flames generally extinguish below 14–15 % oxygen.",
             "Smouldering can persist at 5–8 % oxygen.",
             "Oxygen-enriched atmospheres make materials burn violently.",
             "Oxidisers such as nitrates and peroxides supply their own oxygen."],
    narr=("Air contains twenty-one per cent oxygen by volume. Flaming combustion typically cannot be sustained below about fourteen or fifteen per cent, "
          "but smouldering can continue at five to eight per cent, which matters in deep-seated and silo fires. "
          "At the other extreme, an oxygen-enriched atmosphere, above about twenty-three and a half per cent, dramatically lowers ignition energy "
          "and accelerates burning; clothing and hair can burn fiercely. "
          "And we must remember oxidisers: nitrates, chlorates, peroxides and ammonium nitrate contain oxygen within their own structure. "
          "They can sustain or intensify combustion where air is excluded, which is why storage segregation rules exist. "
          "The fourth element, the chain reaction, is the target of clean agents and dry chemical powders: they interrupt the radical chemistry rather than cooling or smothering."),
    note="Mention Beirut 2020 only as a storage-hazard example, not as a fire dynamics case.")

# ----------------------------------------------------------------------------- 04 HEAT TRANSFER
seg(id="ht1", sec="04", kicker="04 · HEAT TRANSFER", title="Three Modes, Always Simultaneous",
    sub="Conduction, convection and radiation move the fire through the building",
    layout="full",
    visual=("heat_modes", {}),
    bullets=[],
    narr=("Heat moves in three ways, and in a real fire all three operate at once. "
          "Conduction is transfer through a solid by molecular contact. Convection is transfer by the movement of a fluid, "
          "in our case hot smoke and gases. Radiation is transfer by electromagnetic waves, requiring no medium at all. "
          "As a fire develops, the dominant mode changes. In the early stage, convection in the plume and radiation from the flame dominate. "
          "In the growth stage, radiation from the deepening hot layer becomes decisive. "
          "In a fully developed compartment fire, radiation and convection through the openings account for most of the energy leaving the compartment. "
          "Understanding which mode dominates tells you what to cool, and where."),
    note="Set up the three following slides.")

seg(id="ht2", sec="04", kicker="04 · HEAT TRANSFER", title="Conduction: The Hidden Path",
    sub="Fourier's law, and why fire appears where there is no flame",
    layout="equation",
    visual=("conduction_diagram", {}),
    bullets=["q = k A ΔT / L — heat flow rises with area and temperature difference, falls with thickness.",
             "Steel (k ≈ 45) conducts a thousand times better than mineral wool (k ≈ 0.04).",
             "Conduction ignites roofs, spreads along pipes, cable trays and steel beams.",
             "Contact cooling with water interrupts the path."],
    narr=("Conduction is described by Fourier's law: heat flow equals the thermal conductivity of the material, times the area, "
          "times the temperature difference, divided by the thickness. "
          "The conductivity constant matters enormously. Steel conducts heat at about forty-five watts per metre kelvin, "
          "mineral wool at about zero point zero four. That is a factor of a thousand. "
          "Conduction is why a fire in a room can ignite material in the roof space above it, why heat travels along a steel pipe "
          "through a fire wall, and why cable trays and conveyor belts carry fire from one end of a plant to the other. "
          "It is also why a closed steel door is not a fire barrier unless it is insulated: the door leaf stays cool on the fire side and hot on the other."),
    note="Concrete example: steel door with uninsulated leaf; heat conducted to the non-fire side.")

seg(id="ht3", sec="04", kicker="04 · HEAT TRANSFER", title="Convection: Smoke Is the Delivery System",
    sub="Newton's law of cooling, and the buoyant transport of energy",
    layout="equation",
    visual=("convection_diagram", {}),
    bullets=["q = h A ΔT — heat carried by a moving fluid.",
             "Hot gases expand, become buoyant and rise.",
             "Most fire energy leaves the compartment through openings as hot gas.",
             "Smoke movement, not flame spread, is usually how fire reaches a new floor."],
    narr=("Convection is heat carried by a moving fluid. Newton's law of cooling expresses it simply: heat flow equals a convective coefficient, "
          "times the area, times the temperature difference between the surface and the gas. "
          "In fire, convection is dominated by buoyancy. Hot products of combustion are less dense than the surrounding air, so they rise, "
          "entraining air as they go, and form a plume. That plume strikes the ceiling and spreads as a hot layer. "
          "Where that layer finds a stair, a shaft, a duct or a roof void, it carries heat and toxic products to places the flame never reached. "
          "In a compartment fire, the majority of energy leaves through the openings in the form of hot gas. "
          "This is why we say that smoke is the conveyor belt of the fire."),
    note="Link convection to smoke control strategy later.")

seg(id="ht4", sec="04", kicker="04 · HEAT TRANSFER", title="Radiation: The Distance Threat",
    sub="Stefan–Boltzmann law: radiative power grows with the fourth power of temperature",
    layout="equation",
    visual=("radiation_diagram", {}),
    bullets=["q″ = ε σ (T₁⁴ − T₂⁴), with temperature in kelvin.",
             "Double the absolute temperature: sixteen times the radiative power.",
             "Radiant heat travels line of sight: it ignites what it can see.",
             "At 20 kW/m², protected skin reaches pain in about 5 s; bare skin blisters in seconds."],
    narr=("Radiation is the transfer of energy by electromagnetic waves, and it needs no medium. "
          "The Stefan-Boltzmann law tells us that radiative power is proportional to the fourth power of absolute temperature. "
          "That fourth power is why fire is so non-linear. Double the absolute temperature of a surface and it radiates sixteen times as much energy. "
          "It also explains why radiant heat is a line-of-sight threat: it ignites the surfaces it can see, and a simple barrier eliminates it. "
          "For people, the thresholds are brutal. At two and a half kilowatts per square metre we can work for a short time. "
          "At twenty kilowatts per square metre, protected skin gives pain in about five seconds and unprotected skin blisters in seconds. "
          "Flashover is defined partly by reaching that figure at floor level."),
    note="Numbers to memorise: 2.5, 5, 20 kW/m².")

seg(id="ht5", sec="04", kicker="04 · HEAT TRANSFER", title="Reading a Fire Through Its Heat Paths",
    sub="A single burning pallet, traced through three modes",
    layout="split",
    visual=("heat_path_trace", {}),
    bullets=["Plume convects heat to the ceiling; the layer radiates down.",
             "Steel rack conducts heat into the next tier of storage.",
             "Radiation preheats the neighbouring rack; ignition follows.",
             "Each path suggests a different intervention."],
    narr=("Let us trace a single burning pallet in a warehouse. The flame convects heat upward, the ceiling jet spreads it laterally, "
          "and within a minute a hot layer is forming over the whole aisle. That layer radiates downward onto the pallets below, "
          "preheating them without any flame contact. "
          "At the same time the steel upright of the rack conducts heat into the next tier, and radiant heat from the flame preheats the rack opposite. "
          "Within a few minutes the second rack ignites, and now we have two fire sources entraining air from the same aisle. "
          "Each heat path points to a different intervention: cool the layer, cool the steel, cool the exposure, or control the air. "
          "Good tactics cool the path that is actually driving the fire, not simply the flame that is visible."),
    note="This slide is the tactical hinge of section 4.")
