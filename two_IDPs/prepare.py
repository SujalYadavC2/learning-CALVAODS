import os
from calvados.cfg import Config, Components

cwd = os.getcwd()
sysname = 'sim'

config = Config(
    sysname = sysname,
    box = [40,40,40], #nm
    temp = 273,
    pH = 7.5,
    ionic = 0.19,
    topol = 'random',

    wfreq = 7000,
    steps  = 1010*7000,   
    restart = 'checkpoint',
    frestart = 'restart.chk',
    verbose = True,
)

path = f'{cwd}/{sysname}'

config.write(path, 'config.yaml')

components = Components(
    molecule_type = 'protein',
    nmol=1,
    charge_termini='both',
    fresidues = f'{cwd}/input/residues_CALVADOS2.csv',
    ffasta = f'{cwd}/input/idr.fasta',
)

components.add(name='FUSRGG3')
components.add(name='aSyn')

components.write(path,'components.yaml')