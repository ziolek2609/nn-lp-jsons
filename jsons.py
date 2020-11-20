


# podsumowuje parametry sieci neronowej
def nn_params(neural_network):
    nn_params = {"atoms":{"sum": 0, "inp": 0, "hid": 0, "out": 0, "rec": 0}, "connections":{"inp2Hid": 0, "hid2Out": 0, "rec": 0}, "bigWeights": {"inp2Hid": 0, "hid2Out": 0, "rec": 0}, "factors":{}}
    nn_params["atoms"]["sum"] = len((neural_network)["nn"]["inpLayer"])+len((neural_network)["nn"]["hidLayer"])+len((neural_network)["nn"]["outLayer"])
    nn_params["atoms"]["inp"] = len((neural_network)["nn"]["inpLayer"]) # atomy na inputLayer
    nn_params["atoms"]["hid"] = len((neural_network)["nn"]["hidLayer"]) # atomy na hiddenLayer
    nn_params["atoms"]["out"] = len((neural_network)["nn"]["outLayer"]) # atomy na outputLayer
    nn_params["connections"]["inp2Hid"] = len(neural_network["nn"]["inpToHidConnections"]) # połączenia inp2Hid
    nn_params["connections"]["hid2Out"] = len(neural_network["nn"]["hidToOutConnections"]) # połączenia hid2Out
    for i in neural_network["nn"]["inpToHidConnections"]:
        if abs(i["weight"]) >= neural_network["nnFactors"]["amin"]:
            nn_params["bigWeights"]["inp2Hid"] += 1 # duże wagi połączeń inp2Hid
    for i in neural_network["nn"]["hidToOutConnections"]:
        if abs(i["weight"]) >= neural_network["nnFactors"]["amin"]:
            nn_params["bigWeights"]["hid2Out"] += 1 # duże wagi połączeń hid2Out
    if "recLayer" in (neural_network)["nn"]:
        nn_params["atoms"]["sum"] += len((neural_network)["nn"]["recLayer"])
        nn_params["atoms"]["rec"] = len((neural_network)["nn"]["recLayer"]) # atomy w recLayer
        nn_params["connections"]["rec"] = len(neural_network["nn"]["recConnections"]) # połączenie rec
        for i in neural_network["nn"]["recConnections"]:
            if abs(i["weight"]) >= neural_network["nnFactors"]["amin"]:
                nn_params["bigWeights"]["rec"] += 1 # duże wagi połączeń rec
    nn_params["factors"] = neural_network["nnFactors"]
    return nn_params


# podsumowuje parametry programu logicznego
def lp_params(logic_program):
    nnParams = {"clauses": {"amount": 0, "onlyPos": 0, "onlyNeg": 0, "mix": 0, "headWithH": 0, "atoms": {"sum": 0, "pos": 0, "neg": 0, "withH": 0, "posWithH": 0, "negWithH": 0}, "difAtoms": {"sum": 0, "pos": 0, "neg": 0, "withH": 0, "posWithH": 0, "negWithH": 0}}, "facts": 0, "assumptions": 0}
    atoms = []
    atoms_pos = []
    atoms_neg = []
    for i in range(len(logic_program)):
        if logic_program[i]["tag"] == "Cl": # klauzule
            nnParams["clauses"]["amount"] += 1
            if len(logic_program[i]["clPAtoms"]) == 0: # klauzule onlyNegAtoms
                nnParams["clauses"]["onlyNeg"] +=1
            elif len(logic_program[i]["clNAtoms"]) == 0: # klauzule onlyPosAtoms
                nnParams["clauses"]["onlyPos"] +=1
            else: #klauzule mixAtoms
                nnParams["clauses"]["mix"] +=1
            nnParams["clauses"]["atoms"]["sum"] += len(logic_program[i]["clPAtoms"]) + len(logic_program[i]["clNAtoms"]) # suma klauzul
            if logic_program[i]["clHead"]["label"] == "h": # klauzule z hHead
                nnParams["clauses"]["headWithH"] += 1
            for j in logic_program[i]["clPAtoms"]: # atomy pozytywne
                nnParams["clauses"]["atoms"]["pos"] +=1
                if j["label"] == "h": # atomy pozytywne z h
                        nnParams["clauses"]["atoms"]["withH"] += 1
                        nnParams["clauses"]["atoms"]["posWithH"] += 1
                if j not in atoms_pos:
                    atoms_pos.append(j)
                    nnParams["clauses"]["difAtoms"]["pos"] += 1 # atomy pozytywne bez powtórzeń
                if not j in atoms:
                    atoms.append(j)
                    if j["label"] == "h": #atomy pozytywne bez powtórzeń z h
                        nnParams["clauses"]["difAtoms"]["withH"] += 1
                        nnParams["clauses"]["difAtoms"]["posWithH"] += 1
            for j in logic_program[i]["clNAtoms"]: # atomy negatywne
                nnParams["clauses"]["atoms"]["neg"] +=1
                if j["label"] == "h": # atomy negatywne z h
                        nnParams["clauses"]["atoms"]["withH"] += 1
                        nnParams["clauses"]["atoms"]["negWithH"] += 1
                if j not in atoms_neg:
                    atoms_neg.append(j)
                    nnParams["clauses"]["difAtoms"]["neg"] += 1 # atomy negatywne bez powtórzeń
                if not j in atoms:
                    atoms.append(j)
                    if j["label"] == "h": # atomy negatywne bez powtórzeń z h
                        nnParams["clauses"]["difAtoms"]["withH"] += 1
                        nnParams["clauses"]["difAtoms"]["negWithH"] += 1
            nnParams["clauses"]["difAtoms"]["sum"] = len(atoms) # atomy bez powtórzeń
        elif logic_program[i]["tag"] == "Fact": # fakty
            nnParams["facts"] += 1
        elif logic_program[i]["tag"] == "Assumption": # assumpitons
            nnParams["assumptions"] += 1
    return nnParams
