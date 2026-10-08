"""
Dataset Loader and Large-Scale News Corpus Generator for NewsSense
Generates and loads a realistic benchmark dataset of 8,000 news articles (1,000 per category)
across 8 distinct domains: Politics, Sports, Business, Technology, Entertainment, Science, Health, World.
"""

import os
import random
import itertools
import pandas as pd
from typing import Tuple

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DATASET_PATH = os.path.join(DATA_DIR, "news_dataset.csv")

CATEGORIES = [
    "Politics",
    "Sports",
    "Business",
    "Technology",
    "Entertainment",
    "Science",
    "Health",
    "World"
]

DOMAIN_COMPONENTS = {
    "Politics": {
        "subjects": [
            "The national parliament", "The prime minister and cabinet", "The parliamentary opposition coalition",
            "The supreme court constitutional bench", "The senate judiciary committee", "The federal election commission",
            "A bipartisan legislative taskforce", "The constitutional review council", "Regional state governors",
            "The parliamentary ethics committee", "Civil liberties advocacy groups", "The national assembly speaker",
            "Government ombudsman investigators", "The congressional budget office", "The electoral oversight council"
        ],
        "actions": [
            "passed landmark electoral reform legislation", "introduced a comprehensive anti-corruption integrity bill",
            "convened an emergency parliamentary debate on fiscal devolution", "issued a constitutional ruling on judicial tenure and voting rights",
            "launched a formal investigation into political campaign funding violations", "ratified new civil liberties protection standards",
            "held public hearings regarding bureaucratic transparency", "debated national infrastructure appropriation budgets",
            "proposed constitutional amendments on executive branch oversight", "announced biometric voter verification across polling stations",
            "reviewed state government revenue redistribution policies", "voted on amendments restricting corporate lobbying influence"
        ],
        "contexts": [
            "following weeks of intense legislative negotiations and partisan disputes", "in response to widespread public demand for institutional accountability",
            "amid heated arguments over federal authority versus regional autonomy", "ahead of the upcoming general elections scheduled for next spring",
            "after extensive constitutional analysis by senior legal scholars", "to modernize government procurement and prevent administrative fraud",
            "during a special late-night parliamentary voting session", "aiming to restore public trust in democratic legislative procedures"
        ],
        "outcomes": [
            "Lawmakers from both parties praised the statutory compromise as a vital step forward for democratic governance.",
            "Political commentators noted that the reform establishes strict legal penalties for ethics non-compliance.",
            "Constitutional experts highlighted that the bill strengthens judicial independence and citizen voting protections.",
            "Opposition party leaders indicated they will monitor executive implementation closely in parliamentary committees.",
            "The historic legislation is slated for formal presidential assent before taking effect nationwide next month."
        ]
    },
    "Sports": {
        "subjects": [
            "The national cricket team", "The defending premier league football champions", "The Olympic gold medalist swimmer",
            "The top-seeded grand slam tennis champion", "The national athletics squad", "The formula one championship racing team",
            "The national basketball federation", "The veteran rugby squad", "The badminton world tour titleholder",
            "The marathon world record holder", "The national gymnastic team", "The international football coaching staff"
        ],
        "actions": [
            "clinched a thrilling tournament championship victory", "secured a decisive late comeback win in the final minutes",
            "set an unprecedented world record time in the finals", "dominated match point rallies with exceptional tactical agility",
            "advanced to the international finals with an undefeated record", "executed a flawless defensive strategy against fierce rivals",
            "staged a dramatic fourth-quarter scoring blitz", "delivered a sensational winning goal in extra time",
            "outperformed veteran competitors with disciplined tactical precision", "overcame match deficits to lift the championship trophy",
            "demonstrated athletic excellence across all tournament fixtures", "unveiled comprehensive training protocols for the upcoming world games"
        ],
        "contexts": [
            "in front of a roaring capacity crowd at the national stadium", "during an electrifying and closely contested championship derby",
            "following grueling months of rigorous high-altitude conditioning", "under challenging weather conditions on the final day of the meet",
            "after a tense penalty shootout that kept spectators on the edge of their seats", "breaking decades of previous tournament statistical records",
            "to secure their seventh consecutive international championship crown", "earning unanimous praise from sports analysts and global broadcasters"
        ],
        "outcomes": [
            "The team captain commended the players' resilience, tactical discipline, and mental composure under pressure.",
            "Broadcasters declared the thrilling finish one of the most memorable sporting moments in tournament history.",
            "Head coaches highlighted the successful integration of youthful talent with veteran match leadership.",
            "The triumphant athletes will be honored in a celebratory national parade scheduled for next weekend.",
            "Sports scientists credited advanced biomechanics analysis and recovery protocols for the peak athletic performance."
        ]
    },
    "Business": {
        "subjects": [
            "The central monetary authority", "Global investment banking institutions", "Top-tier venture capital funds",
            "Multinational manufacturing conglomerates", "Leading e-commerce retail networks", "Institutional asset management firms",
            "Securities and exchange regulatory bodies", "Renewable energy infrastructure developers", "Supply chain logistics providers",
            "Corporate treasury management teams", "Commercial real estate investment trusts", "Financial technology fintech enterprises"
        ],
        "actions": [
            "held benchmark interest rates steady to control inflationary pressures", "reported record quarterly earnings exceeding analyst forecasts",
            "completed a multi-billion dollar cross-border corporate merger", "surged capital allocations into green energy transition portfolios",
            "expanded automated fulfillment logistics across metropolitan distribution hubs", "raised substantial Series B venture funding for cloud platforms",
            "rebalanced institutional portfolios toward high-yielding corporate bonds", "streamlined global supply chain operations to lower unit costs",
            "negotiated sovereign debt restructuring and international trade credits", "unveiled predictive demand forecasting software for inventory control",
            "experienced stock market valuation rallies driven by strong consumer demand", "diversified balance sheet assets into stable treasury yields"
        ],
        "contexts": [
            "amid fluctuating commodity prices and international currency exchange volatility", "driven by resilient recurring subscription revenues and consumer spending",
            "as institutional investors adjust risk exposure in emerging markets", "following favorable macroeconomic indicators and declining inflation prints",
            "to capture growing digital market share in high-growth commercial corridors", "in compliance with stringent new cross-border antitrust regulations",
            "during a period of rapid digital transformation across enterprise sectors", "positioning the firm for long-term sustainable margin expansion"
        ],
        "outcomes": [
            "Financial analysts upgraded the sector's outlook, projecting steady revenue compound annual growth rates.",
            "Chief financial officers emphasized rigorous balance sheet discipline and shareholder capital returns.",
            "Market indices responded positively with broad-based gains across industrial and technology equities.",
            "The strategic expansion is expected to generate significant operational synergies over the fiscal triennium.",
            "Economists noted that prudent monetary policy stance will support sustainable employment and price stability."
        ]
    },
    "Technology": {
        "subjects": [
            "Semiconductor engineering teams", "Leading cloud computing hyperscalers", "Cybersecurity research labs",
            "Autonomous electric vehicle designers", "Quantum computing software architects", "Artificial intelligence research labs",
            "Next-generation 6G telecommunications consortiums", "Open-source software developer foundations", "Decentralized blockchain protocol architects",
            "Edge computing device manufacturers", "Computer vision algorithm engineers", "Distributed systems research groups"
        ],
        "actions": [
            "unveiled a revolutionary 2nm microchip architecture with ultra-dense transistor gates", "open-sourced an advanced multi-modal foundation model for automated coding",
            "discovered and patched a critical zero-day vulnerability in network servers", "achieved fault-tolerant qubit coherence in quantum chemistry simulations",
            "completed autonomous highway pilot tests with multi-sensor LiDAR fusion", "deployed high-throughput distributed database engines with zero-knowledge proofs",
            "tested ultra-wideband millimeter wave wireless data transmission speeds", "optimized deep neural network inference latency on low-power edge silicon",
            "released an enterprise zero-trust identity verification and access management framework", "introduced hardware-accelerated machine learning APIs in mobile operating systems",
            "developed real-time ray-tracing rendering pipelines for interactive graphics", "scaled distributed microservice architectures across multi-region server clusters"
        ],
        "contexts": [
            "slashing energy consumption while doubling computational throughput", "enabling secure privacy-preserving computation for millions of daily active users",
            "demonstrating significant performance speedups over existing legacy platforms", "accelerating industrial automation and software development productivity",
            "under strict end-to-end cryptographic encryption and safety validation checks", "overcoming longstanding physical limits in microelectronic manufacturing",
            "to power the next generation of intelligent mobile and cloud computing systems", "setting new open benchmark standards across industry developer ecosystems"
        ],
        "outcomes": [
            "System architects highlighted that the technological breakthrough establishes a new standard for computing efficiency.",
            "Software engineers praised the modular developer SDKs and comprehensive documentation provided with the release.",
            "Industry experts anticipate widespread commercial adoption across cloud infrastructure and mobile consumer hardware.",
            "Peer-reviewed benchmark results confirmed a fourfold reduction in latency compared to previous generation chips.",
            "The technology platform has been submitted for formal open-source standardization by global engineering consortia."
        ]
    },
    "Entertainment": {
        "subjects": [
            "Acclaimed independent film directors", "Grammy-winning orchestral composers", "Global streaming entertainment platforms",
            "Celebrated Broadway theatrical companies", "Major international animation studios", "Renowned world cinema actors",
            "Interactive video game production studios", "Contemporary visual art curators", "Chart-topping recording artists",
            "International television production networks", "Cinematography guild adjudicators", "Documentary film festival juries"
        ],
        "actions": [
            "swept prestigious honors at the international film festival awards ceremony", "released a chart-topping symphonic album breaking worldwide digital streaming records",
            "debuted an acclaimed period drama series featuring historically authentic costumes", "staged a breathtaking theatrical revival with dynamic orchestral choreography",
            "launched an immersive open-world role-playing adventure with branching narratives", "received the lifetime achievement fellowship celebrating five decades of filmmaking",
            "announced a sold-out worldwide stadium concert tour with innovative visual effects", "produced a visually stunning animated feature combining handcrafted and 3D techniques",
            "premiered an investigative documentary capturing standing ovations from critics", "curated an expansive multimedia art installation exploring contemporary culture",
            "broke global box office weekend records with positive international critical reception", "collaborated with legendary session musicians on a genre-defining acoustic record"
        ],
        "contexts": [
            "earning standing ovations from audiences and near-universal acclaim from critics", "exploring profound human themes of resilience, identity, and personal discovery",
            "showcasing state-of-the-art cinematic sound design and photorealistic visual rendering", "redefining artistic conventions and setting fresh creative benchmarks in the medium",
            "combining masterful narrative storytelling with transformative lead performances", "delivering an unforgettable sensory experience to millions of viewers worldwide",
            "celebrating rich cultural heritage through contemporary musical interpretations", "marking a triumphant creative milestone in contemporary popular culture"
        ],
        "outcomes": [
            "Film critics praised the nuanced screenplay, evocative score, and masterful cinematography throughout the production.",
            "Audiences around the world took to social media to celebrate the emotional resonance and visual artistry of the release.",
            "Industry executives noted that the production demonstrates the enduring power of original creative storytelling.",
            "The soundtrack album climbed to the number one position on global streaming charts within hours of launch.",
            "The award-winning production has secured distribution agreements across more than eighty international theatrical territories."
        ]
    },
    "Science": {
        "subjects": [
            "Astrophysicists utilizing deep space orbital telescopes", "High-energy particle physics research teams", "Marine oceanographers and deep-sea researchers",
            "Planetary scientists analyzing Martian satellite radar data", "Atmospheric research scientists and climatologists", "Materials science laboratories",
            "Archaeological excavation expeditions", "Biophysicists studying macromolecular structures", "Quantum optics researchers",
            "Volcanology and seismology survey teams", "Paleontological researchers", "Space exploration flight dynamics engineers"
        ],
        "actions": [
            "captured high-resolution infrared observations of galaxies formed after the Big Bang", "detected rare subatomic particle decay anomalies in subterranean particle accelerators",
            "discovered uncharted hydrothermal vent ecosystems teeming with extremophile organisms", "confirmed extensive subsurface liquid water ice reservoirs on planetary plateaus",
            "synthesized a room-temperature crystal lattice exhibiting unique electronic properties", "published numerical climate models mapping stratospheric atmospheric circulation",
            "unearthed well-preserved hominin fossil remains dating back over two million years", "mapped atomic-scale structural conformations of transport proteins using cryo-EM",
            "measured gravitational wave signatures from coalescing binary neutron star systems", "demonstrated quantum entanglement transfer over record optical fiber distances",
            "reconstructed prehistoric climate cycles from deep polar ice core sediment samples", "analyzed mineral compositions of asteroid samples returned by robotic spacecraft"
        ],
        "contexts": [
            "challenging prevailing theoretical assumptions and expanding scientific knowledge", "providing novel empirical evidence for physics beyond established theoretical frameworks",
            "at depths exceeding four thousand meters beneath the ocean surface", "utilizing cutting-edge spectroscopy instrumentation and cryogenic detectors",
            "through years of rigorous collaborative field investigations across multiple continents", "opening revolutionary possibilities for next-generation energy and quantum devices",
            "published in leading peer-reviewed scientific journals after extensive replication", "advancing our fundamental understanding of cosmological origins and planetary evolution"
        ],
        "outcomes": [
            "Principal investigators stated that the findings open unprecedented research avenues in fundamental science.",
            "Independent research groups have commenced follow-up observational studies to replicate the experimental data.",
            "The breakthrough was hailed by national scientific academies as a milestone achievement in empirical discovery.",
            "Scientific funding councils announced expanded grants to support subsequent phases of the research program.",
            "The newly published observational datasets have been made openly accessible to the international scientific community."
        ]
    },
    "Health": {
        "subjects": [
            "Clinical oncology medical researchers", "Epidemiologists and infectious disease specialists", "Neuroscience and cognitive research institutes",
            "Cardiovascular medicine clinical investigators", "Public health immunization taskforces", "Biomedical engineering development teams",
            "Genomic medicine and CRISPR therapeutic laboratories", "Preventative medicine and lifestyle health researchers",
            "Pediatric healthcare research networks", "Clinical pharmacology research teams", "Mental health clinical trial investigators",
            "Diagnostic biomarker discovery consortia"
        ],
        "actions": [
            "reported remarkable tumor regression in Phase 3 oncology immunotherapy trials", "issued comprehensive evidence-based guidelines on antibiotic stewardship protocols",
            "identified novel blood-based neural biomarkers for early diagnostic screening of cognitive decline", "demonstrated significant reductions in cardiovascular mortality through targeted therapy",
            "developed a non-invasive wearable biosensor for real-time continuous glucose monitoring", "successfully applied gene-editing therapeutics to treat inherited hemoglobinopathies",
            "published a large-scale randomized clinical trial on preventative pediatric health interventions", "completed clinical evaluations of novel targeted monoclonal antibody therapies",
            "evaluated the clinical efficacy of structured cognitive behavioral interventions for anxiety", "established rapid diagnostic testing protocols for primary healthcare clinics",
            "conducted nationwide epidemiological surveys on nutritional health and chronic disease prevention", "validated artificial intelligence diagnostic tools for early radiographic anomaly detection"
        ],
        "contexts": [
            "demonstrating statistically significant improvements in long-term patient survival outcomes", "with rigorous double-blind randomized control methodologies across multiple hospitals",
            "without observing adverse off-target effects or significant clinical complications", "enabling timely medical intervention prior to the onset of severe chronic symptoms",
            "in accordance with international clinical practice standards and patient safety guidelines", "empowering patients with accessible real-time health data and automated alerts",
            "representing a transformative advancement for personalized precision medicine", "supported by collaborative international grants from leading health research foundations"
        ],
        "outcomes": [
            "Lead medical authors emphasized that the therapeutic regimen substantially improves quality of life for patients.",
            "Regulatory health authorities have granted accelerated review status for the breakthrough clinical treatment.",
            "Hospital physicians welcomed the standardized diagnostic protocol as a crucial advancement in preventative care.",
            "Patient advocacy organizations commended the research team for prioritizing accessible and equitable healthcare solutions.",
            "Further multi-center clinical trials are underway to evaluate long-term therapeutic durability across diverse populations."
        ]
    },
    "World": {
        "subjects": [
            "The United Nations General Assembly", "International diplomatic peace envoys", "Multilateral trade cooperation delegations",
            "International humanitarian relief agencies", "Foreign ministerial summits of leading global economies",
            "The African Union continental integration council", "Global food security and agricultural coalitions",
            "International maritime security coalitions", "Cross-border environmental protection taskforces",
            "Disaster response emergency coordination teams", "Global development finance institutions", "International civil aviation authorities"
        ],
        "actions": [
            "convened a high-level multilateral summit to finalize binding international climate accords", "brokered a historic ceasefire pact establishing demilitarized humanitarian corridors",
            "signed a comprehensive regional free trade agreement reducing tariffs across member states", "deployed emergency medical supplies and clean water purification units to disaster zones",
            "negotiated sovereign debt sustainability frameworks and multilateral development grants", "reopened vital maritime international shipping lanes under coordinated naval patrols",
            "unanimously adopted a unified declaration on clean energy infrastructure investment", "established an international grain reserve to protect vulnerable regions against supply shocks",
            "agreed on coordinated international standards for cross-border carbon accounting", "launched joint infrastructure development projects linking regional transportation corridors",
            "coordinated disaster relief efforts following severe seismic and meteorological events", "strengthened multilateral partnerships to promote sustainable economic development"
        ],
        "contexts": [
            "fostering diplomatic stability, mutual security, and sustainable economic growth across regions", "under the direct supervision of international peacekeeper monitoring teams",
            "to ensure the uninterrupted flow of essential humanitarian aid to affected civilian populations", "demonstrating the vital importance of collective multilateral diplomacy in resolving crises",
            "aligning international legal frameworks with sustainable development and environmental goals", "strengthening regional economic integration and cross-border commercial partnerships",
            "during high-level bilateral and plenary negotiations spanning multiple days", "reaffirming global commitment to international law, human dignity, and shared prosperity"
        ],
        "outcomes": [
            "Diplomatic delegates from participating nations expressed optimism for lasting regional cooperation and peace.",
            "The United Nations Secretary-General commended member states for demonstrating political will and diplomatic unity.",
            "Humanitarian organizations reported that relief supplies are reaching vulnerable communities without impediment.",
            "Economic analysts projected that the trade agreement will boost inter-regional commerce and job creation.",
            "Follow-up ministerial monitoring conferences have been scheduled to review compliance and milestone progress."
        ]
    }
}

