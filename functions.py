from variables import *

#Lookup tables for Taylor polynomials
sineLookup       = [1.0,
                    -0.16666666666666666,
                    0.008333333333333333,
                    -0.0001984126984126984,
                    2.7557319223985893e-06,
                    -2.505210838544172e-08,
                    1.6059043836821613e-10,
                    -7.647163731819816e-13,
                    2.8114572543455206e-15,
                    -8.22063524662433e-18,
                    1.9572941063391263e-20,
                    -3.868170170630684e-23,
                    6.446950284384474e-26,
                    -9.183689863795546e-29,
                    1.1309962886447716e-31,
                    -1.216125041553518e-34,
                    1.151633562077195e-37,
                    -9.67759295863189e-41,
                    7.265460179153071e-44]

cosineLookup     = [1.0,
                    -0.5,
                    0.041666666666666664,
                    -0.001388888888888889,
                    2.48015873015873e-05,
                    -2.755731922398589e-07,
                    2.08767569878681e-09,
                    -1.1470745597729725e-11,
                    4.779477332387385e-14,
                    -1.5619206968586225e-16,
                    4.110317623312165e-19,
                    -8.896791392450574e-22,
                    1.6117375710961184e-24,
                    -2.4795962632247976e-27,
                    3.279889237069838e-30,
                    -3.7699876288159054e-33,
                    3.8003907548547434e-36,
                    -3.387157535521162e-39,
                    2.6882202662866363e-42]

expLookup        = [1.0,
                    1.0,
                    0.5,
                    0.16666666666666666,
                    0.041666666666666664,
                    0.008333333333333333,
                    0.001388888888888889,
                    0.0001984126984126984,
                    2.48015873015873e-05,
                    2.7557319223985893e-06,
                    2.755731922398589e-07,
                    2.505210838544172e-08,
                    2.08767569878681e-09,
                    1.6059043836821613e-10,
                    1.1470745597729725e-11,
                    7.647163731819816e-13,
                    4.779477332387385e-14,
                    2.8114572543455206e-15]

arcsineLookup   = [1.0,
                   0.16666666666666666,
                   0.075,
                   0.044642857142857144,
                   0.030381944444444444,
                   0.022372159090909092,
                   0.017352764423076924,
                   0.01396484375,
                   0.011551800896139705,
                   0.009761609529194078,
                   0.008390335809616815,
                   0.0073125258735988454,
                   0.006447210311889649,
                   0.005740037670841924,
                   0.005153309682319905,
                   0.004660143486915096,
                   0.004240907093679363,
                   0.003880964558837669]

natLogLookup    = [1.0,
                   -0.5,
                   0.3333333333333333,
                   -0.25,
                   0.2,
                   -0.16666666666666666,
                   0.14285714285714285,
                   -0.125,
                   0.1111111111111111,
                   -0.1,
                   0.09090909090909091,
                   -0.08333333333333333,
                   0.07692307692307693,
                   -0.07142857142857142,
                   0.06666666666666667,
                   -0.0625,
                   0.058823529411764705,
                   -0.05555555555555555,
                   0.05263157894736842]

arctanLookup    = [1.0,-0.3333333333333333,0.2,-0.14285714285714285,0.1111111111111111,-0.09090909090909091,0.07692307692307693,-0.06666666666666667,0.058823529411764705,-0.05263157894736842,0.047619047619047616]

    
#Defining functions

def sgn(x):
    if x < 0:
        return -1
    if x == 0:
        return 0
    return 1

#####################################################################

#@functools.cache
def fact(x):
    if x != int(x) or x < 0:
        raise ValueError(''''Undefined for negative integers or
                         decimal values''')
    if x == 1 or x == 0:
        return 1 #Definiton of the factorial
    else:
        return x * fact(x-1) #n! = n(n-1)!

#####################################################################

def floor(x):
    return int(x) #Alias for int, used where floor is more intuitive

#####################################################################

def ceil(x):
    if x == int(x):
        return x
    else:
        return int(x) + 1

#####################################################################
    
#@functools.cache
def sin(x):
    if x < 0:
        return sin(x % (2*pi))
    if x > 2*pi:
        return sin(x % (2*pi)) #Range reduction so that the Taylor
    #polynomial only has to be accurate in [0, 2pi]
    s = 0
    for n in range(19):
        s += x**(2*n+1) * sineLookup[n] #Calculates the value of
        #the Taylor polynomial of sine at x
    return s

#####################################################################

#@functools.cache
def cos(x):
    if x < 0:
        return cos(x % (2*pi))
    if x > 2*pi:
        return cos(x % (2*pi)) 
    s = 0
    for n in range(19):
        s += x**(2*n) * cosineLookup[n]
    return s

#####################################################################

