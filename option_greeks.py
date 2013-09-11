import sys
import os
import math


"""
Black-Scholes-Merton method to calculate option premium for forward or futures contract
@param callPutFlag
@param F future price
@param X strike price
@param T time to expiration
@param r risk-free interest rate
@param v implied volatility
@return Double option premium
"""
def BlackScholes(callPutFlag, f, x, t, r, v):
    d1 = (math.log(f / x) + (math.pow(v,2) / 2) * t) / (v * math.sqrt(t))
    d2 = d1 - v * math.sqrt(t)
    premium = 0
    if (callPutFlag == "c"):
        premium = math.exp(-1 * r * t) * (f * CND(d1) - x * CND(d2))
    elif (callPutFlag == "p"):
        premium = math.exp(-1 * r * t) * (x * CND(-1 * d2) - f * CND(-1 * d1))

    return premium


"""
Cumulative Normal Distribution Function using Hart Algorithm
Hart, J.F. et al, 'Computer Approximations', Wiley 1968
@param X
@return Double cumulative normal distribution
"""
def CND(x):
    y = abs(x)

    if (x > 37):
        cnd = 1
        return cnd
    elif (x < -37):
        cnd = 0
        return cnd
    else:
        exponential = math.exp(-1 * y * y / 2)
        if (y < 7.07106781186547):
            sumA = 0.0352624965998911 * y + 0.700383064443688
            sumA = sumA * y + 6.373962203531650
            sumA = sumA * y + 33.91286607838300
            sumA = sumA * y + 112.0792914978709
            sumA = sumA * y + 221.2135961699311
            sumA = sumA * y + 220.2068679123761
            sumB = 0.0883883476483184 * y + 1.75566716318264
            sumB = sumB * y + 16.06417757920695
            sumB = sumB * y + 86.78073220294608
            sumB = sumB * y + 296.5642487796737
            sumB = sumB * y + 637.3336333788311
            sumB = sumB * y + 793.8265125199484
            sumB = sumB * y + 440.4137358247522
            cnd = exponential * sumA / sumB
        else:
            sumA = y + 0.65
            sumA = y + 4 / sumA
            sumA = y + 3 / sumA
            sumA = y + 2 / sumA
            sumA = y + 1 / sumA
            cnd = exponential / (sumA * 2.506628274631001)
    if (x > 0):
        cnd = 1 - cnd

    return cnd


def phi(x):
    'Cumulative distribution function for the standard normal distribution'
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


"""
calculates delta, b = 0 for futures option
Delta is the option's sensitivity to small changes in the underlying asset price
@param callPutFlag
@param F future price
@param X strike price
@param T time to expiration
@param r risk-free interest rate
@param b cost of carry
@param v implied volatility
@return Double Delta
"""
def Delta(callPutFlag, f, x, t, r, b, v):
    delta = 0
    d1 = (math.log(f / x) + (b + v * v / 2) * t) / (v * math.sqrt(t))
    if (callPutFlag == "c"):
        delta = math.exp(-1 * r * t) * CND(d1)
    else:
        delta = -1 * math.exp(-1 * r * t) * CND(-1 * d1)
    return delta
    

"""
calculates vega, b = 0 for futures option
Vega is the option's sensitivity to a small change in the volatility of the underlying asset.
@param F future price
@param X strike price
@param T time to expiration
@param r risk-free interest rate
@param b cost of carry
@param v implied volatility
@return Double Vega
"""
def Vega(f, x, t, r, b, v):
    d1 = (math.log(f / x) + (b + v * v / 2) * t) / (v * math.sqrt(t))
    nd1 = (1 / math.sqrt(2 * math.pi)) * math.exp(-1 * d1 * d1 / 2)
    vega = f * math.exp((b - r) * t) * (nd1 * math.sqrt(t))
    return vega

def onePercentVega(f, x, t, r, b, v):
    vega = Vega(f, x, t, r, b, v)
    return vega / 100


"""
Gamma is the delta's sensitivity to small changes in the underlying asset price
@param F future price
@param X strike price
@param T time to expiration
@param r risk-free interest rate
@param b cost of carry
@param v implied volatility
@return Double Gamma
"""
def Gamma(f, x, t, r, b, v):
    d1 = (math.log(f / x) + (b + v * v / 2) * t) / (v * math.sqrt(t))
    nd1 = (1 / math.sqrt(2 * math.pi)) * math.exp(-1 * d1 * d1 / 2)
    gamma = (nd1 * math.exp((b - r) * t)) / (f * v * math.sqrt(t))
    return gamma


def Theta(callPutFlag, f, x, t, r, b, v):
    d1 = (math.log(f / x) + (b + v * v / 2) * t) / (v * math.sqrt(t))
    d2 = d1 - v * math.sqrt(t)
    nd1 = (1 / math.sqrt(2 * math.pi)) * math.exp(-1 * d1 * d1 / 2)
    theta = 0
    if (callPutFlag == "p"):
        nnd1 = CND(-1 * d1)
        nnd2 = CND(-1 * d2)
        theta = (-1 * f * math.exp((b - r) * t) * nd1 * v) / (2 * math.sqrt(t)) + (b - r) * f * math.exp((b - r) * t) * nnd1 + r * x * math.exp(-1 * r * t) * nnd2
    elif (callPutFlag == "c"):
        nd1 = CND(d1)
        nd2 = CND(d2)
        theta = (-1 * f * math.exp((b - r) * t) * nd1 * v) / (2 * math.sqrt(t)) - (b - r) * f * math.exp((b - r) * t) * nd1 - r * x * math.exp(-1 * r * t) * nd2
    # divide by 365 to get theta for a one-day time decay
    return theta / 365


"""
Newton-Raphson method to calculate implied volatility for future
b = 0 gives Black(1976) futures option model.
@param callPutFlag
@param F future price
@param X strike price
@param T time to expiration
@param r risk-free interest rate
@param b cost of carry
@param cm market price for option
@param epsilon desired degree of accuracy
@return Double implied volatility
"""
def ImpliedVolatilityNR(callPutFlag, f, x, t, r, b, cm, epsilon):
    # Manaster and Koehler seed value (vi)
    vi = math.sqrt(abs(math.log(f / x)) * 2 / t)
    ci = BlackScholes(callPutFlag, f, x, t, r, vi)
    vegai = Vega(f, x, t, r, 0.0, vi)
    minDiff = abs(cm - ci)

    while (abs(cm - ci) >= epsilon and abs(cm - ci) <= minDiff):
        vi = vi - (ci - cm) / vegai
        ci = BlackScholes(callPutFlag, f, x, t, r, vi)
        vegai = Vega(f, x, t, r, 0.0, vi)
        minDiff = abs(cm - ci)

    if (abs(cm - ci) < epsilon):
        impliedVolatility = vi
    else:
        impliedVolatility = None

    return impliedVolatility
    

print "CND with Hart Algorithm\n"
print CND(-0.54)
print "CND with python erf()\n"
print phi(-0.54)
premium = BlackScholes("c", 187.93, 195.0, 15.0/365.0, 0, 0.15525)
print "call, f=5569.97, x=6000, t=139, r=0.0231, v=0.18611 \n"
print "premium: " + str(premium)
delta = Delta("c", 187.93, 195.0, 15.0/365.0, 0, 0, 0.15525)
print "delta: " + str(delta)
impliedVol = ImpliedVolatilityNR("c", 187.93, 195.0, 15.0/365.0, 0, 0, 0.36, 0.0001)
print "implied vol: " + str(impliedVol)