ADDITIONAL_JOURNALISTIC_PREFIXES = [
    "According to comprehensive official reports released this morning, ",
    "In a detailed press briefing delivered before international correspondents, ",
    "Industry analysts and veteran observers noted that ",
    "Following extensive inter-agency consultations and policy reviews, ",
    "Recent investigative findings and empirical field surveys confirm that ",
    "During an extraordinary plenary session convened at the capital, ",
    "A formal investigative whitepaper published today revealed that ",
    "Speaking at the international symposium, senior delegates announced that ",
    "Key institutional stakeholders emphasized during the annual conference that ",
    "New authoritative data presented at the global summit demonstrate that "
]

ADDITIONAL_JOURNALISTIC_TRANSITIONS = [
    " Furthermore, extensive background analysis indicated that ",
    " In related proceedings, senior officials underlined that ",
    " Concurrently, independent assessment reports confirmed that ",
    " In addition to these measures, institutional delegates observed that ",
    " Simultaneously, technical evaluation teams verified that "
]


def generate_large_news_corpus(total_samples: int = 8000) -> pd.DataFrame:
    """
    Generates a deterministic, balanced dataset of exactly `total_samples` (e.g. 8,000 articles,
    1,000 per category) with authentic prose and rich domain terminology.
    """
    random.seed(42)
    per_category = total_samples // len(CATEGORIES)
    data = []

    print(f"Generating balanced corpus of {total_samples} articles ({per_category} per category across {len(CATEGORIES)} categories)...")

    for category in CATEGORIES:
        comp = DOMAIN_COMPONENTS[category]
        subjects = comp["subjects"]
        actions = comp["actions"]
        contexts = comp["contexts"]
        outcomes = comp["outcomes"]

        # Generate combinatorial distinct permutations
        generated_articles = set()
        
        while len(generated_articles) < per_category:
            s1 = random.choice(subjects)
            a1 = random.choice(actions)
            c1 = random.choice(contexts)
            o1 = random.choice(outcomes)
            prefix = random.choice(ADDITIONAL_JOURNALISTIC_PREFIXES)

            # Two-sentence structure with contextual depth
            if random.random() > 0.35:
                s2 = random.choice(subjects)
                a2 = random.choice(actions)
                trans = random.choice(ADDITIONAL_JOURNALISTIC_TRANSITIONS)
                text = f"{prefix}{s1.lower()} {a1} {c1}.{trans}{s2.lower()} {a2}. {o1}"
            else:
                text = f"{prefix}{s1.lower()} {a1} {c1}. {o1}"

            text = text.strip()
            if text not in generated_articles:
                generated_articles.add(text)
                data.append({
                    "category": category,
                    "text": text
                })

    df = pd.DataFrame(data)
    # Deterministic shuffle
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df


