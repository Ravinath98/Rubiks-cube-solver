import kociemba

def convert(s):
    str1 = ""
    return(str1.join(s))

def get_rubic_solution(cube):
    s1 = ""
    s2= ""
    s3= ""
    s4= ""
    s5= ""
    s6 = ""

    for i in range(0,9):
        s1 = s1 + cube[i]
        s2 = s2 + cube[i+9]
        s3 = s3 + cube[i+18]
        s4 = s4 + cube[i+27]
        s5 = s5 + cube[i+36]
        s6 = s6 + cube[i+45]
        print(i)

    c= [s5,s2,s1,s6,s4,s3] # cosiemba input correspondence
    #print(c)

    # #can be removed ------------------------------------------
    # for i in range(0,len(c)):
    #     x=list(c[i])
    #     for j in range(0,len(c[i])):
    #         if x[j]=='B':
    #             x[j]='G'
    #         elif x[j]=='W':
    #             x[j]='B'
    #
    #         elif x[j]=='G':
    #             x[j]='W'
    #
    #     c[i] = convert(x)
    # #can be removed ------------------------------------------
    #print(c)
    cube = convert(c)
    #print(cube)
    # cube = cube.replace('Y', 'U')
    # cube = cube.replace('R', 'R')
    # cube = cube.replace('B', 'F')
    # cube = cube.replace('W', 'D')
    # cube = cube.replace('O', 'L')
    # cube = cube.replace('G', 'B')
    cube = cube.replace('Y', 'D')
    cube = cube.replace('R', 'R')
    cube = cube.replace('B', 'B')
    cube = cube.replace('W', 'U')
    cube = cube.replace('O', 'L')
    cube = cube.replace('G', 'F')

    try:

        solution = kociemba.solve(str(cube))
        print(solution)
        return solution

    except:
        print('exceptttttttttttttttttttttttttttttt')
        return "Not a valid input"


#
# solution = get_rubic_solution(cube)
# print(solution)
