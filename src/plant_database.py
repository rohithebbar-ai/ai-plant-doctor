# plant_database.py - Comprehensive Plant Health Knowledge Base

class PlantDatabase:
    def __init__(self):
        """Initialize comprehensive plant health database with diseases, treatments, and advice"""
        
        self.conditions = {
            # ===== FUNGAL DISEASES =====
            "fungal_leaf_spot": {
                "name": "Fungal Leaf Spot",
                "symptoms": ["spots", "browning", "circular_lesions", "blackening"],
                "keywords": ["brown spots", "circular", "lesions", "fungal", "spots with halos"],
                "description": "Common fungal infection causing circular spots on leaves with yellow halos",
                "treatments": [
                    {
                        "type": "fungicide",
                        "action": "Apply copper-based fungicide",
                        "details": [
                            "Spray every 7-14 days until symptoms improve",
                            "Apply in early morning or evening to avoid leaf burn",
                            "Ensure complete leaf coverage including undersides"
                        ],
                        "products": ["Copper sulfate", "Copper hydroxide", "Bordeaux mixture"]
                    },
                    {
                        "type": "cultural",
                        "action": "Improve plant hygiene and air circulation",
                        "details": [
                            "Remove affected leaves immediately and dispose (don't compost)",
                            "Clean up fallen debris around plants",
                            "Increase spacing between plants for air flow",
                            "Water at soil level, avoid wetting leaves"
                        ]
                    },
                    {
                        "type": "organic",
                        "action": "Use organic fungicides",
                        "details": [
                            "Neem oil spray every 7-10 days",
                            "Baking soda solution (1 tsp per quart water)",
                            "Compost tea spray for beneficial microorganisms"
                        ]
                    }
                ],
                "prevention": [
                    "Choose disease-resistant plant varieties",
                    "Avoid overhead watering, use drip irrigation",
                    "Ensure good air circulation around plants",
                    "Don't work with plants when they're wet",
                    "Rotate crops annually in vegetable gardens"
                ],
                "common_plants": ["tomato", "rose", "pepper", "cucumber", "bean", "squash"],
                "severity_indicators": ["spreading rapidly", "multiple leaves affected", "defoliation"],
                "seasonal_info": "Most common in warm, humid conditions (spring/summer)",
                "recovery_time": {"mild": "1-2 weeks", "moderate": "2-4 weeks", "severe": "4-8 weeks"}
            },
            
            "rust_disease": {
                "name": "Rust Disease",
                "symptoms": ["rust_colored", "spots", "reddening", "powdery", "yellow_spots"],
                "keywords": ["rust", "orange", "pustules", "reddish", "orange powder", "spores"],
                "description": "Fungal disease causing orange/rust colored pustules, often on leaf undersides",
                "treatments": [
                    {
                        "type": "fungicide",
                        "action": "Apply systemic fungicide",
                        "details": [
                            "Use triazole-based fungicides (myclobutanil, propiconazole)",
                            "Apply every 10-14 days during active infection",
                            "Rotate fungicide types to prevent resistance",
                            "Apply preventively in high-risk periods"
                        ]
                    },
                    {
                        "type": "removal",
                        "action": "Remove infected plant parts",
                        "details": [
                            "Prune affected leaves and stems immediately",
                            "Dispose of infected material in trash (not compost)",
                            "Disinfect pruning tools with 70% alcohol between cuts",
                            "Thin plants to improve air circulation"
                        ]
                    }
                ],
                "prevention": [
                    "Plant rust-resistant varieties when available",
                    "Avoid overcrowding plants",
                    "Water early in the day so leaves dry quickly",
                    "Remove alternate hosts (wild plants that harbor rust)",
                    "Apply preventive fungicide sprays in susceptible plants"
                ],
                "common_plants": ["wheat", "corn", "beans", "hollyhock", "snapdragon", "rose", "apple", "cedar"],
                "recovery_time": {"mild": "2-3 weeks", "moderate": "4-6 weeks", "severe": "6-12 weeks"}
            },
            
            "powdery_mildew": {
                "name": "Powdery Mildew",
                "symptoms": ["powdery", "fuzzy_growth", "yellowing", "white_coating"],
                "keywords": ["white powder", "dusty", "mildew", "cottony", "flour-like", "white coating"],
                "description": "Fungal disease creating white powdery coating on leaves, stems, and buds",
                "treatments": [
                    {
                        "type": "organic",
                        "action": "Apply baking soda solution",
                        "details": [
                            "Mix 1 tsp baking soda + 1/2 tsp liquid soap per quart water",
                            "Spray weekly on affected areas",
                            "Apply in evening to avoid leaf burn"
                        ]
                    },
                    {
                        "type": "fungicide",
                        "action": "Use sulfur-based fungicide",
                        "details": [
                            "Apply sulfur dust or wettable sulfur spray",
                            "Don't apply when temperature exceeds 85°F (30°C)",
                            "Repeat every 7-10 days until symptoms disappear"
                        ]
                    },
                    {
                        "type": "biological",
                        "action": "Apply beneficial microorganisms",
                        "details": [
                            "Use Bacillus subtilis-based products",
                            "Apply milk spray (1 part milk to 10 parts water)",
                            "Encourage beneficial soil microbes with compost"
                        ]
                    }
                ],
                "prevention": [
                    "Improve air circulation around plants",
                    "Avoid overhead watering",
                    "Plant in full sun locations when possible",
                    "Remove infected plant debris regularly",
                    "Choose resistant cultivars"
                ],
                "common_plants": ["cucumber", "squash", "pumpkin", "rose", "grape", "zinnia", "phlox", "lilac"],
                "recovery_time": {"mild": "1-2 weeks", "moderate": "2-4 weeks", "severe": "4-6 weeks"}
            },
            
            "anthracnose": {
                "name": "Anthracnose",
                "symptoms": ["dark_spots", "sunken_lesions", "browning", "wilting"],
                "keywords": ["dark lesions", "sunken spots", "anthracnose", "cankers"],
                "description": "Fungal disease causing dark, sunken lesions on leaves, stems, and fruits",
                "treatments": [
                    {
                        "type": "fungicide",
                        "action": "Apply copper or chlorothalonil fungicide",
                        "details": [
                            "Begin applications at first sign of disease",
                            "Spray every 7-14 days during wet weather",
                            "Ensure good coverage of all plant surfaces"
                        ]
                    }
                ],
                "prevention": [
                    "Avoid overhead irrigation",
                    "Provide good air circulation",
                    "Remove and destroy infected plant debris",
                    "Plant resistant varieties"
                ],
                "common_plants": ["tomato", "pepper", "cucumber", "bean", "strawberry", "grape"],
                "recovery_time": {"mild": "2-3 weeks", "moderate": "3-5 weeks", "severe": "6-10 weeks"}
            },
            
            "downy_mildew": {
                "name": "Downy Mildew",
                "symptoms": ["yellowing", "fuzzy_growth_underside", "wilting"],
                "keywords": ["downy", "fuzzy underside", "yellow patches", "grayish growth"],
                "description": "Fungal-like disease causing yellow patches with fuzzy growth on leaf undersides",
                "treatments": [
                    {
                        "type": "fungicide",
                        "action": "Apply systemic fungicide",
                        "details": [
                            "Use mancozeb or metalaxyl-based products",
                            "Apply every 7-10 days during cool, wet conditions",
                            "Spray early morning for best absorption"
                        ]
                    }
                ],
                "prevention": [
                    "Improve air circulation",
                    "Avoid overhead watering",
                    "Space plants properly",
                    "Remove infected debris"
                ],
                "common_plants": ["lettuce", "spinach", "cucumber", "grape", "rose"],
                "recovery_time": {"mild": "1-2 weeks", "moderate": "2-4 weeks", "severe": "4-8 weeks"}
            },
            
            "black_spot": {
                "name": "Black Spot",
                "symptoms": ["black_spots", "yellowing", "defoliation"],
                "keywords": ["black spots", "black lesions", "yellow halos", "rose disease"],
                "description": "Common rose disease causing black spots with yellow halos on leaves",
                "treatments": [
                    {
                        "type": "fungicide",
                        "action": "Apply preventive fungicide spray",
                        "details": [
                            "Use myclobutanil or tebuconazole",
                            "Start applications in early spring",
                            "Spray every 7-14 days during growing season"
                        ]
                    }
                ],
                "prevention": [
                    "Choose black spot resistant rose varieties",
                    "Provide good air circulation",
                    "Water at soil level",
                    "Clean up fallen leaves"
                ],
                "common_plants": ["rose"],
                "recovery_time": {"mild": "2-3 weeks", "moderate": "4-6 weeks", "severe": "season-long"}
            },
            
            # ===== BACTERIAL DISEASES =====
            "bacterial_spot": {
                "name": "Bacterial Spot",
                "symptoms": ["spots", "browning", "holes", "yellowing", "water_soaked"],
                "keywords": ["bacterial", "water-soaked", "angular", "lesions", "shot holes"],
                "description": "Bacterial infection causing dark spots with yellow halos, often with shot-hole appearance",
                "treatments": [
                    {
                        "type": "bactericide",
                        "action": "Apply copper bactericide",
                        "details": [
                            "Use copper hydroxide or copper sulfate",
                            "Apply every 7-10 days during wet weather",
                            "Start treatment early for best results",
                            "Add spreader-sticker for better coverage"
                        ]
                    },
                    {
                        "type": "cultural",
                        "action": "Improve growing conditions",
                        "details": [
                            "Reduce humidity around plants",
                            "Avoid working with wet plants",
                            "Use drip irrigation instead of sprinklers",
                            "Remove infected plant material immediately"
                        ]
                    }
                ],
                "prevention": [
                    "Use pathogen-free seeds and transplants",
                    "Rotate crops annually (3-4 year rotation)",
                    "Avoid overhead irrigation",
                    "Disinfect tools regularly",
                    "Don't save seeds from infected plants"
                ],
                "common_plants": ["tomato", "pepper", "peach", "plum", "cherry"],
                "recovery_time": {"mild": "2-3 weeks", "moderate": "3-6 weeks", "severe": "season-long damage"}
            },
            
            "fire_blight": {
                "name": "Fire Blight",
                "symptoms": ["wilting", "blackening", "shepherd_crook", "cankers"],
                "keywords": ["fire blight", "blackened shoots", "shepherd's crook", "bacterial"],
                "description": "Serious bacterial disease causing shoots to appear burned or scorched",
                "treatments": [
                    {
                        "type": "antibiotic",
                        "action": "Apply streptomycin during bloom",
                        "details": [
                            "Apply during bloom period for prevention",
                            "Use only as preventive measure",
                            "Follow label instructions carefully"
                        ]
                    },
                    {
                        "type": "pruning",
                        "action": "Remove infected branches",
                        "details": [
                            "Cut 12 inches below visible symptoms",
                            "Disinfect tools with 70% alcohol between cuts",
                            "Burn or dispose of infected material",
                            "Prune during dry weather"
                        ]
                    }
                ],
                "prevention": [
                    "Choose fire blight resistant varieties",
                    "Avoid high-nitrogen fertilizers",
                    "Don't prune during bloom",
                    "Remove suckers and water sprouts"
                ],
                "common_plants": ["apple", "pear", "quince", "crabapple"],
                "recovery_time": {"mild": "season-long", "severe": "may kill plant"}
            },
            
            "crown_gall": {
                "name": "Crown Gall",
                "symptoms": ["galls", "swelling", "tumor_growth"],
                "keywords": ["crown gall", "galls", "tumors", "swelling", "bacterial"],
                "description": "Bacterial disease causing tumor-like growths on roots and stems",
                "treatments": [
                    {
                        "type": "removal",
                        "action": "Remove infected plants",
                        "details": [
                            "Remove entire infected plant including roots",
                            "Don't compost infected material",
                            "Sterilize soil if possible",
                            "Wait 3-4 years before replanting susceptible species"
                        ]
                    }
                ],
                "prevention": [
                    "Inspect plants before purchasing",
                    "Avoid wounding plant roots and stems",
                    "Use biological control (Agrobacterium radiobacter K84)",
                    "Plant in well-draining soil"
                ],
                "common_plants": ["fruit trees", "roses", "grapes", "ornamental trees"],
                "recovery_time": {"any": "plant rarely recovers, prevention is key"}
            },
            
            # ===== VIRAL DISEASES =====
            "mosaic_virus": {
                "name": "Mosaic Virus",
                "symptoms": ["mosaic_pattern", "yellowing", "mottling", "stunting"],
                "keywords": ["mosaic", "mottled", "virus", "yellow-green pattern"],
                "description": "Viral disease causing mosaic or mottled yellow-green patterns on leaves",
                "treatments": [
                    {
                        "type": "removal",
                        "action": "Remove infected plants",
                        "details": [
                            "Remove entire infected plant immediately",
                            "Disinfect tools with 10% bleach solution",
                            "Control aphids and other virus vectors",
                            "Don't compost infected material"
                        ]
                    }
                ],
                "prevention": [
                    "Use virus-free seeds and plants",
                    "Control aphids and whiteflies",
                    "Remove weeds that can harbor viruses",
                    "Don't smoke around tomato plants"
                ],
                "common_plants": ["tomato", "pepper", "cucumber", "squash", "bean"],
                "recovery_time": {"any": "no cure - remove infected plants"}
            },
            
            "yellows_virus": {
                "name": "Yellows Virus",
                "symptoms": ["yellowing", "stunting", "witches_broom"],
                "keywords": ["yellows", "virus", "stunted", "witches broom"],
                "description": "Viral disease causing yellowing, stunting, and abnormal growth patterns",
                "treatments": [
                    {
                        "type": "removal",
                        "action": "Remove infected plants",
                        "details": [
                            "Remove infected plants immediately",
                            "Control leafhoppers (primary vector)",
                            "Use reflective mulches to deter insects"
                        ]
                    }
                ],
                "prevention": [
                    "Control leafhopper populations",
                    "Remove infected plants quickly",
                    "Use row covers on young plants"
                ],
                "common_plants": ["aster", "lettuce", "carrot", "celery"],
                "recovery_time": {"any": "no cure - remove infected plants"}
            },
            
            # ===== NUTRIENT DEFICIENCIES =====
            "nitrogen_deficiency": {
                "name": "Nitrogen Deficiency",
                "symptoms": ["yellowing", "lower_leaves", "stunting", "pale_green"],
                "keywords": ["pale", "chlorosis", "stunted", "yellow lower", "nitrogen"],
                "description": "Lack of nitrogen causing yellowing from bottom leaves upward and stunted growth",
                "treatments": [
                    {
                        "type": "fertilizer",
                        "action": "Apply nitrogen-rich fertilizer",
                        "details": [
                            "Use balanced NPK fertilizer with higher N (like 10-5-5)",
                            "Apply liquid fertilizer for quick results (fish emulsion, 20-20-20)",
                            "Side-dress with compost or aged manure",
                            "For quick fix: diluted liquid fertilizer every 2 weeks"
                        ]
                    },
                    {
                        "type": "organic",
                        "action": "Add organic nitrogen sources",
                        "details": [
                            "Apply well-aged chicken or cow manure",
                            "Use fish emulsion (diluted per label)",
                            "Add blood meal or feather meal to soil",
                            "Plant nitrogen-fixing cover crops"
                        ]
                    }
                ],
                "prevention": [
                    "Regular soil testing (annually)",
                    "Maintain proper soil pH (6.0-7.0 for most plants)",
                    "Add compost annually to improve soil structure",
                    "Follow proper fertilization schedule",
                    "Mulch to prevent nutrient leaching"
                ],
                "common_plants": ["vegetables", "annuals", "lawns", "leafy greens", "corn"],
                "recovery_time": {"mild": "1-2 weeks", "moderate": "2-4 weeks", "severe": "4-6 weeks"}
            },
            
            "potassium_deficiency": {
                "name": "Potassium Deficiency",
                "symptoms": ["leaf_edges", "browning", "yellowing", "weak_stems", "marginal_burn"],
                "keywords": ["brown edges", "marginal burn", "weak stems", "potassium", "scorched edges"],
                "description": "Potassium deficiency causing brown leaf edges, weak growth, and poor disease resistance",
                "treatments": [
                    {
                        "type": "fertilizer",
                        "action": "Apply potassium fertilizer",
                        "details": [
                            "Use potassium sulfate (sulfate of potash) - best for most plants",
                            "Apply muriate of potash (potassium chloride) for salt-tolerant plants",
                            "Use balanced fertilizer with adequate K (like 10-10-10)",
                            "Apply kelp meal for slow-release organic option"
                        ]
                    },
                    {
                        "type": "organic",
                        "action": "Add organic potassium sources",
                        "details": [
                            "Apply wood ash sparingly (raises pH)",
                            "Use granite dust for slow-release K",
                            "Add compost made with banana peels and other K-rich materials",
                            "Apply kelp meal or seaweed extract"
                        ]
                    }
                ],
                "prevention": [
                    "Regular soil testing to monitor K levels",
                    "Avoid over-fertilizing with nitrogen (can interfere with K uptake)",
                    "Maintain proper soil moisture (drought reduces K availability)",
                    "Add organic matter to improve nutrient retention",
                    "Test soil pH - K is less available in very acid or alkaline soils"
                ],
                "common_plants": ["tomato", "potato", "fruit trees", "flowers", "vegetables"],
                "recovery_time": {"mild": "2-3 weeks", "moderate": "3-5 weeks", "severe": "5-8 weeks"}
            },
            
            "phosphorus_deficiency": {
                "name": "Phosphorus Deficiency",
                "symptoms": ["purple_reddish", "stunting", "delayed_maturity", "dark_green"],
                "keywords": ["purple", "reddish", "phosphorus", "stunted", "dark green"],
                "description": "Phosphorus deficiency causing purple/reddish coloring, especially on older leaves",
                "treatments": [
                    {
                        "type": "fertilizer",
                        "action": "Apply phosphorus fertilizer",
                        "details": [
                            "Use bone meal for slow-release organic P",
                            "Apply rock phosphate for long-term P supply",
                            "Use high-P starter fertilizer (like 10-20-10)",
                            "Apply liquid phosphorus fertilizer for quick response"
                        ]
                    }
                ],
                "prevention": [
                    "Maintain soil pH between 6.0-7.0 for optimal P availability",
                    "Add organic matter to improve P release",
                    "Avoid over-watering which can leach P",
                    "Regular soil testing"
                ],
                "common_plants": ["corn", "tomato", "beans", "brassicas"],
                "recovery_time": {"mild": "2-4 weeks", "moderate": "4-6 weeks", "severe": "6-10 weeks"}
            },
            
            "iron_deficiency": {
                "name": "Iron Deficiency (Chlorosis)",
                "symptoms": ["yellowing", "between_veins", "green_veins", "new_growth"],
                "keywords": ["interveinal", "veins green", "iron chlorosis", "yellow between veins"],
                "description": "Iron deficiency causing yellowing between leaf veins while veins remain green",
                "treatments": [
                    {
                        "type": "supplement",
                        "action": "Apply iron chelate",
                        "details": [
                            "Use chelated iron (EDDHA, EDTA, or DTPA forms)",
                            "Apply to soil around root zone, not to leaves",
                            "Water in thoroughly after application",
                            "May need multiple applications 4-6 weeks apart"
                        ]
                    },
                    {
                        "type": "soil_amendment",
                        "action": "Improve soil conditions for iron uptake",
                        "details": [
                            "Lower soil pH if too alkaline (add sulfur)",
                            "Improve drainage if soil is waterlogged",
                            "Add organic matter like compost or peat moss",
                            "Avoid over-watering and over-fertilizing"
                        ]
                    }
                ],
                "prevention": [
                    "Maintain proper soil pH (6.0-6.8 for most plants)",
                    "Ensure good drainage to prevent root problems",
                    "Add organic matter annually",
                    "Use acidifying fertilizers for acid-loving plants",
                    "Avoid cultivating around roots"
                ],
                "common_plants": ["azalea", "rhododendron", "blueberry", "oak", "maple", "citrus"],
                "recovery_time": {"mild": "3-4 weeks", "moderate": "4-8 weeks", "severe": "8-12 weeks"}
            },
            
            "magnesium_deficiency": {
                "name": "Magnesium Deficiency",
                "symptoms": ["yellowing", "between_veins", "lower_leaves", "reddish"],
                "keywords": ["magnesium", "interveinal yellowing", "older leaves", "red tinge"],
                "description": "Magnesium deficiency causing yellowing between veins, starting with older leaves",
                "treatments": [
                    {
                        "type": "supplement",
                        "action": "Apply Epsom salt (magnesium sulfate)",
                        "details": [
                            "Dissolve 1-2 tablespoons per gallon water",
                            "Apply as soil drench around root zone",
                            "Can also spray on leaves (weaker solution)",
                            "Repeat every 2-3 weeks until symptoms improve"
                        ]
                    }
                ],
                "prevention": [
                    "Regular soil testing for Mg levels",
                    "Add compost with good Mg content",
                    "Avoid over-application of potassium (can interfere with Mg)",
                    "Maintain proper soil pH"
                ],
                "common_plants": ["tomato", "pepper", "rose", "citrus"],
                "recovery_time": {"mild": "2-3 weeks", "moderate": "3-5 weeks", "severe": "5-8 weeks"}
            },
            
            "calcium_deficiency": {
                "name": "Calcium Deficiency",
                "symptoms": ["blossom_end_rot", "tip_burn", "stunting"],
                "keywords": ["blossom end rot", "calcium", "tip burn", "black spots"],
                "description": "Calcium deficiency often appearing as blossom end rot in fruits or tip burn in leaves",
                "treatments": [
                    {
                        "type": "supplement",
                        "action": "Apply calcium amendments",
                        "details": [
                            "Add gypsum (calcium sulfate) to soil",
                            "Use lime if soil is also acidic",
                            "Apply liquid calcium for faster results",
                            "Ensure consistent soil moisture"
                        ]
                    }
                ],
                "prevention": [
                    "Maintain consistent soil moisture",
                    "Mulch to prevent moisture fluctuations",
                    "Add organic matter to improve calcium availability",
                    "Test and adjust soil pH if needed"
                ],
                "common_plants": ["tomato", "pepper", "apple", "lettuce"],
                "recovery_time": {"mild": "affects new growth in 2-4 weeks", "severe": "season-long issue"}
            },
            
            # ===== ENVIRONMENTAL STRESS =====
            "water_stress": {
                "name": "Water Stress",
                "symptoms": ["wilting", "leaf_edges", "browning", "curling", "dropping"],
                "keywords": ["drought", "overwatering", "root rot", "wilted", "water stress"],
                "description": "Stress from improper watering - either too much or too little water",
                "treatments": [
                    {
                        "type": "watering",
                        "action": "Adjust watering schedule",
                        "details": [
                            "Check soil moisture 2-3 inches deep before watering",
                            "Water deeply but less frequently",
                            "Ensure proper drainage - no standing water",
                            "For overwatered plants: stop watering temporarily"
                        ]
                    },
                    {
                        "type": "mulching",
                        "action": "Apply organic mulch",
                        "details": [
                            "Add 2-3 inches of organic mulch around plants",
                            "Keep mulch 2-3 inches away from plant stems",
                            "Use wood chips, straw, or shredded leaves",
                            "Helps retain moisture and regulate soil temperature"
                        ]
                    },
                    {
                        "type": "soil_improvement",
                        "action": "Improve soil structure",
                        "details": [
                            "Add compost to improve water retention in sandy soils",
                            "Add perlite or sand to improve drainage in clay soils",
                            "Create raised beds for better drainage",
                            "Install drip irrigation for consistent moisture"
                        ]
                    }
                ],
                "prevention": [
                    "Install drip irrigation or soaker hoses",
                    "Group plants by water needs",
                    "Improve soil with organic matter annually",
                    "Monitor soil moisture regularly",
                    "Use moisture meters for accuracy"
                ],
                "common_plants": ["all plants susceptible"],
                "recovery_time": {"mild": "3-7 days", "moderate": "1-2 weeks", "severe": "2-4 weeks or plant death"}
            },
            
            "heat_stress": {
                "name": "Heat Stress",
                "symptoms": ["wilting", "leaf_edges", "curling", "scorch", "sunburn"],
                "keywords": ["heat", "scorch", "sun scald", "temperature", "heat stress"],
                "description": "Stress from excessive heat or intense sun exposure",
                "treatments": [
                    {
                        "type": "shading",
                        "action": "Provide temporary shade",
                        "details": [
                            "Use shade cloth (30-50% shade)",
                            "Move containers to shadier locations",
                            "Create temporary shade with umbrellas or tarps",
                            "Water early morning and evening during heat waves"
                        ]
                    },
                    {
                        "type": "cooling",
                        "action": "Cool the environment",
                        "details": [
                            "Mist around plants (not on leaves) to cool air",
                            "Use reflective mulches to reduce soil temperature",
                            "Ensure adequate air circulation",
                            "Avoid fertilizing during heat stress"
                        ]
                    }
                ],
                "prevention": [
                    "Plant in appropriate locations for your climate",
                    "Provide afternoon shade in hot climates",
                    "Maintain consistent soil moisture",
                    "Use reflective or light-colored mulch",
                    "Choose heat-tolerant varieties"
                ],
                "common_plants": ["cool-season crops", "tender plants", "houseplants", "newly transplanted plants"],
                "recovery_time": {"mild": "1-3 days after cooling", "moderate": "1 week", "severe": "may cause permanent damage"}
            },
            
            "cold_stress": {
                "name": "Cold Stress/Frost Damage",
                "symptoms": ["blackening", "wilting", "water_soaked", "collapsed_tissue"],
                "keywords": ["frost", "freeze", "cold damage", "blackened", "frozen"],
                "description": "Damage from cold temperatures or frost exposure",
                "treatments": [
                    {
                        "type": "damage_assessment",
                        "action": "Assess and prune damage",
                        "details": [
                            "Wait until new growth appears to assess damage",
                            "Prune dead/damaged tissue back to healthy growth",
                            "Don't fertilize immediately - let plant recover",
                            "Provide protection from further cold"
                        ]
                    }
                ],
                "prevention": [
                    "Cover plants before predicted frost",
                    "Use row covers, blankets, or frost cloth",
                    "Water soil before cold nights (wet soil holds heat)",
                    "Plant cold-hardy varieties for your zone",
                    "Bring containers indoors or to protected areas"
                ],
                "common_plants": ["tender vegetables", "tropical plants", "young plants"],
                "recovery_time": {"mild": "2-4 weeks", "severe": "may not recover"}
            },
            
            # ===== PEST DAMAGE =====
            "insect_damage": {
                "name": "Insect Damage",
                "symptoms": ["holes", "chewed", "yellowing", "stippling", "distorted"],
                "keywords": ["eaten", "chewed", "holes", "pest", "insect", "bugs"],
                "description": "Damage caused by various insects feeding on plant leaves, stems, or roots",
                "treatments": [
                    {
                        "type": "organic_pesticide",
                        "action": "Apply organic insecticides",
                        "details": [
                            "Neem oil spray (affects soft-bodied insects)",
                            "Insecticidal soap for aphids, whiteflies, spider mites",
                            "Diatomaceous earth for crawling insects",
                            "Bt (Bacillus thuringiensis) for caterpillars"
                        ]
                    },
                    {
                        "type": "biological",
                        "action": "Encourage beneficial insects",
                        "details": [
                            "Plant flowers to attract ladybugs, lacewings, parasitic wasps",
                            "Avoid broad-spectrum pesticides that kill beneficials",
                            "Release beneficial insects if available locally",
                            "Provide habitat with diverse plantings"
                        ]
                    },
                    {
                        "type": "physical",
                        "action": "Physical pest control",
                        "details": [
                            "Hand-pick large insects like caterpillars",
                            "Use row covers to exclude flying pests",
                            "Apply sticky traps for flying insects",
                            "Spray aphids off with water hose"
                        ]
                    }
                ],
                "prevention": [
                    "Regular plant inspection (weekly during growing season)",
                    "Remove weeds that harbor pest insects",
                    "Use row covers on vulnerable young plants",
                    "Maintain healthy soil and plants for natural resistance",
                    "Rotate crops to break pest cycles"
                ],
                "common_plants": ["vegetables", "ornamentals", "fruit trees", "herbs"],
                "recovery_time": {"mild": "1-2 weeks", "moderate": "2-4 weeks", "severe": "4-8 weeks"}
            },
            
            "aphid_infestation": {
                "name": "Aphid Infestation",
                "symptoms": ["curling", "yellowing", "sticky_honeydew", "sooty_mold"],
                "keywords": ["aphids", "curled leaves", "sticky", "honeydew", "ants"],
                "description": "Small soft-bodied insects that suck plant juices, causing leaf curl and honeydew",
                "treatments": [
                    {
                        "type": "organic",
                        "action": "Apply insecticidal soap or neem oil",
                        "details": [
                            "Spray insecticidal soap every 3-5 days",
                            "Use neem oil spray in evening to avoid sun damage",
                            "Spray undersides of leaves where aphids hide",
                            "Rinse plants with water first to remove some aphids"
                        ]
                    },
                    {
                        "type": "biological",
                        "action": "Introduce natural predators",
                        "details": [
                            "Release ladybugs in garden",
                            "Plant flowers that attract lacewings",
                            "Encourage birds with bird houses and water",
                            "Plant dill, fennel, yarrow to attract beneficial wasps"
                        ]
                    }
                ],
                "prevention": [
                    "Inspect plants regularly, especially new growth",
                    "Use reflective mulches to confuse aphids",
                    "Avoid over-fertilizing with nitrogen",
                    "Remove aphid-infested weeds"
                ],
                "common_plants": ["roses", "vegetables", "fruit trees", "ornamentals"],
                "recovery_time": {"mild": "1 week", "moderate": "2-3 weeks", "severe": "3-4 weeks"}
            },
            
            "spider_mite_damage": {
                "name": "Spider Mite Damage",
                "symptoms": ["stippling", "yellowing", "webbing", "bronze_appearance"],
                "keywords": ["spider mites", "stippled", "bronze", "webbing", "tiny webs"],
                "description": "Microscopic pests causing stippled yellowing and fine webbing on leaves",
                "treatments": [
                    {
                        "type": "organic",
                        "action": "Increase humidity and use miticides",
                        "details": [
                            "Spray plants with water to increase humidity",
                            "Apply neem oil or insecticidal soap",
                            "Use predatory mites if available",
                            "Spray undersides of leaves thoroughly"
                        ]
                    }
                ],
                "prevention": [
                    "Maintain adequate humidity around plants",
                    "Avoid over-fertilizing with nitrogen",
                    "Inspect plants regularly with magnifying glass",
                    "Quarantine new plants before introducing to garden"
                ],
                "common_plants": ["houseplants", "vegetables", "fruit trees", "ornamentals"],
                "recovery_time": {"mild": "2-3 weeks", "moderate": "3-5 weeks", "severe": "5-8 weeks"}
            },
            
            "scale_insects": {
                "name": "Scale Insect Infestation",
                "symptoms": ["yellowing", "sticky_honeydew", "bumps_on_stems", "sooty_mold"],
                "keywords": ["scale", "bumps", "hard shells", "sticky", "honeydew"],
                "description": "Small insects with protective shells that attach to stems and leaves",
                "treatments": [
                    {
                        "type": "systemic",
                        "action": "Apply systemic insecticide",
                        "details": [
                            "Use horticultural oil during dormant season",
                            "Apply systemic insecticide (imidacloprid) to soil",
                            "Scrape off scales manually when possible",
                            "Use alcohol on cotton swab for small infestations"
                        ]
                    }
                ],
                "prevention": [
                    "Inspect plants before purchasing",
                    "Quarantine new plants",
                    "Maintain plant health to improve resistance",
                    "Regular monitoring of susceptible plants"
                ],
                "common_plants": ["citrus", "fruit trees", "ornamental trees", "houseplants"],
                "recovery_time": {"mild": "1-2 months", "severe": "season-long treatment needed"}
            },
            
            # ===== PHYSIOLOGICAL DISORDERS =====
            "sunscald": {
                "name": "Sunscald",
                "symptoms": ["white_patches", "bleached_areas", "papery_texture"],
                "keywords": ["sunscald", "bleached", "white patches", "sun damage"],
                "description": "Damage from intense sunlight causing bleached or white patches on leaves/fruits",
                "treatments": [
                    {
                        "type": "protection",
                        "action": "Provide shade protection",
                        "details": [
                            "Use shade cloth (30-50%)",
                            "Move containers to partial shade",
                            "Paint tree trunks with white latex paint",
                            "Gradually acclimate plants to full sun"
                        ]
                    }
                ],
                "prevention": [
                    "Gradually introduce plants to full sun",
                    "Provide afternoon shade in hot climates",
                    "Maintain adequate soil moisture",
                    "Choose appropriate varieties for your climate"
                ],
                "common_plants": ["tomatoes", "peppers", "citrus", "young trees"],
                "recovery_time": {"mild": "new growth normal in 2-4 weeks", "severe": "permanent damage to affected areas"}
            },
            
            "edema": {
                "name": "Edema (Oedema)",
                "symptoms": ["raised_bumps", "corky_spots", "blisters"],
                "keywords": ["edema", "blisters", "raised spots", "corky", "water-soaked"],
                "description": "Physiological disorder from overwatering causing raised, blister-like spots",
                "treatments": [
                    {
                        "type": "cultural",
                        "action": "Improve growing conditions",
                        "details": [
                            "Reduce watering frequency",
                            "Improve air circulation",
                            "Increase light levels if possible",
                            "Ensure proper drainage"
                        ]
                    }
                ],
                "prevention": [
                    "Avoid overwatering",
                    "Provide adequate light",
                    "Ensure good air circulation",
                    "Use well-draining soil"
                ],
                "common_plants": ["geraniums", "ivy", "cabbage", "cauliflower"],
                "recovery_time": {"mild": "new growth normal in 1-2 weeks"}
            }
        }
        
        # Enhanced treatment categories
        self.treatment_categories = {
            "emergency": {
                "name": "Emergency Actions",
                "urgency": "immediate",
                "icon": "🚨"
            },
            "fungicide": {
                "name": "Fungicide Treatment", 
                "urgency": "high",
                "icon": "💊"
            },
            "bactericide": {
                "name": "Bactericide Treatment",
                "urgency": "high", 
                "icon": "🦠"
            },
            "organic": {
                "name": "Organic Treatment",
                "urgency": "medium",
                "icon": "🌿"
            },
            "cultural": {
                "name": "Cultural Practice",
                "urgency": "medium",
                "icon": "🛠️"
            },
            "biological": {
                "name": "Biological Control",
                "urgency": "medium",
                "icon": "🐞"
            },
            "fertilizer": {
                "name": "Fertilizer Application",
                "urgency": "medium",
                "icon": "🌱"
            },
            "watering": {
                "name": "Water Management",
                "urgency": "high",
                "icon": "💧"
            }
        }
        
        # Comprehensive general advice templates
        self.general_advice = {
            "emergency": [
                "🚨 Remove severely affected plant parts immediately",
                "🧹 Clean up all fallen debris to prevent disease spread",
                "🔍 Isolate affected plants if possible",
                "📱 Consider consulting a local plant expert or extension service",
                "⏰ Take action within 24 hours to prevent further spread"
            ],
            "high_severity": [
                "⚠️ This condition requires prompt attention",
                "📋 Monitor plant closely for changes daily",
                "💧 Adjust watering practices as recommended",
                "🌬️ Improve air circulation around plant",
                "✂️ Remove affected leaves and dispose properly",
                "📸 Take photos to track progress"
            ],
            "moderate": [
                "📋 Monitor plant weekly for changes",
                "💧 Maintain consistent watering schedule", 
                "🌬️ Ensure adequate air circulation",
                "✂️ Remove affected plant material promptly",
                "🌱 Support plant health with proper nutrition",
                "🧹 Keep area clean and free of debris"
            ],
            "mild": [
                "👀 Keep an eye on the plant's progress",
                "💧 Maintain good watering practices",
                "🌱 Ensure plant has proper nutrition",
                "🧹 Practice good garden hygiene",
                "📅 Follow preventive care schedule"
            ],
            "preventive": [
                "🔍 Inspect plants weekly for early problem detection",
                "💧 Water consistently and appropriately for each plant type",
                "🌱 Maintain proper nutrition with regular fertilizing",
                "🧹 Keep garden area clean and tidy",
                "✂️ Prune properly to maintain plant health",
                "🌬️ Ensure good air circulation around plants",
                "📚 Learn about your specific plants' needs",
                "🦠 Practice disease prevention techniques"
            ],
            "seasonal": {
                "spring": [
                    "🌱 Start regular monitoring as plants become active",
                    "💊 Apply preventive treatments before problems start",
                    "🧹 Clean up winter debris that can harbor diseases",
                    "✂️ Prune damaged or dead growth from winter"
                ],
                "summer": [
                    "💧 Monitor watering needs closely in hot weather",
                    "🌡️ Watch for heat stress symptoms",
                    "🦠 Be vigilant for disease in humid conditions",
                    "🐛 Check for increased pest activity"
                ],
                "fall": [
                    "🧹 Clean up fallen leaves to prevent disease carryover",
                    "💧 Adjust watering as temperatures cool",
                    "🌱 Prepare plants for winter",
                    "✂️ Do final pruning before dormancy"
                ],
                "winter": [
                    "🏠 Protect tender plants from cold",
                    "💧 Reduce watering for dormant plants",
                    "📚 Plan for next year's prevention strategies",
                    "🔍 Monitor houseplants more closely"
                ]
            }
        }
        
        # Plant-specific advice
        self.plant_specific_advice = {
            "tomato": {
                "common_issues": ["blight", "blossom_end_rot", "hornworms"],
                "care_tips": [
                    "🍅 Provide consistent moisture to prevent blossom end rot",
                    "🌬️ Ensure good air circulation to prevent fungal diseases",
                    "✂️ Prune lower leaves to improve air flow",
                    "🎯 Use cages or stakes for support"
                ]
            },
            "rose": {
                "common_issues": ["black_spot", "powdery_mildew", "aphids"],
                "care_tips": [
                    "🌹 Water at soil level to keep leaves dry",
                    "✂️ Prune for good air circulation",
                    "🧹 Clean up fallen leaves regularly",
                    "🌱 Feed regularly during growing season"
                ]
            },
            "cucumber": {
                "common_issues": ["powdery_mildew", "bacterial_wilt", "cucumber_beetles"],
                "care_tips": [
                    "🥒 Provide consistent moisture",
                    "🌬️ Ensure good air circulation",
                    "🛡️ Use row covers early in season",
                    "🔄 Rotate crops annually"
                ]
            }
        }
    
    def get_condition(self, condition_name: str):
        """Get specific condition information"""
        return self.conditions.get(condition_name)
    
    def get_all_conditions(self):
        """Get all conditions in the database"""
        return self.conditions
    
    def search_by_symptoms(self, symptoms: list):
        """Find conditions matching given symptoms"""
        matches = []
        for name, condition in self.conditions.items():
            match_score = 0
            for symptom in symptoms:
                if symptom in condition["symptoms"]:
                    match_score += 2
                elif any(keyword in symptom for keyword in condition["keywords"]):
                    match_score += 1
            
            if match_score > 0:
                matches.append((name, condition, match_score))
        
        # Sort by match score
        return sorted(matches, key=lambda x: x[2], reverse=True)
    
    def get_general_advice(self, category: str):
        """Get general advice by category"""
        return self.general_advice.get(category, [])
    
    def get_seasonal_advice(self, season: str):
        """Get seasonal advice"""
        return self.general_advice.get("seasonal", {}).get(season, [])
    
    def get_plant_specific_advice(self, plant_type: str):
        """Get advice specific to plant type"""
        return self.plant_specific_advice.get(plant_type.lower(), {})
    
    def get_treatment_info(self, treatment_type: str):
        """Get information about treatment types"""
        return self.treatment_categories.get(treatment_type, {})
    
    def search_by_plant_type(self, plant_type: str):
        """Get conditions commonly affecting specific plant types"""
        matches = []
        plant_lower = plant_type.lower()
        
        for name, condition in self.conditions.items():
            if plant_lower in condition.get("common_plants", []):
                matches.append((name, condition))
        
        return matches
    
    def get_emergency_conditions(self):
        """Get conditions that require immediate attention"""
        emergency_conditions = []
        for name, condition in self.conditions.items():
            treatments = condition.get("treatments", [])
            if any(t.get("type") == "emergency" for t in treatments):
                emergency_conditions.append((name, condition))
        
        return emergency_conditions
    
    def get_organic_treatments_only(self):
        """Get conditions with organic treatment options"""
        organic_conditions = []
        for name, condition in self.conditions.items():
            treatments = condition.get("treatments", [])
            if any(t.get("type") in ["organic", "biological", "cultural"] for t in treatments):
                organic_conditions.append((name, condition))
        
        return organic_conditions