def ensure_large_dataset_exists(target_samples: int = 8000) -> str:
    """Ensures that the CSV dataset has target sample count on disk."""
    os.makedirs(DATA_DIR, exist_ok=True)
    regenerate = False
    
    if not os.path.exists(DATASET_PATH):
        regenerate = True
    else:
        try:
            existing_df = pd.read_csv(DATASET_PATH, encoding="utf-8")
            if len(existing_df) < target_samples:
                regenerate = True
        except Exception:
            regenerate = True

    if regenerate:
        df = generate_large_news_corpus(total_samples=target_samples)
        df.to_csv(DATASET_PATH, index=False, encoding="utf-8")
        print(f"Saved {len(df)} articles to {DATASET_PATH}")
    return DATASET_PATH


# Alias for backward compatibility
ensure_dataset_exists = ensure_large_dataset_exists


def load_dataset() -> pd.DataFrame:
    """Loads news dataset from CSV."""
    path = ensure_large_dataset_exists(target_samples=8000)
    df = pd.read_csv(path, encoding="utf-8")
    return df


def get_dataset_stats() -> dict:
    """Returns dataset summary statistics for dashboard and explorer."""
    df = load_dataset()
    category_counts = df['category'].value_counts().to_dict()
    
    word_counts = df['text'].apply(lambda t: len(str(t).split()))
    char_counts = df['text'].apply(lambda t: len(str(t)))
    
    return {
        "total_articles": len(df),
        "total_categories": len(category_counts),
        "categories": sorted(list(category_counts.keys())),
        "category_distribution": category_counts,
        "word_count_stats": {
            "mean": round(float(word_counts.mean()), 1),
            "min": int(word_counts.min()),
            "max": int(word_counts.max()),
            "median": round(float(word_counts.median()), 1)
        },
        "char_count_stats": {
            "mean": round(float(char_counts.mean()), 1),
            "min": int(char_counts.min()),
            "max": int(char_counts.max())
        }
    }


if __name__ == "__main__":
    ensure_large_dataset_exists(8000)
    stats = get_dataset_stats()
    print("Dataset Stats:", stats)
