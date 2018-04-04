import game 


moi = None
PMAX = 2
params=[-1,5,1,1,1,1,1]

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
    def dot (param, evals):#produit scalaire poids*sous fonctions d'eval
        res=0
        for i in range(len(evals)):
            res+=params[i]*evals[i]    
        return res
    evals = [diffScores(jeu), priseDesCoins(jeu), priseDesBords(jeu), priseDuCentre(jeu), priseDesBordsMilieu(jeu), peuDePions (jeu), regroupement(jeu)]
    return dot (params, evals)
    
def diffScores(jeu) :
    return game.getScore(jeu,moi)-game.getScore(jeu, moi%2+1)
    

def priseDesCoins(jeu) : #fin de partie : prise de pions definitifs dans les coins
    res = 0
    if (len(jeu[3])>=50) :
        if (jeu[0][0][0]==moi) :
            res +=1
        if (jeu[0][0][7]==moi) :
            res+=1
        if (jeu[0][7][0]==moi):
            res+=1
        if (jeu[0][7][7]==moi) :
            res+=1
    return res
            
def priseDesBords(jeu) : #fin de partie : avoir des pions definitifs dans les bords
    res=0
    i = 0
    if (len(jeu[3])>=50) : 
        for i in range (7) :
            if (jeu[0][0][i]==moi):
                res+=1
            if (jeu[0][i][0]==moi):
                res+=1
            if (jeu[0][7][i]==moi) :
                res+=1
            if (jeu[0][i][7]==moi) :
                res+=1
    return res
            

def priseDuCentre (jeu) :#avoir les 4 pions du centre 
    res = 0
    if (jeu[0][3][3]==moi) : 
        res+=1
    if (jeu[0][4][3]==moi) : 
        res+=1
    if (jeu[0][3][4]==moi) : 
        res+=1
    if (jeu[0][4][4]==moi) : 
        res+=1
    return res

def priseDesBordsMilieu (jeu) : #milieu de partie : prise des bords externes dangereuse
    res = 0
    if (len(jeu[3])<50) : 
        for i in range (7) :
            if (jeu[0][0][i]==moi):
                res-=1
            if (jeu[0][i][0]==moi):
                res-=1
            if (jeu[0][7][i]==moi) :
                res-=1
            if (jeu[0][i][7]==moi) :
                res-=1
    return res

def peuDePions (jeu) : #debut et milieu de partie : peu de pions assure une meilleure mobilite
    res = 0
    if (len(jeu[3])<45) : 
        for i in range (7) :
            for j in range (7) :
                if (jeu[0][i][j]==moi):
                    res-=1
    return res

def regroupement (jeu) : #debut et milieu de partie : ne pas avoir de pion "seul"
    res = 0
    if (len(jeu[3]) <40) :
        for i in range(7) :
            for j in range (7) : 
                if ((jeu[0][i][j]==moi) and (jeu[0][i+1][j]==moi)) :
                    res+=1
                if ((jeu[0][i][j]==moi) and (jeu[0][i-1][j]==moi)) :
                    res+=1
                if ((jeu[0][i][j]==moi) and (jeu[0][i][j+1]==moi)) :
                    res+=1
                if ((jeu[0][i][j]==moi) and (jeu[0][i][j-1]==moi)) :
                    res+=1
    return res

def mobilite (jeu) : #nombre de coups valides possibles VS nombre de coups de l'adversaire
    if moi == jeu[1]:
        return (jeu[2])
    else :
        return -jeu[2]
                
       




