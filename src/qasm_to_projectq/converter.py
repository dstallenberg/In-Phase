import re

preps = [['prep_x', re.compile(r'prep_x q\[\d+]')],
         ['prep_y', re.compile(r'prep_y q\[\d+]')],
         ['prep_z', re.compile(r'prep_z q\[\d+]')]]

singles = [['X', re.compile(r'X q\[\d+:?\d*]'), 'X'],
           ['Y', re.compile(r'Y q\[\d+:?\d*]'), 'Y'],
           ['Z', re.compile(r'Z q\[\d+:?\d*]'), 'Z'],
           ['H', re.compile(r'H q\[\d+:?\d*]'), 'H'],
           ['I', re.compile(r'I q\[\d+:?\d*]'), 'I'],
           ['measure', re.compile(r'(measure)|(Measure_z) q\[\d+:\d*]'), 'Measure']]

single_args = [['Rx', re.compile(r'Rx q\[\d+], *-?\d+.?\d*'), 'Rx'],
               ['Ry', re.compile(r'Ry q\[\d+], *-?\d+.?\d*'), 'Ry'],
               ['Rz', re.compile(r'Rz q\[\d+], *-?\d+.?\d*'), 'Rz']]

doubles = [['CNOT', re.compile(r'CNOT q\[\d+], *q\[\d+]'), 'X'],
           ['CZ', re.compile(r'CZ q\[\d+], *q\[\d+]'), 'Z'],
           ['SWAP', re.compile(r'CZ q\[\d+], *q\[\d+]'), 'SWAP']]

doubles_args = [['CR', re.compile(r'CR q\[\d+], *q\[\d+], *-?\d+.?\d*'), 'Rz']]

triples = [['Toffoli', re.compile(r'Toffoli q\[\d+], *q\[\d+], *q\[\d+]'), 'X']]

subcode = re.compile(r'{.*}')
check_multi = re.compile(r'q\[\d+:\d+]')
get_qubit = re.compile(r'q\[\d+]')
get_num = re.compile(r'\d+')

alloc = re.compile(r'qubits \d')

measure_x = re.compile(r'Measure_x q\[\d]\n')
measure_y = re.compile(r'Measure_y q\[\d]\n')
measure_all = re.compile(r'Measure_all q\[\d]\n')

def qasm_to_projectq(qasm_code):
    result = ['from projectq import MainEngine', 'from projectq.backends import Simulator']

    projectq_code, total_bits, used_gates = convert_qasm_to_projectq(qasm_code)
    used_gates.append('Measure')
    used_gates.append('All')

    unique_gates = set(used_gates)
    gates_string = ', '.join(unique_gates)
    result.append(f'from projectq.ops import {gates_string}')
    result.append('def calc_probs():')
    result.append('\tsim = Simulator()')

    result.append('\teng = MainEngine(backend=sim)')
    result.append('\t' + projectq_code)

    bits_string = 'q' + ', q'.join(list(str(x) for x in range(total_bits)))
    result.append(f'\tAll(Measure) | [{bits_string}]')

    result.append('\teng.flush()')
    result.append('\tresult = dict()')

    result.append('\tfor i in range(2**len(qubits)):')
    result.append('\t\tbinary = \'{0:b}\'.format(i)')

    result.append('\t\tif len(qubits) != len(binary):')
    result.append('\t\t\tbinary = (\'0\' * (len(qubits) - len(binary))) + binary')

    result.append('\t\tresult[binary] = sim.get_probability(binary, qubits)')
    result.append('\treturn result')

    return '\n'.join(result)

def convert_qasm_to_projectq(qasm_code):
    result = []
    total_bits = 0
    used_gates = []

    for line in qasm_code.splitlines():
        if subcode.match(line):
            projecq_subcode, _, used_sub_gates = convert_qasm_to_projectq('\n'.join(line.replace('{', '').replace('}', '').split('|')))
            used_gates.extend(used_sub_gates)
            result.append(projecq_subcode)

        bits = get_num.findall(''.join(get_qubit.findall(line)))
        qrange = check_multi.findall(line)
        if qrange:
            min_max_bits = get_num.findall(qrange[0])
            bits = list(str(x) for x in range(int(min_max_bits[0]), int(min_max_bits[1])))

        bits_string = 'q' + ', q'.join(bits)

        found = False

        if alloc.match(line):
            total_bits = int(line.split(' ')[1])
            result.append(f'qubits = eng.allocate_qureg({total_bits})')
            for i in range(total_bits):
                result.append(f'q{i} = qubits[{i}]')
            continue

        # Singles
        for single in singles:
            if single[1].match(line):
                used_gates.append(single[2])
                if qrange:
                    used_gates.append('All')
                    result.append(f'All({single[2]}) | [{bits_string}]')
                else:
                    result.append(f'{single[2]} | q{bits[0]}')
                found = True
                break

        if found:
            continue

        # Singles with args
        for single in single_args:
            if single[1].match(line):
                used_gates.append(single[2])
                parts = line.split(',')
                result.append(f'{single[2]}({parts[1]}) | q{bits[0]}')
                found = True
                break

        if found:
            continue

        # Doubles
        for double in doubles:
            if double[1].match(line):
                used_gates.append('C')
                used_gates.append(double[2])
                result.append(f'C({double[2]}) | ({bits_string})')
                found = True
                break

        if found:
            continue

        # Doubles with args
        for double in doubles_args:
            if double[1].match(line):
                used_gates.append('C')
                used_gates.append(double[2])
                parts = line.split(',')
                result.append(f'C({double[2]}({parts[2]})) | ({bits_string})')
                found = True
                break

        if found:
            continue

        # Triples
        for triple in triples:
            if triple[1].match(line):
                used_gates.append('C')
                used_gates.append(triple[2])
                result.append(f'C({triple[2]}, 2) | ({bits_string})')
                found = True
                break

        if found:
            continue

    result = '\n\t'.join(result)
    return result, total_bits, used_gates


