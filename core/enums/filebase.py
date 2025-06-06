from core.libraries import *

@dataclass
class Dirs():
    appdata = os.getenv('APPDATA')
    main = os.path.join(appdata, 'denza.color-explorer')
    configs = os.path.join(main, 'configs')
    logs = os.path.join(main, 'logs')
    labs = os.path.join(main, 'labs')
    assets = os.path.join(main, 'assets')

@dataclass
class Files():
    data = os.path.join(Dirs.configs, 'data.json')
    langlab = os.path.join(Dirs.labs, 'langlab.json')
    #colorlab = os.path.join(Dirs.labs, 'colorlab.json')
    #iconlab = os.path.join(Dirs.labs, 'iconlab.json')
    #database = os.path.join(Dirs.main, 'database.json')