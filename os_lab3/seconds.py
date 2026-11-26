#!/usr/bin/enu python3
import argparse
import time
def main():
	parser=argparse.ArgumentParser(
		description="Report seconds elapsed since startup."
	)
	parser.add_argument(
		"--watch",
		action="store_true",
		help="keep reporting elapsed seconds"
	)
	args=parser.parse_args()
	initial=time.monotonic()
	if args.watch:
		try:
			while True:
				print(int(time.monotonic() - initial))
				time.sleep(1)
		except KeyboardInterrupt:
			return 0
	print(int(time.monotonic() - initial))
	return 0
if __name__ == "__main__":
	raise SystemExit(main())
