#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:42:12 2019

@author: paul
"""

import numpy as np
import matplotlib.pyplot as plt

class player(object):
    def __init__(self,strategy=None):
        """
        The player class holds all variables that belong to one person. 
        Namely the current strategy and the last payoff.
        
        :type strategy: int
        :param strategy: The strategies are encoded by integers. 
        Where 0 represents a cooperator, 1 a defector and 2 a loner
        
        """
        
        if strategy==None:
            self.__strategy = np.random.randint(0,3)
        else:
            self.__strategy = strategy
        
        self.__payoff = 0.
        
    @property
    def strategy(self):
        return self.__strategy
    
    @strategy.setter
    def strategy(self,value):
        assert value in [0,1,2]
        self.__strategy = value
    
    @property
    def payoff(self):
        return self.__payoff
    
    @payoff.setter
    def payoff(self,value):
        self.__payoff = value
    
class bucketModel(object):
    def __init__(self,nplayers,inital_distribution=None):
        """
        The bucket model class holds the variables that define a public goods game in
        a mean field and the methods to play the public goods game
        
        :param nplayers: number of total players
        :param inital_distribution: The initial distribution of players [cooperators,defectors,loners]
        """
        self.nplayers = nplayers
        self.__initGame(inital_distribution)
        
    @property
    def players(self):
        return self.__players
        
    def __initGame(self,inital_distribution):
        """
        initialize strategies with a equal propability for each strategy when inital_distribution is None. 
        Or using the initial distribution.
        """
        if inital_distribution == None:
            self.__players = [player() for i in range(self.nplayers)]
        else:
            assert sum(inital_distribution) == 1.
            
            pc = inital_distribution[0]
            pd = inital_distribution[1]
            pl = inital_distribution[2]
            
            strategies = np.random.choice([0,1,2],size=self.nplayers,replace=True,p=[pc,pd,pl])
            
            self.__players = [player(strategies[i]) for i in range(self.nplayers)]
        
    def playGame(self,nparticipants,c,r,sigma):
        """
        play one time the public goods game
        
        :param nparticipants: The number of players that are chosen randomely from all players and 
        given the opportunity to particpate in the public 
        goods game (note:loners do not play the public goods game!).
        
        :param cost: The cost of playing the public goods game for the cooperator
        
        :param r: The facor with which the pot of costs is multiplied
        
        :param sigma: The payoff for the loner
        
        """
        # check if r and sigma are chosen correctly 
        assert (1 < r and r < nparticipants)
        assert (0 < sigma and sigma < r-1 )
        
        # set game properties
        self.c = c
        self.r = r
        self.sigma = sigma
        
        # choose randomely players
        random_player_indeces =  np.random.choice(self.nplayers, nparticipants, replace=False)
        
        # count the cooperators and defectors
        nc = 0
        nd = 0
        for i in random_player_indeces:
            if self.players[i].strategy == 0:
                nc +=1
            elif self.players[i].strategy == 1:
                nd +=1
        
        # assign payoffs
        for i in random_player_indeces:
            self.__assignPayoff(self.players[i], nc, nd)
        
        
    def __assignPayoff(self,player_instance, ncooperators, ndefectors):
        """
        assign a payoff o one player of a public goods game 
        
        :param player_instance: a instance of the player class
        :ncooperators: number of cooperators in the public goods game
        :nparticipants: number of participants in the public goods game
        """
        
        assert isinstance(player_instance,player)
        
        # assign payoff depending on the strategy played by the player
        if player_instance.strategy == 0:
            player_instance.payoff += - self. c + self.r * self.c * ncooperators/(ncooperators + ndefectors)
        
        elif player_instance.strategy == 1:
            player_instance.payoff += self.r * self.c * ncooperators/(ncooperators + ndefectors)
        
        elif player_instance.strategy == 2:
            player_instance.payoff += self.sigma
            
    
    def reviseStragey(self,player_index,tau=0.1,K=0.1):
        """
        revision protocol for player1 to change his strategy to the strategy of player2
        
        :param player1,player2: instance of class player
        """
        # choose a randomely players
        random_player_index =  np.random.choice(self.nplayers)
        
        payoff1 = self.players[player_index].payoff
        payoff2 = self.players[random_player_index].payoff

        self.tau = tau
        self.K = K
        
        p = self.__revisionProtocol(payoff1,payoff2)
        
        change = np.random.choice([False,True],p=[1-p,p])
        
        if change:
            self.players[player_index].strategy = self.players[random_player_index].strategy
    
    def __revisionProtocol(self,payoff1,payoff2):
        
        change_likelihood = 1/(1+np.exp(payoff1 - payoff2 + self.tau)/self.K)
        
        return change_likelihood
    
    def clearPayoffs(self):
        for i in range(self.nplayers):
            self.players[i].payoff = 0
            
    def countStrategies(self):
        nc = 0
        nd = 0
        
        for i in range(self.nplayers):
            if self.players[i].strategy == 0:
                nc+=1
            elif self.players[i].strategy == 1:
                nd+=1
        nl = self.nplayers - nc - nd
        
        return nc,nd,nl
        
if __name__ == "__main__":
    
    # total number of players
    nplayers = 300
    
    # rounds each player (approximately) plays
    rounds = 100
    
    # Public goods game settings 
    # number of players that is offered to play PGG
    nparticipants = 5 
    
    # cost of participating
    c = 1.
    
    # multipliaction factor for the pot
    r = 3.
    
    # loners payoff
    sigma = 1.
    
    strategies = np.zeros(shape=(rounds,3))
    
    bm = bucketModel(nplayers,inital_distribution=[0.4,0.1,0.5])
    
    for j in range(rounds):
        
        for i in range(int(nplayers/nparticipants)):
            bm.playGame(nparticipants,c,r,sigma)
        
        for i in range(nplayers):
            bm.reviseStragey(i)
        
        bm.clearPayoffs()
    
        strategies[j,:] = bm.countStrategies()
    
    plt.close("all")
    plt.plot(np.arange(rounds),strategies)

    
    