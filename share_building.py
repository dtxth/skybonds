"""
To start script use:
python3 share_building.py  --amount 4 --values 4 1.5 3 6 1.5


O(n)
~20 min

"""

import sys
import argparse


calculate_data = lambda amount, values: [ round(x / sum(values), 3) for x in values]

def main(argv):
	if not argv:
		print("Use that params for script:")
		print("--amount shares amount")
		print("--values values of share")
		sys.exit(2)

	CLI = argparse.ArgumentParser()      

	CLI.add_argument(
	  "--amount",  # shares amount
	  type=int
	)

	CLI.add_argument(
	    "--values",  # values of share
	    nargs="*",  # 0 or more values expected => creates a list
	    type=float
	) 	

	args = CLI.parse_args(argv)

	if len(args.values) is None or not args.amount :
		print("U should add ptoperly amount of values")

	print("shares amount: ", args.amount)
	print("values: ", args.values)

	print("resul: ", calculate_data(args.amount, args.values))


if __name__ == "__main__":
   main(sys.argv[1:])


