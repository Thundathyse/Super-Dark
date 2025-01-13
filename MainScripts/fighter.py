# # unitdict = {
# #     1:["Infantry", 3, 10, 10, 1],
# #     2:["Mech", 10, 10, 20, 2],
# #     3:["Tank", 7, 10, 30, 3]
# # }
# #dice rolls of soldiers and enemies
# infantry_attack = random.randint(1, 3)
# mech_attack = random.randint(1,10)
# tank_attack = random.randint(1,7)
# enemy_attack = random.randint(1,5)
# # ally_attack = 0
#
# def runThrow(throws, antithrows):
#     #quotes are placeholders
#     #replace ally troop and enemy troop with corresponding names
#     #we also need variables for the selected troops
#     throws = ["ally troop"]
#     antithrows = ["enemy troop"]
#     if "ally troop" == "Infantry":
#         throws = throws.replace("ally troop", infantry_attack)
#     elif "ally troop" == "Mech":
#         throws = throws.replace("ally troop", mech_attack)
#     elif "ally troop" == "tank":
#         throws = throws.replace("ally troop", tank_attack)
#
#     if "enemy troop" == "enemy":
#         throws = throws.replace("ally troop", enemy_attack)
#     while throws and antithrows:
#         # Access the first element of each list
#         throw = throws[0]
#         antithrow = antithrows[0]
#         if throw[0] < antithrow[0]:
#             # Subtract throw value from antithrow
#             antithrow[0] -= throw.pop(0)
#             if not throw:  # Remove empty lists
#                 throws.pop(0)
#         elif throw[0] > antithrow[0]:
#             # Subtract antithrow value from throw
#             throw[0] -= antithrow.pop(0)
#             if not antithrow:  # Remove empty lists
#                 antithrows.pop(0)
#         else:
#             # Values are equal; remove both
#             throw.pop(0)
#             antithrow.pop(0)
#             if not throw:
#                 throws.pop(0)
#             if not antithrow:
#                 antithrows.pop(0)
