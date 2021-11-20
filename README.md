# explainability-of-possibilistic-rule-based-systems


This repo contains some of my PhD thesis work. 
It contains programs related to the methods presented in the following articles:

- Baaj, I., Poli, J., Ouerdane, W. & Maudet, N. (2021). Inférence min-max pour un système à base de règles possibilistes @ LFA 2021 Rencontres Francophones sur la Logique Floue et ses Applications, October 2021, Paris, France. 
- Baaj, I., Poli, J., Ouerdane, W. & Maudet, N. (2021). Representation of Explanations of Possibilistic Inference Decisions @ ECSQARU 2021 European Conference on Symbolic and Quantitative Approaches to Reasoning with Uncertainty, September 2021, Prague, Czechia. DOI: http://dx.doi.org/10.1007/978-3-030-86772-0_37
- Baaj, I., Poli, J., Ouerdane, W. & Maudet, N. (2021). Min-max inference for possibilistic rule-based system @ FUZZ-IEEE 2021 International Conference on Fuzzy Systems, July 2021, Luxemburg, Luxemburg.  DOI: https://doi.org/10.1109/FUZZ45933.2021.9494506

The program in the "equation-system" folder allows us to construct the equation system associated to a cascade. (a set of $n$ possibilistic rules chained with a set of $m$ possibilistic rules) (Chapter 3 of my PhD Thesis). 

The program in the "example-1" folder allows us to form explanations of the inference results of the possibilistic rule-based system used as an example in both the ECSQARU 2021 paper and in Chapter 5 of my PhD thesis. 

The program in the "example-2" folder allows us to form the explanations of the inference results of the second possibilistic rule-based system used as an example  in Chapter 5 of my PhD thesis.

The programs were tested with Python 3.9.8 and Mac OSX 11.5.2. They need the package named click to work: ```pip3 install click'''.

![CC0](https://licensebuttons.net/l/by/3.0/88x31.png)
