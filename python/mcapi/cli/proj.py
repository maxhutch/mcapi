import sys
from mcapi import get_all_projects
from mcapi.cli.list_objects import ListObjects
from mcapi.cli.functions import _trunc_name, _proj_path, _format_mtime, _proj_config

class ProjSubcommand(ListObjects):
    def __init__(self):
        super(ProjSubcommand, self).__init__("proj", "Project", "Projects", 
            requires_project=False, proj_member=False, expt_member=False,
            list_columns=['current', 'name', 'owner', 'id', 'mtime'],
            headers=['', 'name', 'owner', 'id', 'mtime'],
            deletable=True)
    
    def get_all_from_experiment(self, expt):
        raise Exception("Projects are not members of experiments")
    
    def get_all_from_project(self, proj):
        raise Exception("Projects are not members of projects")
    
    def get_all(self):
        projs = get_all_projects()
        # TODO: not sure why this is happening?
        for p in projs:
            if p.input_data['id'] is id:
                p.input_data['id'] = p.id
        return projs
    
    def list_data(self, obj):
        _is_current = ' '
        if _proj_path() is not None:
            with open(_proj_config()) as f:
                j = json.load(f)
            if obj.id == j['project_id']:
                _is_current = '*'
        
        return {
            'current':_is_current,
            'owner': obj.owner,
            'name': _trunc_name(obj),
            'id': obj.id,
            'mtime': _format_mtime(obj.mtime)
        }
    
    def delete(self, objects, dry_run, out=sys.stdout):
        pp = PrettyPrint(shift=shift, indent=indent, out=out)
        
        msg = ""
        if dry_run:
            msg = "(Dry-run)"
        pp.write("Deleting projects " + msg + "\n")
        for obj in objects:
            pp.write("name:", pp.str(obj.name))
            pp.n_indent += 1
            obj.delete(dry_run=dry_run)
            pp.write("delete_tally:")
            pp.n_indent += 1
            for key, val in proj.delete_tally.__dict__.iteritems():
                pp.write(key + ": " + pp.str(val))
            pp.n_indent -= 1
            pp.write("")
            pp.n_indent += 1
            

    
