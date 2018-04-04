#ne sait pas jouer en joueur 2
import game

moi = None
PMAX = 3

def saisieCoup(jeu) :
    global moi
    moi=game.getJoueur(jeu)
    coup=decision(jeu,game.getCoupsValides(jeu))
    
    return coup
    
def decision (jeu, listeCoups) : 
    """ jeu*[coup]-> pair[coup, score]
    choisit le coup a jouer dans une liste de coup possibles
    """
    #print(str(listeCoups))    
    coupAjouer = None
    scoremax = -10000000000
    s=""
    for coup in listeCoups :
        score_estime = estimation (jeu, coup, 1)
        s+=","+str(score_estime)
        if score_estime > scoremax : 
            coupAjouer = coup
            scoremax=score_estime
    #print(s)
    #print(coupAjouer)
    return coupAjouer
    
    
def estimation (jeu, coup, profondeur) : 
    copie = game.getCopieJeu(jeu)
    game.joueCoup (copie, coup)    
    if game.finJeu(copie) : 
        gagnant = game.getGagnant(copie)
        if gagnant == moi :
            return 10000
        elif gagnant == 0 : 
            return -100
        else :
            return -10000
            
    if profondeur == PMAX :
        return evaluation (copie)
        
    listeCoups = game.getCoupsValides (copie)        
    if profondeur%2 ==0:
        scoremax=-10000
        for c in listeCoups : 
            score_estime = estimation(copie, c, profondeur+1)

            if  score_estime > scoremax :
                scoremax=score_estime
        return scoremax

    if profondeur%2==1:
        scoremin=10000
        for c in listeCoups : 
            score_estime = estimation(copie, c, profondeur+1)
            if  score_estime < scoremin :
                scoremin=score_estime
        return scoremin
        
def evaluation (jeu) : 
    """ jeu -> int 
    """
    return game.getScore(jeu,moi)-game.getScore(jeu, moi%2+1)
