import json

# podsumowuje parametry sieci neronowej
def nn_params(source):
    if type(source) == str:
        with open(source, "r") as data:
            neural_network = json.load(data)
    else:
        neural_network = source

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
    return json.dumps(nn_params)

# podsumowuje parametry programu logicznego
def lp_params(source):
    if type(source) == str:
        with open(source, "r") as data:
            logic_program = json.load(data)
    else:
        logic_program = source

    lp_params = {"clauses": {"amount": 0, "onlyPos": 0, "onlyNeg": 0, "mix": 0, "headWithH": 0, "atoms": {"sum": 0, "pos": 0, "neg": 0, "withH": 0, "posWithH": 0, "negWithH": 0}, "difAtoms": {"sum": 0, "pos": 0, "neg": 0, "withH": 0, "posWithH": 0, "negWithH": 0}}, "facts": 0, "assumptions": 0}
    atoms = []
    atoms_pos = []
    atoms_neg = []
    for i in range(len(logic_program["lp"]["clauses"])):
        if logic_program["lp"]["clauses"][i]["tag"] == "Cl": # klauzule
            lp_params["clauses"]["amount"] += 1
            if len(logic_program["lp"]["clauses"][i]["clPAtoms"]) == 0: # klauzule onlyNegAtoms
                lp_params["clauses"]["onlyNeg"] +=1
            elif len(logic_program["lp"]["clauses"][i]["clNAtoms"]) == 0: # klauzule onlyPosAtoms
                lp_params["clauses"]["onlyPos"] +=1
            else: #klauzule mixAtoms
                lp_params["clauses"]["mix"] +=1
            lp_params["clauses"]["atoms"]["sum"] += len(logic_program["lp"]["clauses"][i]["clPAtoms"]) + len(logic_program["lp"]["clauses"][i]["clNAtoms"]) # suma klauzul
            if logic_program["lp"]["clauses"][i]["clHead"]["label"] == "h": # klauzule z hHead
                lp_params["clauses"]["headWithH"] += 1
            for j in logic_program["lp"]["clauses"][i]["clPAtoms"]: # atomy pozytywne
                lp_params["clauses"]["atoms"]["pos"] +=1
                if j["label"] == "h": # atomy pozytywne z h
                        lp_params["clauses"]["atoms"]["withH"] += 1
                        lp_params["clauses"]["atoms"]["posWithH"] += 1
                if j not in atoms_pos:
                    atoms_pos.append(j)
                    lp_params["clauses"]["difAtoms"]["pos"] += 1 # atomy pozytywne bez powtórzeń
                if not j in atoms:
                    atoms.append(j)
                    if j["label"] == "h": #atomy pozytywne bez powtórzeń z h
                        lp_params["clauses"]["difAtoms"]["withH"] += 1
                        lp_params["clauses"]["difAtoms"]["posWithH"] += 1
            for j in logic_program["lp"]["clauses"][i]["clNAtoms"]: # atomy negatywne
                lp_params["clauses"]["atoms"]["neg"] +=1
                if j["label"] == "h": # atomy negatywne z h
                        lp_params["clauses"]["atoms"]["withH"] += 1
                        lp_params["clauses"]["atoms"]["negWithH"] += 1
                if j not in atoms_neg:
                    atoms_neg.append(j)
                    lp_params["clauses"]["difAtoms"]["neg"] += 1 # atomy negatywne bez powtórzeń
                if not j in atoms:
                    atoms.append(j)
                    if j["label"] == "h": # atomy negatywne bez powtórzeń z h
                        lp_params["clauses"]["difAtoms"]["withH"] += 1
                        lp_params["clauses"]["difAtoms"]["negWithH"] += 1
            lp_params["clauses"]["difAtoms"]["sum"] = len(atoms) # atomy bez powtórzeń

    lp_params["facts"] += len(logic_program["lp"]["facts"]) # fakty
    lp_params["assumptions"] += len(logic_program["lp"]["assumptions"]) # assumptions
    return json.dumps(lp_params)
