C10H4Au6S2=./tests/sampleinput_michael
H2O_dscf=./tests/sampleinput_dscf
H2O_ridft=./tests/sampleinput_ridft

cwd:=$(abspath .)

documentation_html:
	cd docs/ && make html
	firefox ${cwd}/docs/build/html/index.html

install:
	./install.sh

test_all: test_H2O_dscf test_H2O_ridft test_C10H4Au6S2

test_C10H4Au6S2:
	pyiets ${C10H4Au6S2}

test_H2O_dscf: 
	pyiets ${H2O_dscf}

test_H2O_ridft: 
	pyiets ${H2O_ridft}

clean: clean_C10H4Au6S2 clean_H2O_dscf clean_H2O_ridft clean_docs

clean_C10H4Au6S2: 
	rm -rf ${C10H4Au6S2}/*distortions* ${C10H4Au6S2}/*.restart ${C10H4Au6S2}/output 

clean_H2O_dscf:
	rm -rf ${H2O_dscf}/*distortions* ${H2O_dscf}/*.restart ${H2O_dscf}/output 

clean_H2O_ridft:
	rm -rf ${H2O_ridft}/*distortions* ${H2O_ridft}/*.restart ${H2O_ridft}/output 

clean_docs:
	cd docs && make clean
