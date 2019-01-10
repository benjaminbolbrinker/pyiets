test:
	make clean && ls -l /home/bolbrinker/Software/artaios/bin/ && ./pyiets.py tests/sampleinput

clean: 
	rm -rf ./tests/sampleinput/*dissortions* ./tests/sampleinput/*.restart
