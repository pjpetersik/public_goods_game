#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:42:12 2019

@author: paul
"""

import numpy as np

class player(object):
    def __init__(self,strategy=None):
        """
        The person object holds all variables that belong to one person. 
        Namely the current strategy and the last payoff.
        
        :type strategy: int
        :param strategy: The strategies are encoded by integers. 
        Where 0 represents a cooperator, 1 a defector and 2 a loner
        
        """
        
        if strategy==None:
            self.__strategy = np.random.randint(0,3)
        
        self.__payoff = 0.
        
    @property
    def strategy(self):
        return self.__strategy
    
    @property
    def payoff(self):
        return self.__payoff
    
    @payoff.setter
    def payoff(self,value):
        self.__payoff = value
    
class meanFieldModel(object):
    def __init__(self,nplayers):
        """
        The mean field object holds the variables that define a public goods game in
        a mean field and the methods to play the public goods game
        """
        self.nplayers = nplayers
        self.initGame()
        
    @property
    def players(self):
        return self.__players
        
    def initGame(self):
        self.__players = [player() for i in range(self.nplayers)]
    
    def playGame(self,nparticipants,c,r,sigma):
        """
        play one time the public goods game
        
        :param nparticipants: the number of players that participate in one game
        :param cost: the cost of playing the public goods game for the cooperator
        :param r: the facor with which the pot of costs is multiplied
        :param sigma: the payoff for the loner
        
        """
        assert (1<r and r<nparticipants)
        assert (0<sigma and sigma<r-1 )
        
        self.c = c
        self.r = r
        self.sigma = sigma
        
        random_player_indeces =  np.random.choice(self.nplayers, nparticipants, replace=False)
        
        nc = 0
        
        for i in random_player_indeces:
            if self.players[i].strategy == 0:
                nc +=1
        
        for i in random_player_indeces:
            self.assignPayoff(self.players[i], nc, nparticipants)
        
        
    def assignPayoff(self,player_instance, ncooperators, nparticpants):
        
        assert isinstance(player_instance,player)
        
        if player_instance.strategy == 0:
            player_instance.payoff += - self. c + self.r * self.c * ncooperators/nparticpants
        
        if player_instance.strategy == 1:
            player_instance.payoff += self.r * self.c * ncooperators/nparticpants
        
        if player_instance.strategy == 2:
            player_instance.payoff += self.sigma
            
if __name__ == "__main__":
    
    mfm = meanFieldModel(10)
    for i in range(1000):
        mfm.playGame(5,1.,4.,1.)
    
    
    