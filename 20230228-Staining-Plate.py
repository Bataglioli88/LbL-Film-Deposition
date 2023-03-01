#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
University of Campinas-20220904
LbL staining plate protocols
"""

from opentrons import protocol_api

metadata = {'apiLevel': '2.8'}

def run(protocol: protocol_api.ProtocolContext):

    # Containers
    Film_plate1 = protocol.load_labware('corning_96_wellplate_360ul_flat', '1')     #Plate1 for film deposition - shallow 96 well plate
    Film_plate2 = protocol.load_labware('corning_96_wellplate_360ul_flat', '4')     #Plate2 for film deposition - shallow 96 well plate
    Film_plate3 = protocol.load_labware('corning_96_wellplate_360ul_flat', '7')     #Plate3 for film deposition - shallow 96 well plate
    
    Dye_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '2')  #Dye Plate - 12-channel trouugh

    Water1_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '5') #Rinse Water - 8 channel trough
    Water2_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '8') #Rinse Water - 8 channel trough
    Water3_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '11') #Rinse Water - 8 channel trough
     
    trash_dye_plate = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '9') #Trash
                
    # Polymers and rinse water position in the plate
    Dye1 = Dye_plate.wells_by_name()['A1']
    Dye2 = Dye_plate.wells_by_name()['A2']
    Dye3 = Dye_plate.wells_by_name()['A5']    
    
    Water1 = Water1_plate.wells_by_name()['A1'] #Water    
    Water2 = Water2_plate.wells_by_name()['A1'] #Water     
    Water3 = Water3_plate.wells_by_name()['A1'] #Water
    
    trash_dye = trash_dye_plate.wells_by_name()['A1']

    # Film plate columns
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

    # Tip rack
    Tip_rack1 =  protocol.load_labware('opentrons_96_tiprack_300ul', '3')

    # Multi channel pipette
    p300m = protocol.load_instrument('p300_multi', mount='left', tip_racks=[Tip_rack1])
    
    # Process variables
    vol_dye = 100  # uL
    vol_wash = 250  # uL
    ads_time = 15*60  # s
    wash_time = 60  # s
    
    def staining(vol_dye, vol_wash, ads_time, wash_time, Dye1, Dye2, Dye3, Water1, Water2, Water3, first_column, last_column):
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
        # Dye transfer to the film plates
        p300m.pick_up_tip()
        for i in range(first_column, last_column+1):
            p300m.transfer(vol_dye, Dye1.bottom(6), Col[i].bottom(6), new_tip='never', blow_out=True, touch_tip=False)        
            p300m.transfer(vol_dye, Dye2.bottom(6), Col[i+12].bottom(6), new_tip='never', blow_out=True, touch_tip=False) 
            p300m.transfer(vol_dye, Dye3.bottom(6), Col[i+24].bottom(6), new_tip='never', blow_out=True, touch_tip=False) 
        p300m.drop_tip()
        p300m.pick_up_tip()
        p300m.move_to(Col[first_column].top())
        protocol.delay(seconds=ads_time)

        # Dye removal from the film plates       
        for i in range(first_column,last_column+1):
            p300m.aspirate(vol_dye * 3, Col[i].bottom(1))
            p300m.blow_out(trash_dye)
            p300m.aspirate(vol_dye * 3, Col[i+12].bottom(1))
            p300m.blow_out(trash_dye)
            p300m.aspirate(vol_dye * 3, Col[i+24].bottom(1))
            p300m.blow_out(trash_dye)           
        p300m.drop_tip()  
          
        # Rinse step
        for step in range(3):
            #Rinse water transfer to the film plate
            p300m.pick_up_tip() 
            for i in range(first_column, last_column+1):
                p300m.transfer(vol_wash, Water1.bottom(6), Col[i].bottom(5), new_tip='never', blow_out=True, touch_tip=False)
                p300m.transfer(vol_wash, Water2.bottom(6), Col[i+12].bottom(5), new_tip='never', blow_out=True, touch_tip=False)
                p300m.transfer(vol_wash, Water3.bottom(6), Col[i+24].bottom(5), new_tip='never', blow_out=True, touch_tip=False)                
            p300m.move_to(Col[first_column].top())      
            protocol.delay(seconds=wash_time)

            #Rinse water removal from the film plate    
            for i in range(first_column, last_column+1):
                p300m.aspirate(vol_wash , Col[i].bottom(1))
                p300m.blow_out(trash_dye)                
                p300m.aspirate(vol_wash , Col[i+12].bottom(1))
                p300m.blow_out(trash_dye)                
                p300m.aspirate(vol_wash , Col[i+24].bottom(1)) 
                p300m.blow_out(trash_dye) 
            p300m.drop_tip()
    staining(vol_dye, vol_wash, ads_time, wash_time, Dye1, Dye2, Dye3, Water1, Water2, Water3, 0,11)
    