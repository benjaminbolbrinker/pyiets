fold=./tests/sampleinput_michael

test:
	make clean && ./pyiets.py ${fold}

clean: 
	rm -rf ${fold}/*dissortions* ${fold}/*.restart ${fold}/output
