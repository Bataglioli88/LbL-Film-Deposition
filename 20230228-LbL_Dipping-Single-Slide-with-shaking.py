#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
University of Campinas-20220904
LbL-dipping method
"""

from opentrons import protocol_api
import time
metadata = {'apiLevel': '2.8'}
def run(protocol: protocol_api.ProtocolContext):

    #Cointainer
    Poly_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '2') #12-channel trough
     
    #polymers and rinsing water
    #Priming layer - PEI
    PEI1 = Poly_plate.wells_by_name()['C1'] #Position #1
    PEI2 = Poly_plate.wells_by_name()['F1'] #Position #2       
    #Note: Positions #1 and #2 provide movement inside the polymer channel trough

    #Priming layer - Rinding water    
    Water1A_PEI = Poly_plate.wells_by_name()['C2'] #Position #1
    Water1B_PEI = Poly_plate.wells_by_name()['F2'] #Position #2
    Water2A_PEI = Poly_plate.wells_by_name()['C3'] #Position #1
    Water2B_PEI = Poly_plate.wells_by_name()['F3'] #Position #2
    Water3A_PEI = Poly_plate.wells_by_name()['C4'] #Position #1
    Water3B_PEI = Poly_plate.wells_by_name()['F4'] #Position #2

    #Polyanion
    Poly1A = Poly_plate.wells_by_name()['C5'] #Position #1
    Poly1B = Poly_plate.wells_by_name()['F5'] #Position #2        
    
    Water1A_Poly1 = Poly_plate.wells_by_name()['C6'] #Position #1
    Water1B_Poly1 = Poly_plate.wells_by_name()['F6'] #Position #2
    Water2A_Poly1 = Poly_plate.wells_by_name()['C7'] #Position #1
    Water2B_Poly1 = Poly_plate.wells_by_name()['F7'] #Position #2
    Water3A_Poly1 = Poly_plate.wells_by_name()['C8'] #Position #1
    Water3B_Poly1 = Poly_plate.wells_by_name()['F8'] #Position #2

    #Polycation
    Poly2A = Poly_plate.wells_by_name()['C9'] #Position #1
    Poly2B = Poly_plate.wells_by_name()['F9'] #Position #2       
    
    Water1A_Poly2 = Poly_plate.wells_by_name()['C10'] #Position #1
    Water1B_Poly2 = Poly_plate.wells_by_name()['F10'] #Position #2
    Water2A_Poly2 = Poly_plate.wells_by_name()['C11'] #Position #1
    Water2B_Poly2 = Poly_plate.wells_by_name()['F11'] #Position #2
    Water3A_Poly2 = Poly_plate.wells_by_name()['C12'] #Position #1
    Water3B_Poly2 = Poly_plate.wells_by_name()['F12'] #Position #2
    
    #pipette - works as a robot arm to attach the coated substrates
    Tip_rack1 =  protocol.load_labware('opentrons_96_tiprack_300ul', '3')  #tip rack
    p300s = protocol.load_instrument('p300_single', mount='right', tip_racks=[Tip_rack1]) # single channel pipette
    
    #Process variables
    ads_time = 600  # s 
    wash_time = 120 # s
    n_bilayers = 12  # number of monolayers
    #monolayer function    
    def monolayer(PolymerA, PolymerB, Water1A, Water1B, Water2A, Water2B, Water3A, Water3B):
        # Monolayer
        p300s.move_to(PolymerA.top(25))    # center of the trough
        t0 = time.time() # initial instant (when films are immersed)
        t = time.time() # current instant
        while t-t0 <= ads_time:
            p300s.move_to(PolymerA.top(25),force_direct=True, speed=30) # returns to initial position
            p300s.move_to(PolymerB.top(25),force_direct=True, speed=30) # moves to rows in the same trough with the substrate immersed
            t = time.time() # updates actual instant    
        p300s.move_to(PolymerA.top(100)) 
    
        # Washing step1
        p300s.move_to(Water1A.top(25))
        t0 = time.time() # initial instant (when films are immersed)
        t = time.time() # actual instant
        while t-t0 <= wash_time:
            p300s.move_to(Water1A.top(25),force_direct=True, speed=30) # returns to initial position
            p300s.move_to(Water1B.top(25),force_direct=True, speed=30) # moves to rows in the same trough with the substrate immersed
            t = time.time() # updates actual instant    
        p300s.move_to(Water1A.top(100))

        # Washing step2
        p300s.move_to(Water2A.top(25))
        t0 = time.time() # initial instant (when films are immersed)
        t = time.time() # actual instant
        while t-t0 <= wash_time/2:
            p300s.move_to(Water2A.top(25),force_direct=True, speed=30) # returns to initial position
            p300s.move_to(Water2B.top(25),force_direct=True, speed=30) # moves to rows in the same trough with the substrate immersed
            t = time.time() # updates actual instant
        p300s.move_to(Water2A.top(100))
    
        # Washing step3
        p300s.move_to(Water3A.top(25))
        t0 = time.time() # initial instant (when films are immersed)
        t = time.time() # actual instant
        while t-t0 <= wash_time/2:
            p300s.move_to(Water3A.top(25),force_direct=True, speed=30) # returns to initial position
            p300s.move_to(Water3B.top(25),force_direct=True, speed=30) # moves to rows in the same trough with the substrate immersed
            t = time.time() # updates actual instant
        p300s.move_to(Water3A.top(100))
    #time to attach the glass slide
    p300s.pick_up_tip(Tip_rack1['A1'].top(100)) # center of the trough
    p300s.blow_out(PEI1.top(100)) # center of the trough
    t0 = time.time() # initial instant
    t =  time.time() # actual instant
    while t-t0 <= 5:
        t = time.time() # updates actual instant

    #Film assembly
    if not protocol.is_simulating():
        #PEI Deposition
        monolayer(PEI1, PEI2, Water1A_PEI, Water1B_PEI, Water2A_PEI, Water2B_PEI, Water3A_PEI, Water3B_PEI)
        # Building up bilayers
        for bilayer in range(n_bilayers):
            monolayer(Poly1A, Poly1B, Water1A_Poly1, Water1B_Poly1, Water2A_Poly1, Water2B_Poly1, Water3A_Poly1, Water3B_Poly1)
            monolayer(Poly2A, Poly2B, Water1A_Poly2, Water1B_Poly2, Water2A_Poly2, Water2B_Poly2, Water3A_Poly2, Water3B_Poly2)