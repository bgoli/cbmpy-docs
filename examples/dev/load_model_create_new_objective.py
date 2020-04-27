"""
CBMPy (http://cbmpy.sourceforge.net/) example script

name: load_model_create_new_objective.py
description: Load two models and create a new objective function
licence: BSD 3.0
author: Brett G. Olivier PhD


(C) Brett G. Olivier, Amsterdam, 2020.

"""

# setup paths and imports

import os
cdir = os.path.dirname(os.path.abspath(os.sys.argv[0]))
mod_dir = os.path.join(cdir, '..', 'models')

print('Model path: {}'.format(os.path.abspath(mod_dir)))

import cbmpy

# Load two models: "core" (and core2) a small test model and "ecoli" a small Ecoli model.

core = cbmpy.loadModel(os.path.join(mod_dir, 'test_core.xml.zip'))
core2 = cbmpy.loadModel(os.path.join(mod_dir, 'test_core.xml.zip'))
eco = cbmpy.loadModel(os.path.join(mod_dir, 'test_eco.xml.zip'))

# Print the "core" active objective id and stoichiometry

print(core.getActiveObjective().getId())
print(core.getActiveObjectiveStoichiometry())

# Print the "ecoli" active objective id and stoichiometry

print(eco.getActiveObjective().getId())
print(eco.getActiveObjectiveStoichiometry())

# first note something that we need to consider, take a look at the "core"
# species ids and the ecoli objective reaction reagents.

print('\ncore species ids')
print(core.getSpeciesIds())
print('\necoli objective reactions')
print(eco.getReaction(eco.getActiveObjectiveReactionIds()[0]).getStoichiometry())

### Method 1: copying the reaction ###

# Note that there are no common metabolites! Now we copy the objective reaction
# (and its reagents) from "ecoli" to "core" and create a new objective.
# Check that you understand what createObjectiveFunction is doing.

cbmpy.CBMultiModel.copyReaction(eco, core, 'R_BIOMASS_Ecoli')
core.createObjectiveFunction('R_BIOMASS_Ecoli')

# Let's take a look at the new "core" model

print('\ncore species ids')
print(core.getSpeciesIds())
print('\necoli objective reactions')
print(eco.getReaction(eco.getActiveObjectiveReactionIds()[0]).getStoichiometry())

# Also note the status of the new species

[print('{} is fixed: {}'.format(s.getId(), s.is_boundary)) for s in core.species]

# Obviously you need to link the two models but I  leave that to you!

### Method 2: create a reaction from scratch ###

# create a new Reaction from scratch a
core2.createReaction('NewBiomass')
core2.createReactionReagent('NewBiomass', 'A', -1)
core2.createReactionReagent('NewBiomass', 'G', 1)
core2.getReaction('NewBiomass').getStoichiometry()
core2.getReaction('NewBiomass').getEquation()
core2.createObjectiveFunction('NewBiomass')

# get a reaction objectect and set a note.
R = core2.getReaction('NewBiomass')
R.setNotes("See notes on how I dealt with missing reagents.")

