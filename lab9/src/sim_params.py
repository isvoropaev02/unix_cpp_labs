"""Random generator parameters"""

SEED = 0

"""Number of requests of each type"""
U1 = 3  # good example with U1=U2=U3=1
U2 = 5
U3 = 10

"""Processing time of requests of each type"""
T1 = 0.5  # Registration
T2 = 0.3  # Get main page
T3 = 0.1  # Get active users

"""Processing CPU usage of requests of each type"""
C1 = 0.25  # Registration
C2 = 0.15  # Get main page
C3 = 0.01  # Get active users

"""Number of parallel workers (threaded/multiprocess simulation)"""
NUM_WORKERS = 4

"""CPU Manager settings"""
CPU_MANAGER_ENABLE = True
T_WAIT = 0.01
MAX_CAPACITY = 1.0
OUTPUT_SAVE_PATH = (
    "lab9/doc/cpu_report_"
    + str(U1)
    + "_"
    + str(U2)
    + "_"
    + str(U3)
    + "_nworkers"
    + str(NUM_WORKERS)
    + ".png"
)
