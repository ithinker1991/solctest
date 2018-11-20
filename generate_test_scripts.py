#!/usr/bin/python

import os
import commands
import json


SOLC_OUTPUT_FORMATE = "%s/solc_output_%s"


def complie_solc(bin_path, case_path, version):
    solc_output_path = SOLC_OUTPUT_FORMATE % (case_path, version)
    solc_file_path = case_path + "/test.sol"
    other_opt = "--bin --opcodes --abi --optimize --asm --ast"
    cmd = "{bin_path} {other_opt} -o {solc_output_path} {solc_path} --overwrite".format(bin_path=bin_path,
                                                                                        other_opt=other_opt,
                                                                                        solc_output_path=solc_output_path,
                                                                                        solc_path=solc_file_path
                                                                                        )
    print(cmd)
    sts, msg = commands.getstatusoutput(cmd)
    print(msg)
    generate_source_script(case_path, version)


def generate_source_script(case_path, version):
    solc_output = SOLC_OUTPUT_FORMATE % (case_path, version)
    files = os.listdir(solc_output)
    script_file = open("%s/%s.script" % (case_path, version), "w")
    contracts = set()
    for f in files:
        if f.endswith("bin"):
            contracts.add(f[:-4])

    for contract in contracts:
        script_file.write("contract:" + contract + "\n")
        generate_contract_scrpits(case_path, contract, version, script_file)
        script_file.write("\n\n")


def generate_contract_scrpits(case_path, contract, version, script_file):
    solc_output = SOLC_OUTPUT_FORMATE % (case_path, version)
    # script_file = open("%s/%s_%s.script" % (case_path, version, contract), "w")
    print script_file

    bin_file = "%s/%s.bin" % (solc_output, contract)
    abi_file = "%s/%s.abi" % (solc_output, contract)
    bin_str = open(bin_file, "r").read()
    abi_str = open(abi_file, "r").read()

    construct_sign, constructor_params, is_hex, fee_limit = "#", "#", "false", "1000000000"
    resource_percent, origin_energy_limit, value, token_value, token_id = "100", "10000000", "0", "0", "#"
    deploy_script = "deploycontract {contract_name} {abi} {bytecode} {constructor_sign} {constructor_params} " \
                    "{is_hex} {fee_limit} {resource_percent} {origin_energy_limit} {call_value} " \
                    "{token_value} {token_id}".format(contract_name="%s_%s" % (contract, version),
                                                      abi=abi_str,
                                                      bytecode=bin_str,
                                                      constructor_sign=construct_sign,
                                                      constructor_params=constructor_params,
                                                      is_hex="false",
                                                      fee_limit=fee_limit,
                                                      resource_percent=resource_percent,
                                                      origin_energy_limit=origin_energy_limit,
                                                      call_value=value,
                                                      token_value=token_value,
                                                      token_id=token_id)

    # print "deploy script:"
    script_file.write("deploy script:\n")
    print(deploy_script)
    script_file.write(deploy_script)
    script_file.write("\n")

    script_file.write("tirgger script:\n")
    entrys = json.loads(abi_str)
    for e in entrys:
        param_names = []
        if e['type'] == "function":
            for input in e['inputs']:
                param_names.append(input["type"])

            trigger_script = "triggercontract {address} {method} {parms} {is_hex} {fee_limit} {call_value} " \
                "{token_value} {token_id}\n".format(address="Txxxxxxxxxxx",
                                                    method="%s(%s)" % (e["name"], ",".join(param_names)),
                                                    parms="#" if len(param_names) == 0 else ",".join(param_names),
                                                    is_hex=is_hex,
                                                    fee_limit=fee_limit,
                                                    call_value=value,
                                                    token_value=token_value,
                                                    token_id=token_id)

            script_file.write(trigger_script)


def main():
    # bin_path, solc_path = sys.argv[1], sys.argv[2]
    bin_path1 = "./solc_bin/solc-lastest"
    bin_path2 = "./solc_bin/solc-release"


    casees_path = "./solctest/cases"
    for f in os.listdir(casees_path):
        if f.startswith("case"):
            solc_path = casees_path + "/" + f
            complie_solc(bin_path1, solc_path, "lastest")
            complie_solc(bin_path2, solc_path, "release")


main()