#@functools.cache
def ln(x):
    if x <= 0:
        raise ValueError('Undefined') #ln is undefined for
    #x <= 0
    elif x == 2:
        return 0.69314718056  #Predefined for range reduction
    else:
        s = 0
        while x > 1.55: #Arbitrary cut-off point for where
            #I decided the approximation was too inaccurate
            s += ln(2) #Range reduction using ln(ab) = ln(a) + ln(b)
            x /= 2
        x -= 1 #Needed because the Taylor polynomial
        #approximates ln(1+x) instead of ln(x)
        for n in range(19):
            s += (x)**(n+1) * natLogLookup[n]
        return s

#####################################################################
    
def log(num, base):
    return ln(num) / ln(base)

#####################################################################

def exp(x):
    s = 0
    for n in range(18):
        s += x**n * expLookup[n]
    return s

#####################################################################

#@functools.cache
def arcsin(x):
    if x > 1 or x < -1:
        raise ValueError('Undefined for x > 1 or x < 1')
    s = 0
    for n in range(16):
        s += x**(2*n+1) * arcsineLookup[n]
    return s

#####################################################################

def arccos(x):
    return pi / 2 - arcsin(x) #An identity for arccos

#####################################################################

#@functools.cache
def arctan(x):
    if x >= 0:
        if x < 0.832362: #Upper bound for the Taylor polynomia.l being
            #accurate 
            s = 0
            for n in range(11):
                s += x**(2*n+1) * arctanLookup[n]
            return s
        
        elif x > 1.18549: #Lower bound for the Taylor polynomial of
            #arctan being accurate for
            #arctan(x) = pi/2 - arctan(1/x)
            s = pi / 2
            for n in range(11):
                s -= arctanLookup[n] / x**(2*n+1)
            return s

        else:
            return -0.25*(x**2) + x + 0.0354 #Intermediate function
    else:
        return -arctan(-1 * x) #-arctan(-x) = arctan(x), used to
        #simplify the function

#####################################################################

def tan(x):
    t = cos(x)
    if t != 0:
        return sin(x) / t
    else:
        raise ValueError('tan(x) undefined for x = pi/2 + k*pi')

#####################################################################

def sec(x):
    t = cos(x)
    if t != 0:
        return 1 / t
    else:
        raise ValueError('sec(x) undefined for x = pi/2 + k*pi')

#####################################################################

def csc(x):
    t = sin(x)
    if t != 0:
        return 1/t
    else:
        raise ValueError('csc(x) undefined for x = k*pi')

#####################################################################

def cot(x):
    t = sin(x)
    if x != 0:
        return cos(x) / t
    else:
        raise ValueError('cot(x) undefined for x = k*pi')

#####################################################################

def arcsec(x):
    return pi/2 - arcsin(1/x)

#####################################################################

def arccsc(x):
    return arcsin(1/x)

#####################################################################

def arccot(x):
    if x == 0:
        return pi/2
    if x > 0:
        return arctan(1/x)
    return pi + arctan(1/x)  #Identities for arccot(x)

#####################################################################

def sinh(x):
    t = exp(x)-exp(-x)
    return 0.5 * t

#####################################################################

def cosh(x):
    t = exp(x) + exp(-x)
    return 0.5*t

#####################################################################


def tanh(x):
    n = sinh(x)
    d = cosh(x)
    return n / d

#####################################################################

def coth(x):
    n = exp(2*x) + 1
    d = exp(2*x) - 1
    return n / d

#####################################################################

def sech(x):
    n = 2*exp(x)
    d = exp(2*x) + 1
    return n / d

#####################################################################

def csch(x):
    if x != 0:
        n = 2 * exp(x)
        d = exp(2*x) - 1
        return n / d
    raise ValueError('csch(x) undefined for x = 0')

#####################################################################

def arsinh(x):
    return ln(x + (x**2 + 1)**(0.5))

#####################################################################

def arcosh(x):
    if x >= 1:
        return ln(x + (x**2 - 1)**(0.5))
    raise ValueError('arcosh(x) undefined for x < 1')

#####################################################################

def artanh(x):
    if abs(x) < 1:
        return 0.5 * ln((1+x) / (1-x))
    raise ValueError('artanh(x) undefined for |x| >= 1')

#####################################################################

def arcoth(x):
    if abs(x) > 1:
        return 0.5 * ln((x+1)/(x-1))
    raise ValueError('arcoth(x) undefined for |x| <= 1')

#####################################################################

def arsech(x):
    if 0 < x <= 1:
        return ln((1 + (1 - x**2)**0.5)/x)
    raise ValueError('arsech(x) undefined for x <= 0 or x > 1')

#####################################################################

