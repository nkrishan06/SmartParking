
# NOTE: All modules are singleton.

### System init
FREE = 1
OCCUP = 0


# Dictionary where each key : value  ->  sensorID : parkingSlotState
parking_lot_states = dict()


# Load parking lots
parking_lot_states['science'] = dict()
# Load sensor list
# TODO: Ideally this should be done by taking the list from something like a DB where
# the administrators of the parking will keep a list of the sensors and their locations
for i in range(2):
    parking_lot_states['science'][i] = FREE
###