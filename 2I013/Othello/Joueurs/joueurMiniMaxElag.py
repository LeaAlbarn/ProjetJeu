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
    coupAjouer = None
    scoremax = -10000000000
    for coup in listeCoups :
        score_estime = estimation (jeu, coup, 1, -10000000,10000000)
        if score_estime > scoremax : 
            coupAjouer = coup
            scoremax=score_estime
    return coupAjouer
    
    
def estimation (jeu, coup, profondeur, alpha, beta) : 
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
   
    if profondeur%2 ==0:  #noeud max
        scoremax=-10000000
        for c in listeCoups : 
            score_estime = estimation(copie, c, profondeur+1, max(alpha, scoremax), beta)
            if  score_estime >= beta :
                return 10000000  
            if score_estime>scoremax : 
                scoremax=score_estime
        return scoremax

    if profondeur%2==1:#noeud min
        scoremin=10000000
        for c in listeCoups : 
            score_estime = estimation(copie, c, profondeur+1, alpha, min(beta, scoremin))
            if  score_estime <= alpha :
                return -10000000
            if score_estime<scoremin:
                scoremin=score_estime
        return scoremin

            
def evaluation (jeu) : 
    """ jeu -> int 
    """
    return game.getScore(jeu,moi)-game.getScore(jeu, moi%2+1)