def arcsch(x):
    if x != 0:
        return ln(x**-1 + (x**(-2) + 1)**0.5)
    raise ValueError('arcsch(x) undefined for x = 0')

#####################################################################


def initialiseAlias():
    alias = {'sgn': ['sign'],
             'fact': ['factorial'],
             'sin': ['sine'],
             'cos': ['cosine'],
             'arcsin': ['arcsine', 'asin', 'asine'],
             'arccos': ['arccosine', 'acos', 'acosine'],
             'arctan': ['arctangent', 'atan', 'atangent'],
             'tan': ['tangent'],    
             'sec': ['secant'],
             'csc': ['cosecant', 'cosec'],
             'cot': ['cotangent', 'cot'],
             'arcsec': ['arcsecant'],
             'arccsc': ['arccosec'],
             'arccot': ['arccotangent'],

             'sinh': ['hsin', 'hsine', 'sinehyperbolic', 'sinhyperbolic', 'sinehyper', 'sinhyper', 'sineh',
                      'hyperbolicsine', 'hyperbolicsin', 'hypersine', 'hypersin'],

             'cosh': ['cosineh', 'cosinehyperbolic', 'coshyperbolic', 'cosinehyper', 'coshyper', 'hcos', 'hcosine',
                      'hypercosine', 'hypercos', 'hyperboliccosine', 'hyperboliccos'],

             'tanh': ['tangenth', 'tangenthyperbolic', 'tangenthyper', 'tanhyperbolic', 'tanhyper', 'htan', 'htangent',
                      'hyperbolictan', 'hyperbolictangent', 'hypertan', 'hypertangent'],

             'coth': ['cotangenthyperbolic', 'cotangenthyper', 'cotangenth', 'cotanhyperbolic', 'cotanhyper', 'cotanh',
                      'cothyperbolic', 'cothyper', 'hcotangent', 'hcotan', 'hcot', 'hyperboliccotangent',
                      'hyperboliccotan', 'hyperboliccot', 'hypercotan', 'hypercot'],

             'sech': ['secanthyperbolic', 'secanthyper', 'secanth', 'sechyperbolic', 'sechyper', 'hsecant', 'hsec',
                      'hypersecant', 'hypersec', 'hyperbolicsecant', 'hyperbolicsec'],

             'csch': ['cosecanthyperbolic', 'cosecanthyper', 'cosecanth', 'cosechyperbolic', 'cosechyper', 'cschyper',
                      'hcosecant', 'hcsc', 'hypercosecant', 'hypercosec', 'hyperboliccosecant', 'hyperboliccosec',
                      'cschyperbolic', 'cschyper', 'hypercsc', 'hyperboliccsc'],

             'arsinh': ['arhsin', 'arhsine', 'arsinehyperbolic', 'arsinhyperbolic', 'arsinehyper', 'arsinhyper', 'arsineh',
                      'arhyperbolicsine', 'arhyperbolicsin', 'arhypersine', 'arhypersin'],

             'arcosh': ['arcosineh', 'arcosinehyperbolic', 'arcoshyperbolic', 'arcosinehyper', 'arcoshyper', 'arhcos',
                        'arhcosine', 'arhypercosine', 'arhypercos', 'arhyperboliccosine', 'arhyperboliccos'],

             'artanh': ['artangenth', 'artangenthyperbolic', 'artangenthyper', 'artanhyperbolic', 'artanhyper', 'arhtan',
                        'arhtangent', 'arhyperbolictan', 'arhyperbolictangent', 'arhypertan', 'arhypertangent'],

             'arcsch': ['arcosecanthyperbolic', 'arcosecanthyper', 'arcosecanth', 'arcosechyperbolic', 'arcosechyper',
                        'arcschyper', 'arhcosecant', 'arhcsc', 'arhypercosecant', 'arhypercosec', 'arhyperboliccosecant',
                        'arhyperboliccosec', 'arcschyperbolic', 'arcschyper', 'arhypercsc', 'arhyperboliccsc'],
             
             'arcoth': ['arcotangenthyperbolic', 'arcotangenthyper', 'arcotangenth', 'arcotanhyperbolic', 'arcotanhyper',
                        'arcotanh', 'arcothyperbolic', 'arcothyper', 'arhcotangent', 'arhcotan', 'arhcot',
                        'arhyperboliccotangent', 'arhyperboliccotan', 'arhyperboliccot', 'arhypercotan', 'arhypercot'],
             
             'arsech': ['arsecanthyperbolic', 'arsecanthyper', 'arsecanth', 'arsechyperbolic', 'arsechyper', 'arhsecant',
                        'arhsec', 'arhypersecant', 'arhypersec', 'arhyperbolicsecant', 'arhyperbolicsec']}
                      

    for i in alias.keys():
        for j in alias[i]:
            exec(f'{j}={i}')
