import os
from GDB_manager import GDB_Manager
from dotenv import load_dotenv
load_dotenv()

NEO4J_NAME = str(os.getenv("NEO4J_DB_NAME"))
NEO4J_USER = str(os.getenv("NEO4J_DB_USER"))
NEO4J_PASS = str(os.getenv("NEO4J_DB_PASS"))
NEO4J_URI = str(os.getenv("NEO4J_DB_URI"))

client = GDB_Manager(NEO4J_URI, NEO4J_USER, NEO4J_PASS)

query = """
    /* === MERGE all nodes (idempotent node creation) === */

/* Subatomic particle: proton */
MERGE (proton:SubatomicParticle {id:'proton'})
  SET proton.name='Proton',
      proton.symbol='p',
      proton.alternativeSymbols=['p','p+','1H+'],
      proton.electricCharge_e = 1.0,
      proton.mass_kg = 1.67262192595e-27,
      proton.mass_Da = 1.0072764665789,
      proton.mass_MeV_c2 = 938.27208943,
      proton.protonToElectronMassRatio = 1836.0,
      proton.chargeRadius_m = 0.84075e-15,
      proton.meanLifetime_years = 9.6e32,
      proton.electricDipoleMoment_e_cm = 2.1e-25,
      proton.electricPolarizability_fm3 = 0.00112,
      proton.magneticMoment_J_T = 1.41060679545e-26,
      proton.spin_hbar = '1/2',
      proton.isospin = '1/2',
      proton.parity = '+1',
      proton.statistics = 'Fermionic',
      proton.family = 'Hadron',
      proton.compositionText = 'two up quarks (u), one down quark (d)';

/* Quarks (valence) */
MERGE (upQuark:Quark {id:'up_quark'}) 
  SET upQuark.name='Up quark', upQuark.charge_e = 0.6666667, upQuark.note='valence quark in proton';

MERGE (downQuark:Quark {id:'down_quark'}) 
  SET downQuark.name='Down quark', downQuark.charge_e = -0.3333333, downQuark.note='valence quark in proton';

/* Antiparticle */
MERGE (antiproton:SubatomicParticle {id:'antiproton'}) 
  SET antiproton.name='Antiproton', antiproton.electricCharge_e = -1.0;

/* Interactions */
MERGE (gravity:Interaction {id:'gravity'}) SET gravity.name='Gravity';
MERGE (electromagnetic:Interaction {id:'electromagnetic'}) SET electromagnetic.name='Electromagnetic';
MERGE (weak:Interaction {id:'weak'}) SET weak.name='Weak';
MERGE (strong:Interaction {id:'strong'}) SET strong.name='Strong (QCD)';

/* People (historical/theoretical) */
MERGE (goldstein:Person {id:'eugen_goldstein'}) SET goldstein.name='Eugen Goldstein';
MERGE (rutherford:Person {id:'ernest_rutherford'}) SET rutherford.name='Ernest Rutherford';
MERGE (prout:Person {id:'william_prout'}) SET prout.name='William Prout';

/* Facility / experiment */
MERGE (LHC:Facility {id:'LHC'}) SET LHC.name='Large Hadron Collider';

/* Uses / applications as simple nodes */
MERGE (protonTherapy:Experiment {id:'proton_therapy'}) SET protonTherapy.name='Proton therapy';
MERGE (particleExperiments:Experiment {id:'particle_physics_experiments'}) SET particleExperiments.name='Particle physics experiments';

/* === CREATE relationships using MATCH + MERGE (active-voice verbs & relationship properties) === */

/* Composition: proton COMPOSE_OF upQuark (2) and downQuark (1) */
MATCH (proton:SubatomicParticle {id:'proton'}), (upQuark:Quark {id:'up_quark'})
MERGE (proton)-[:COMPOSE_OF {count:2, role:'valence'}]->(upQuark);

MATCH (proton:SubatomicParticle {id:'proton'}), (downQuark:Quark {id:'down_quark'})
MERGE (proton)-[:COMPOSE_OF {count:1, role:'valence'}]->(downQuark);

/* Proton classification: proton CLASSIFY_AS properties (family/statistics etc.) - use relationships to Property nodes */
MERGE (hadronProp:Property {id:'hadron'}) SET hadronProp.name='Hadron';
MERGE (baryonProp:Property {id:'baryon'}) SET baryonProp.name='Baryon';
MERGE (fermionProp:Property {id:'fermionic'}) SET fermionProp.name='Fermionic';

MATCH (proton:SubatomicParticle {id:'proton'}), (hadronProp:Property {id:'hadron'})
MERGE (proton)-[:CLASSIFY_AS {source:'Wikipedia intro'}]->(hadronProp);

MATCH (proton:SubatomicParticle {id:'proton'}), (baryonProp:Property {id:'baryon'})
MERGE (proton)-[:CLASSIFY_AS {source:'Wikipedia intro'}]->(baryonProp);

MATCH (proton:SubatomicParticle {id:'proton'}), (fermionProp:Property {id:'fermionic'})
MERGE (proton)-[:CLASSIFY_AS {source:'Wikipedia intro'}]->(fermionProp);

/* Interactions the proton participates in (active: proton INTERACT_BY interaction) */
MATCH (proton:SubatomicParticle {id:'proton'}), (gravity:Interaction {id:'gravity'})
MERGE (proton)-[:INTERACT_BY {strength:'very weak (relative)'}]->(gravity);

MATCH (proton:SubatomicParticle {id:'proton'}), (electromagnetic:Interaction {id:'electromagnetic'})
MERGE (proton)-[:INTERACT_BY {strength:'electromagnetic (due to +1 e)'}]->(electromagnetic);

MATCH (proton:SubatomicParticle {id:'proton'}), (weak:Interaction {id:'weak'})
MERGE (proton)-[:INTERACT_BY {strength:'weak interaction'}]->(weak);

MATCH (proton:SubatomicParticle {id:'proton'}), (strong:Interaction {id:'strong'})
MERGE (proton)-[:INTERACT_BY {strength:'strong (QCD), binds quarks'}]->(strong);

/* Antiparticle relation (active voice) */
MATCH (proton:SubatomicParticle {id:'proton'}), (antiproton:SubatomicParticle {id:'antiproton'})
MERGE (proton)-[:ANTAGONIST_OF {note:'antiparticle'}]->(antiproton);

/* Historical discovery & naming (active voice) */
/* Goldstein observed H+ (1886) as an ion in discharge tubes — associate year on the DISCOVER relation */
MATCH (goldstein:Person {id:'eugen_goldstein'}), (proton:SubatomicParticle {id:'proton'})
MERGE (goldstein)-[:DISCOVER {year:1886, note:'observed H+ (ion) in discharge experiments'}]->(proton);

/* Rutherford identified the hydrogen nucleus as proton and named/defined it (1920) */
/* Article: name given by Rutherford in 1920 — attach NAME relation */
MATCH (rutherford:Person {id:'ernest_rutherford'}), (proton:SubatomicParticle {id:'proton'})
MERGE (rutherford)-[:NAME {year:1920, note:'named hydrogen nucleus "proton", Greek for \"first\"'}]->(proton);

/* Prout's hypothesis (theorized in 1815) */
MATCH (prout:Person {id:'william_prout'}), (proton:SubatomicParticle {id:'proton'})
MERGE (prout)-[:THEORIZE {year:1815, note:'early conjecture about atomic building blocks (Prout hypothesis)'}]->(proton);

/* Proton occurrence: proton PRESENT_IN every atomic nucleus (encode as relation to a general Atom node) */
MERGE (atom:Entity {id:'atom', name:'Atom'})
MATCH (proton:SubatomicParticle {id:'proton'}), (atom:Entity {id:'atom'})
MERGE (proton)-[:PRESENT_IN {scope:'atomic_nuclei', note:'one or more protons present in nucleus of every atom'}]->(atom);

/* Proton role: proton ENABLE (or PROVIDE) electrostatic central force binding electrons */
MERGE (electrostaticForce:Property {id:'electrostatic_central_force'}) SET electrostaticForce.name='Electrostatic central force';
MATCH (proton:SubatomicParticle {id:'proton'}), (electrostaticForce:Property {id:'electrostatic_central_force'})
MERGE (proton)-[:PROVIDE {role:'binds atomic electrons', note:'protons provide attractive electrostatic force that binds electrons'}]->(electrostaticForce);

/* Proton applications: proton USED_IN experiments & therapy */
MATCH (proton:SubatomicParticle {id:'proton'}), (LHC:Facility {id:'LHC'})
MERGE (proton)-[:USED_IN {context:'particle_accelerators', note:'routinely used for accelerators; LHC is major facility example'}]->(LHC);

MATCH (proton:SubatomicParticle {id:'proton'}), (protonTherapy:Experiment {id:'proton_therapy'})
MERGE (proton)-[:USED_IN {context:'medical', note:'used for proton therapy'}]->(protonTherapy);

MATCH (proton:SubatomicParticle {id:'proton'}), (particleExperiments:Experiment {id:'particle_physics_experiments'})
MERGE (proton)-[:USED_IN {context:'research', note:'used in particle physics experiments'}]->(particleExperiments);

/* Proton mass relation to neutron and electron (express ratios / approximate facts) */
MERGE (neutron:SubatomicParticle {id:'neutron'}) SET neutron.name='Neutron';
MATCH (proton:SubatomicParticle {id:'proton'}), (neutron:SubatomicParticle {id:'neutron'})
MERGE (proton)-[:COMPARE {to:'neutron', note:'mass slightly less than neutron'}]->(neutron);

MERGE (electron:SubatomicParticle {id:'electron'}) SET electron.name='Electron';
MATCH (proton:SubatomicParticle {id:'proton'}), (electron:SubatomicParticle {id:'electron'})
MERGE (proton)-[:COMPARE {to:'electron', ratio:1836.0, note:'proton approximately 1836 times the mass of electron'}]->(electron);

/* Quark-level information: indication that quark rest masses contribute ~1% of proton mass (store as an annotation) */
MATCH (proton:SubatomicParticle {id:'proton'}), (upQuark:Quark {id:'up_quark'}), (downQuark:Quark {id:'down_quark'})
MERGE (proton)-[:ANNOTATE {note:'rest masses of quarks contribute about 1% of proton mass; remaining mass from QCD binding energy'}]->(upQuark)
MERGE (proton)-[:ANNOTATE {note:'rest masses of quarks contribute about 1% of proton mass; remaining mass from QCD binding energy'}]->(downQuark);

/* Proton charge radius measurement note (two measurement kinds give slightly different values) */
MATCH (proton:SubatomicParticle {id:'proton'})
MERGE (proton)-[:MEASURE {property:'charge_radius', value_meters:0.84075e-15, note:'charge radius; different measurement methods produce slightly different values'}]->(proton);

/* Magnetic / electric property relations */
MATCH (proton:SubatomicParticle {id:'proton'})
MERGE (proton)-[:HAS_PROPERTY {name:'magneticMoment_J_T', value:1.41060679545e-26, unit:'J T^-1'}]->(proton);

MATCH (proton:SubatomicParticle {id:'proton'})
MERGE (proton)-[:HAS_PROPERTY {name:'electricPolarizability_fm3', value:0.00112, unit:'fm^3'}]->(proton);

/* Antiparticle discovery/classification: antiproton as antiparticle (no year given in article for antiproton discovery) */
MATCH (antiproton:SubatomicParticle {id:'antiproton'}), (proton:SubatomicParticle {id:'proton'})
MERGE (antiproton)-[:ANTAGONIST_OF {note:'antiproton is antiparticle of proton'}]->(proton);



"""

output = client.run_dump(query)
print(f"GDB back with: {output}")
client.close()