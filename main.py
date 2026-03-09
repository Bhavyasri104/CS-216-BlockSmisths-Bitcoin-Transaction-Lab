import os

print("Bitcoin Transaction Lab")
print("----------------------------")

print("\nRunning Legacy Transaction: A -> B")
os.system("python part1_legacy_AB.py")

print("\nRunning Legacy Transaction: B -> C")
os.system("python part1_legacy_BC.py")

print("\nRunning SegWit Transaction: A' -> B'")
os.system("python part2_segwit_AB.py")

print("\nRunning SegWit Transaction: B' -> C'")
os.system("python part2_segwit_BC.py")

print("\nAll transactions executed successfully.")
