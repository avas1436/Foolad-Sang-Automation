from packages.safe_round import NumberRounder

rounder = NumberRounder()
print(rounder.round(1.23))

print(rounder(3.1411615))
print(rounder.round_list([1.25153, 2.355158, 0, None], zero_return=False))
