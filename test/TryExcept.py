def TryExcept():
    try:
        print(1)
    except:
       print(2)
    print(3)

def TryExceptMulti():
    try:
        print(1)
    except a:
       print(2)
    except b:
       print(3)
    except c:
       print(4)
    print(5)

def TryExceptMultiFallback():
    try:
        print(1)
    except a:
       print(2)
    except b:
       print(3)
    except:
       print(4)
    print(5)

def TryExceptMultiNamed():
    try:
        print(1)
    except A as a:
       print(2)
    except B as b:
       print(3)
    except C as c:
       print(4)
    print(5)

def TryExceptMultiNamedFallback():
    try:
        print(1)
    except A as a:
       print(2)
    except B as b:
       print(3)
    except:
       print(4)
    print(5)

def TryExceptMultiNamedAndUnnamed():
    try:
        print(1)
    except A as a:
       print(2)
    except b:
       print(3)
    except:
       print(4)
    print(5)

def TryExceptElseBare():
    try:
        print(1)
    except:
        print(2)
    else:
        print(3)
    print(4)

def TryExceptElseMulti():
    try:
        print(1)
    except a:
        print(2)
    except b:
        print(3)
    else:
        print(4)
    print(5)

def TryExceptElseMultiFallback():
    try:
        print(1)
    except a:
        print(2)
    except b:
        print(3)
    except:
        print(4)
    else:
        print(5)
    print(6)

def TryExceptElseNamed():
    try:
        print(1)
    except A as a:
        print(2)
    except B as b:
        print(3)
    else:
        print(4)
    print(5)

def TryExceptElseMultiNamedAndUnnamed():
    try:
        print(1)
    except A as a:
       print(2)
    except b:
       print(3)
    except:
       print(4)
    else:
        print(5)
    print(6)

def TryFinallyBare():
    try:
        print(1)
    finally:
        print(2)
    print(3)

def TryExceptFinallyBare():
    try:
        print(1)
    except:
        print(2)
    finally:
        print(3)
    print(4)
##### NOT YET IMPLEMENTED #####
##### crashes cflow.py #####
##def TryExceptFinallyBareSpecific():
##    try:
##        print(1)
##    except a:
##        print(2)
##    finally:
##        print(3)
##    print(4)
##
##def TryExceptMultiFinally():
##    try:
##        print(1)
##    except a:
##        print(2)
##    except b:
##        print(3)
##    finally:
##        print(4)
##    print(5)
##
## Broken
##def TryExceptMultiFallbackFinally():
##    try:
##        print(1)
##    except a:
##        print(2)
##    except:
##        print(3)
##    finally:
##        print(4)
##    print(5)

def TryExceptMultiNamedFinally():
    try:
        print(1)
    except A as a:
        print(2)
    except B as b:
        print(3)
    finally:
        print(4)
    print(5)

def TryExceptMultiNamedFallbackFinally():
    try:
        print(1)
    except A as a:
        print(2)
    except:
        print(3)
    finally:
        print(4)
    print(5)

def TryExceptMultiNamedAndUnnamedFinally():
    try:
        print(1)
    except A as a:
       print(2)
    except b:
       print(3)
    except:
       print(4)
    finally:
        print(5)
    print(6)

def TryExceptElseFinallyBare():
    try:
        print(1)
    except:
        print(2)
    else:
        print(3)
    finally:
        print(4)
    print(5)

def TryExceptBareNested():
    try:
        print(1)
    except:
        print(2)
        try:
            print(3)
        except:
            print(4)

def TryExceptReturn():
    try:
        print(1)
        return 2
    except:
        print(2)

# Not currently working, see https://github.com/syssec-utd/pylingual/issues/24#issuecomment-3005215427
def TryExceptRaise():
    try:
        print(1)
    except:
        print(2)
        raise Exc

def TryExceptRaiseNamed():
    try:
        print(1)
    except A as a:
        print(2)
        raise Exc

### Expected to fail on 3.10- has the same issue as TryExceptFinally
def TryExceptBareNestedNamed():
    try:
        print(1)
    except A as a:
        print(2)
        try:
            print(3)
        except:
            print(4)

def TryExceptReturnNamed():
    try:
        print(1)
        return 2
    except A as a:
        print(2)

def TryExceptBareNestedMulti():
    try:
        print(1)
    except a:
        print(2)
        try:
            print(3)
        except:
            print(4)
    except b:
        print(5)
        try:
            print(6)
        except:
            print(7)

def TryExceptReturnMulti():
    try:
        print(1)
        return 2
    except a:
        print(2)
    except b:
        print(3)

def TryExceptRaiseMulti():
    try:
        print(1)
    except a:
        print(2)
        raise Exc
    except b:
        print(3)
        raise Exc
