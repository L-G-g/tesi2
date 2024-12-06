from pymol import cmd, stored

def proxy_load():
    '''
DESCRIPTION

    Get polar interactions in a really easy way
    '''

    cmd.load("/home/gabi/tesi2/ligqrev_res/ligqrev/GIJ/GIJ_4HT2/4HT2.pdbqt", "protein_whole")
    cmd.load("/home/gabi/tesi2/ligqrev_res/ligqrev/GIJ/GIJ_4HT2/best.pdbqt", "best")
    cmd.dist("best_polar_conts","(best)","(not best)",quiet=1,mode=2,label=0,reset=1);cmd.enable("best_polar_conts")
    cmd.select("near", "protein_whole within 9.0 of best")
    cmd.extract("best_polar","near",zoom=0)
    cmd.delete("protein_whole")
    cmd.hide("everything","best_polar")
    cmd.show("sticks","best_polar")
    cmd.zoom("best_polar")

cmd.extend( "proxy_load", proxy_load );
