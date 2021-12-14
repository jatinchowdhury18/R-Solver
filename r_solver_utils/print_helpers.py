import subprocess, sys, re

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

    # C syntax can't do exponents using the '^' operator.
    # This is a stupid hack that assumes all resistors have
    # a 2-character label, e.g. 'Ra'
    count = 0
    for f in re.finditer(re.escape('^2'), M_strs):
        s_ind = f.start() + count
        chars_to_square = M_strs[s_ind-2:s_ind]
        M_strs = M_strs[:s_ind] + f'*{chars_to_square}' + M_strs[s_ind+2:]
        count += 1

    if out_file is not None:
        out_file.write(M_strs)
    else:
        print(M_strs)

def print_shape(M):
    '''Prints the shape of a Sage matrix'''
    print((M.nrows(), M.ncols()))

def verbose_print(mat, name):
    print('')
    print(name)
    print(mat)
    print_shape(mat)
