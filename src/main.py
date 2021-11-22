from paynet import paynet

p = paynet.Paynet("https://ebill-ki.postfinance.ch/B2BService/B2BService.svc", True)
p.ping()
