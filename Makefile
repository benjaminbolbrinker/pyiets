C10H4Au6S2=./tests/C10H4Au6S2_ridft
H2O_dscf=./tests/H2O_dscf
H2O_dscf_tm_params=./tests/H2O_dscf_tm_parms
H2O_dscf_g09=./tests/H2O_dscf_gaussian
H2O_ridft=./tests/H2O_ridft
H2O_ridft_gaussianin=./tests/H2O_ridft_gaussianin
H2O_ridft_fake_gaussianin=./tests/H2O_ridft_fakegaussianin
H2O_ridft_turbomole_M=./tests/H2O_ridft_turbomolein_M
H2O_M=./tests/H2O_M
H2O_self=./tests/H2O_self

cwd:=$(abspath .)

documentation:
	cd docs/ && make html
	firefox ${cwd}/docs/build/html/index.html

test_all: test_H2O_dscf test_H2O_dscf_tm_params test_H2O_dscf_g09 test_H2O_ridft test_H2O_ridft_gaussianin test_H2O_ridft_fake_gaussianin test_H2O_ridft_turbomole_M test_H2O_M test_H2O_self

test_C10H4Au6S2:
	pyiets ${C10H4Au6S2}

test_H2O_dscf: 
	pyiets ${H2O_dscf}

test_H2O_dscf_tm_params: 
	pyiets ${H2O_dscf_tm_params}

test_H2O_dscf_g09: 
	pyiets ${H2O_dscf_g09}

test_H2O_ridft: 
	pyiets ${H2O_ridft}

test_H2O_ridft_gaussianin: 
	pyiets ${H2O_ridft_gaussianin}

test_H2O_ridft_fake_gaussianin: 
	pyiets ${H2O_ridft_fake_gaussianin}

test_H2O_ridft_turbomole_M: 
	pyiets ${H2O_ridft_turbomole_M}

test_H2O_M: 
	pyiets ${H2O_M}

test_H2O_self: 
	pyiets ${H2O_self}

clean: clean_C10H4Au6S2 clean_H2O_dscf clean_H2O_dscf_tm_params clean_H2O_dscf_g09 clean_H2O_ridft clean_docs clean_H2O_ridft_gaussianin clean_H2O_ridft_fake_gaussianin clean_H2O_ridft_turbomole_M clean_H2O_M clean_H2O_self

clean_C10H4Au6S2: 
	rm -rf ${C10H4Au6S2}/*distortions* ${C10H4Au6S2}/*.restart ${C10H4Au6S2}/output 

clean_H2O_dscf:
	rm -rf ${H2O_dscf}/*distortions* ${H2O_dscf}/*.restart ${H2O_dscf}/output 
	
clean_H2O_dscf_tm_params:
	rm -rf ${H2O_dscf_tm_params}/*distortions* ${H2O_dscf_tm_params}/*.restart ${H2O_dscf_tm_params}/output 

clean_H2O_dscf_g09:
	rm -rf ${H2O_dscf_g09}/*distortions* ${H2O_dscf_g09}/*.restart ${H2O_dscf_g09}/output 

clean_H2O_ridft:
	rm -rf ${H2O_ridft}/*distortions* ${H2O_ridft}/*.restart ${H2O_ridft}/output 

clean_H2O_ridft_gaussianin:
	rm -rf ${H2O_ridft_gaussianin}/*distortions* ${H2O_ridft_gaussianin}/*.restart ${H2O_ridft_gaussianin}/output 

clean_H2O_ridft_fake_gaussianin:
	rm -rf ${H2O_ridft_fake_gaussianin}/*distortions* ${H2O_ridft_fake_gaussianin}/*.restart ${H2O_ridft_fake_gaussianin}/output 

clean_H2O_ridft_turbomole_M:
	rm -rf ${H2O_ridft_turbomole_M}/*distortions* ${H2O_ridft_turbomole_M}/*.restart ${H2O_ridft_turbomole_M}/output 

clean_H2O_M:
	rm -rf ${H2O_M}/*distortions* ${H2O_M}/*.restart ${H2O_M}/output 

clean_H2O_self:
	rm -rf ${H2O_self}/*distortions* ${H2O_self}/*.restart ${H2O_self}/output 

clean_docs:
	cd docs && make clean
