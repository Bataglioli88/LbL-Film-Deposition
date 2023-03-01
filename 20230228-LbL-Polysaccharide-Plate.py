"""
University of Campinas - 20220903
LbL coating plate protocol
"""

from opentrons import protocol_api
metadata = {'apiLevel': '2.8'}

def run(protocol: protocol_api.ProtocolContext):

    # Containers  
    Film_plate1 = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')
    Film_plate2 = protocol.load_labware('corning_96_wellplate_360ul_flat', '4')
    Film_plate3 = protocol.load_labware('corning_96_wellplate_360ul_flat', '7')
    
    #Polymer solution plates
    Poly_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '2')
    
    #Rinse water for polyanions (WaterA) and Polycations (WaterC) 
    WaterA1_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '5') 
    WaterC1_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '6') 
    WaterA2_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '8')    
    WaterC2_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '9')     
    WaterA3_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '10')     
    WaterC3_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '11')    

    # Tip rack
    Tip_rack1 =  protocol.load_labware('opentrons_96_tiprack_300ul', '3')

    # Multi channel pipette
    p300m = protocol.load_instrument('p300_multi', mount='left', tip_racks=[Tip_rack1]) 

    #Polyanions position in the Polymer Plate
    PolyA1 = Poly_plate.wells_by_name()['A1']
    PolyA2 = Poly_plate.wells_by_name()['A2']
    PolyA3 = Poly_plate.wells_by_name()['A3']
    PolyA4 = Poly_plate.wells_by_name()['A4']
    PolyA5 = Poly_plate.wells_by_name()['A5']    
    PolyA6 = Poly_plate.wells_by_name()['A6']

    #Polycations position in the Polymer Plate    
    PolyC1 = Poly_plate.wells_by_name()['A7']
    PolyC2 = Poly_plate.wells_by_name()['A8']
    PolyC3 = Poly_plate.wells_by_name()['A9']
    PolyC4 = Poly_plate.wells_by_name()['A10']
    PolyC5 = Poly_plate.wells_by_name()['A11']   
    PolyC6 = Poly_plate.wells_by_name()['A11']
    
    #PEI position in the Polymer Plate      
    PEI = Poly_plate.wells_by_name()['A6']     

    #Rinse water positions    
    WaterA1 = WaterA1_plate.wells_by_name()['A1']     
    WaterC1 = WaterC1_plate.wells_by_name()['A1']    
    WaterA2 = WaterA2_plate.wells_by_name()['A1']    
    WaterC2 = WaterC2_plate.wells_by_name()['A1']
    WaterA3 = WaterA3_plate.wells_by_name()['A1']   
    WaterC3 = WaterC3_plate.wells_by_name()['A1']     

    #Trash position
    trash = protocol.fixed_trash['A1']
  
    #Filmm plate columns  
    Col=[]
    Col= [
          Film_plate1.wells_by_name()['A1'], 
          Film_plate1.wells_by_name()['A2'],
          Film_plate1.wells_by_name()['A3'], 
          Film_plate1.wells_by_name()['A4'],          
          Film_plate1.wells_by_name()['A5'],
          Film_plate1.wells_by_name()['A6'], 
          Film_plate1.wells_by_name()['A7'], 
          Film_plate1.wells_by_name()['A8'], 
          Film_plate1.wells_by_name()['A9'],
          Film_plate1.wells_by_name()['A10'], 
          Film_plate1.wells_by_name()['A11'],          
          Film_plate1.wells_by_name()['A12'],
          Film_plate2.wells_by_name()['A1'], 
          Film_plate2.wells_by_name()['A2'],
          Film_plate2.wells_by_name()['A3'], 
          Film_plate2.wells_by_name()['A4'],          
          Film_plate2.wells_by_name()['A5'],
          Film_plate2.wells_by_name()['A6'],
          Film_plate2.wells_by_name()['A7'], 
          Film_plate2.wells_by_name()['A8'], 
          Film_plate2.wells_by_name()['A9'],
          Film_plate2.wells_by_name()['A10'], 
          Film_plate2.wells_by_name()['A11'],          
          Film_plate2.wells_by_name()['A12'],
          Film_plate3.wells_by_name()['A1'], 
          Film_plate3.wells_by_name()['A2'],
          Film_plate3.wells_by_name()['A3'], 
          Film_plate3.wells_by_name()['A4'],          
          Film_plate3.wells_by_name()['A5'],
          Film_plate3.wells_by_name()['A6'],
          Film_plate3.wells_by_name()['A7'], 
          Film_plate3.wells_by_name()['A8'],
          Film_plate3.wells_by_name()['A9'], 
          Film_plate3.wells_by_name()['A10'],          
          Film_plate3.wells_by_name()['A11'],
          Film_plate3.wells_by_name()['A12']               
          ]         

    #Tip positions
    Col_tip=[]
    Col_tip=[
          Tip_rack1.wells_by_name()['A1'],
          Tip_rack1.wells_by_name()['A2'],          
          Tip_rack1.wells_by_name()['A3'],
          Tip_rack1.wells_by_name()['A4'],
          Tip_rack1.wells_by_name()['A5'],
          Tip_rack1.wells_by_name()['A6'],          
          Tip_rack1.wells_by_name()['A7'],
          Tip_rack1.wells_by_name()['A8'],          
          Tip_rack1.wells_by_name()['A9'],
          Tip_rack1.wells_by_name()['A10'],          
          Tip_rack1.wells_by_name()['A11'],
          Tip_rack1.wells_by_name()['A12']          
             ]  
    
    # Process variables
    vol_pol = 50  # uL
    vol_wash = 150  # uL
    ads_time = 600  # s
    wash_time = 60  # s
    
    #Monolayer deposition function
    def monolayer(Polymer, Water, vol_pol, vol_wash, ads_time, wash_time, first_column, last_column, tip_pos):
        """
        Builds up one monolayer on every column between first_column and last_column. Both are also included.
        Does 2 washing steps.
        :param Polymer: polymer column
        :param Water: water column
        :param vol_pol: polymer volume
        :param vol_wash: water volume
        :param ads_time: adsorption time
        :param wash_time: washing time
        :param first_column: first coating column
        :param last_column: last coating column
        :return:
        """        
        #Polymer transfer to the film plate
        p300m.pick_up_tip(Col_tip[tip_pos])
        for i in range(first_column, last_column+1):
            p300m.transfer(vol_pol, Polymer.bottom(6), Col[i].bottom(6), new_tip='never', blow_out=True, touch_tip=False)        
            p300m.transfer(vol_pol, Polymer.bottom(6), Col[i+12].bottom(6), new_tip='never', blow_out=True, touch_tip=False)
            p300m.transfer(vol_pol, Polymer.bottom(6), Col[i+24].bottom(6), new_tip='never', blow_out=True, touch_tip=False)                    
        p300m.move_to(Col[first_column].top())
        protocol.delay(seconds=ads_time)
    
        #Polymer removal from the film plate
        for i in range(first_column, last_column+1):
            p300m.aspirate(vol_pol * 3, Col[i].bottom(1))
            p300m.blow_out(trash)

            p300m.aspirate(vol_pol * 3, Col[i+12].bottom(1))
            p300m.blow_out(trash)            

            p300m.aspirate(vol_pol * 3, Col[i+24].bottom(1))
            p300m.blow_out(trash)
    
        # Rinse step
        for step in range(3):
            # Rinse water transfer to the film plate
            for i in range(first_column, last_column+1):
                p300m.transfer(vol_wash, Water.bottom(6), Col[i].bottom(5), new_tip='never', blow_out=True, touch_tip=False)
                p300m.transfer(vol_wash, Water.bottom(6), Col[i+12].bottom(5), new_tip='never', blow_out=True, touch_tip=False)
                p300m.transfer(vol_wash, Water.bottom(6), Col[i+24].bottom(5), new_tip='never', blow_out=True, touch_tip=False)                
            p300m.move_to(Col[first_column].top())      
            protocol.delay(seconds=wash_time)

            # Rinse water removal from the film plate    
            for i in range(first_column, last_column+1):
                p300m.aspirate(vol_wash * 1.5, Col[i].bottom(1))
                p300m.blow_out(trash)
                
                p300m.aspirate(vol_wash * 1.5, Col[i+12].bottom(1))
                p300m.blow_out(trash)                

                p300m.aspirate(vol_wash * 1.5, Col[i+24].bottom(1)) 
                p300m.blow_out(trash)     
        p300m.return_tip()

    #Bilayer deposition function   
    def bilayer(first_column, last_column, PolymerA,  PolymerC, WaterA, WaterC, tip_pos):

        #Builds up one bilayer on every first_column and last_column. Both are also included.
        monolayer(PolymerA, WaterA, vol_pol, vol_wash, ads_time, wash_time, first_column, last_column, tip_pos)
        monolayer(PolymerC, WaterC, vol_pol, vol_wash, ads_time, wash_time, first_column, last_column, tip_pos+1)

    #Priming layer deposition function
    monolayer(PEI, WaterC1, vol_pol, vol_wash, ads_time, wash_time, 0, 5, 11)
    #Note: PEI solution plate is replaced by the Polymer solutions plate right after priming layer deposition
    
    #1st bilayer deposition
    n = 1
    start = 1
    tip_pos=0
    while start <= 1:
        for bilayers in range(1):
            bilayer(0, 11, PolyA1, PolyC1, WaterA1, WaterC1, tip_pos)
            n+=1
            start+=1                
    #2nd bilayer deposition       
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(1, 11, PolyA2, PolyC2, WaterA2, WaterC2, tip_pos)
            n+=1
            start+=1    
    tip_pos+=2

    #3rd bilayer deposition 
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(2, 11, PolyA3, PolyC3, WaterA3, WaterC3, tip_pos)
            n+=1
            start+=1                
    #4th bilayer deposition       
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(3, 11, PolyA4, PolyC4, WaterA3, WaterC3, tip_pos)
            n+=1
            start+=1    
    tip_pos+=2

    #5th bilayer deposition
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(4, 11, PolyA5, PolyC5, WaterA2, WaterC2, tip_pos)
            n+=1
            start+=1                
    #6th bilayer deposition        
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(5, 11, PolyA6, PolyC6, WaterA1, WaterC1, tip_pos)
            n+=1
            start+=1    
    tip_pos+=2

    #7th bilayer deposition
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(6, 11, PolyA1, PolyC1, WaterA3, WaterC3, tip_pos)
            n+=1
            start+=1                
    #8th bilayer deposition        
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(7, 11, PolyA2, PolyC2, WaterA2, WaterC2, tip_pos)
            n+=1
            start+=1    
    tip_pos+=2

    #9th bilayer deposition
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(8, 11, PolyA3, PolyC3, WaterA1, WaterC1, tip_pos)
            n+=1
            start+=1                
    #10th bilayer deposition       
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(9, 11, PolyA4, PolyC4, WaterA1, WaterC1, tip_pos)
            n+=1
            start+=1    
    tip_pos+=2

    #11th bilayer deposition
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(10, 11, PolyA5, PolyC5, WaterA2, WaterC2, tip_pos)
            n+=1
            start+=1                
    #12th bilayer deposition        
    start = 1
    while start <= 1:
        for bilayers in range(1):
            bilayer(11, 11, PolyA6, PolyC6, WaterA3, WaterC3, tip_pos)
            n+=1
            start+=1                     