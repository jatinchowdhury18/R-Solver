import subprocess, sys

def print_matrix(M, out_file, num_ports):
    '''Prints a Sage matrix as a C-style 2D array'''
    args = subprocess.list2cmdline(sys.argv[:])
    comments = '// This scattering matrix was derived using the R-Solver python script (https://github.com/jatinchowdhury18/R-Solver),\n'
    comments += '// invoked with command: ' + args + '\n'
    prefix = f'const auto S_matrix[{num_ports}][{num_ports}] = {{'
    empty_prefix = ' ' * len(prefix)
    
    M_strs = M.str(rep_mapping=lambda a: str(a) + ',')
    M_strs = M_strs.replace('[', empty_prefix + '{').replace(',]', '},')
    M_strs = comments + prefix + M_strs[len(prefix):-1] + '};'

    if out_file is not None:
        out_file.write(M_strs)
    else:
        print(M_strs)

def print_shape(M):
    '''Prints the shape of a Sage matrix'''
    print((M.nrows(), M.ncols()))
