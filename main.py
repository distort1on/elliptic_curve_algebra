#  Copyright (c) 2022. Illia Popov.

from dataclasses import dataclass
import random
import math 


def extended_euclidean_algorithm(a, b):
    """
    ax + by = gcd (a,b)
    :return: gcd (a, b), x, y
    """
    if a == 0:
        return b, 0, 1
    else:
        _gcd, x, y = extended_euclidean_algorithm(b % a, a)
        return _gcd, y - (b // a) * x, x

def modular_multiplicative_inverse(a, m):
    # a*x ≡ 1 mod m; gcd(a, m) = 1
    if a < 0:
        return m - modular_multiplicative_inverse(-a, m)

    d = extended_euclidean_algorithm(a, m)[1] % m

    return d


@dataclass
class Point:
    x: float
    y: float


class EllipticCurve:
    def __init__(self, _a: float, _b: float, _p: int):
        self.a = _a
        self.b = _b
        self.p = _p
        #self.n
        

class ECPoint:

    @staticmethod
    def BasePointGGet(curve: EllipticCurve):
        """
        Think that all points on curve are equally good to be the base point
        """
        pass


    @staticmethod
    def ECPointGen(x: float, y: float) -> Point:
        return Point(x, y)

    @staticmethod
    def IsOnCurveCheck(a: Point, curve: EllipticCurve) -> bool:
        return (a.y**2 - a.x**3 - curve.a*a.x - curve.b) % curve.p == 0

    @staticmethod
    def AddECPoints(a: Point, b: Point, curve: EllipticCurve) -> Point:
        if a != b:
            m = (a.y - b.y) * modular_multiplicative_inverse(a.x - b.x, curve.p)
        else:
            m =  (3 * a.x**2 + curve.a) * modular_multiplicative_inverse(2 * a.y, curve.p)

        x_r = (m**2 - a.x - b.x) % curve.p
        y_r = -(a.y + m * (x_r - a.x)) % curve.p

        if not ECPoint.IsOnCurveCheck(Point(x_r, y_r), curve):
            return None

        return Point(x_r, y_r)

    @staticmethod
    def DoubleECPoints(point: Point, curve: EllipticCurve) -> Point:
        m = (3 * point.x**2 + curve.a) * modular_multiplicative_inverse(2 * point.y, curve.p)
        x_r = (m**2 - point.x - point.x) % curve.p
        y_r = -(point.y + m * (x_r - point.x)) % curve.p

        if not ECPoint.IsOnCurveCheck(Point(x_r, y_r), curve):
            return None
        return Point(x_r, y_r)

    @staticmethod
    def ScalarMult(a: Point, k: int, curve: EllipticCurve) -> Point:

        res_point = a

        for i in range(2, k + 1):
            if res_point is None:
                    res_point = a
                    i += 1
            else:
                res_point = ECPoint.AddECPoints(res_point, a, curve)
           
            
        return res_point

    @staticmethod
    def ECPointToString(point: Point) -> str:
        return point.__str__()

    @staticmethod
    def PrintECPoint(point: Point) -> None:
        print(ECPoint.ECPointToString(point))


def find_order(point: ECPoint, curve: EllipticCurve):
    n = 2
    sum_point = ECPoint.DoubleECPoints(point, curve)

    while True:
        if sum_point is None:
            return n
        sum_point = ECPoint.AddECPoints(sum_point, point, curve)
        n += 1


def test_operations():
    test_curve = EllipticCurve(-7, 10, 13)
    print('Curve: y^2 = x^3 - 7*x + 10 (mod 13)\n')

    #_g, _subgroup = ECPoint.BasePointGGet(10, curve=test_curve)
    #print(f'Base point - {_g} \nSubgroup: {_subgroup}\n')

    print(f'(1, 2) + (3, 4) = {ECPoint.AddECPoints(Point(1,2), Point(3,4), test_curve)}\n')
    
    print(f'Double (1, 2) = {ECPoint.DoubleECPoints(Point(1, 2), curve=test_curve)}\n')

    print(f'5 * (1, 2) = {ECPoint.ScalarMult(Point(1, 2), 5, curve=test_curve)}\n')

    test_point = ECPoint.ECPointGen(1, 2)
    print(f'Gen point (1, 2) -> {test_point}\n')
    ECPoint.PrintECPoint(test_point)


def test_shared_secret():
    test_curve = EllipticCurve(2, 3, 1861)
    print('Curve: y^2 = x^3 + 2*x + 3 (mod 1861)\n')

    _g = Point(1359, 1854)
    order = 956
    print(f'Base point - {_g} \n')
    

    alice_private_key = random.randint(1, order - 1)
    alice_public_key = ECPoint.ScalarMult(_g, alice_private_key, test_curve)
    print ("Alice public key: ", alice_public_key)

    bob_private_key = random.randint(1, order - 1)
    bob_public_key = ECPoint.ScalarMult(_g, bob_private_key, test_curve)
    print ("Bob public key: ", bob_public_key)

    alice_shared_key = ECPoint.ScalarMult(bob_public_key, alice_private_key, test_curve)
    bob_shared_key = ECPoint.ScalarMult(alice_public_key, bob_private_key, test_curve)

    print(f"\nAlice shared key = {alice_shared_key.x}\nBob shared key = {bob_shared_key.x}")



if __name__ == "__main__":
    test_shared_secret()
    #test_operations()
    
    
