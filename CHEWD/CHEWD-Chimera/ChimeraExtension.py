from chimera.extension import EMO, manager

class CHEWD_EMO(EMO):

        def name(self):
                return 'CHEWD'
        def description(self):
                return 'Molecular Surface Viewer for the residues wise energies'
        def categories(self):
                return ['Utilities']
        def icon(self):
                return None
        def activate(self):
                from chimera.dialogs import display
                display(self.module('gui').CHEWDDialog.name)
                return None

manager.registerExtension(CHEWD_EMO(__file__))