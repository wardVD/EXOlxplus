from ROOT import *
from array import array
from math import fabs, sqrt

#label function                                                                                                                                                                                                                                
def label(quadrant):
    if (quadrant!=1 and quadrant !=2):
        print "This quadrant is not defined, choose a value of 1 or 2!"
    else:
        if (quadrant == 1):
            x1 = 0.19
            x2 = 0.37
            y1 = 0.92
            y2 = 0.97
        if (quadrant == 2):
            x1 = 0.73
            x2 = 0.91
            y1 = 0.92
            y2 = 0.97

    headlabel = TPaveText( x1, y1, x2, y2, "brNDC" )
    if (quadrant == 1):
        headlabel.AddText("CMS = 19.3 fb^{-1}")
    if (quadrant == 2):
        headlabel.AddText("#sqrt{s} = 8 TeV")

    headlabel.SetFillColor(kWhite)
    headlabel.SetTextSize(0.04)
    headlabel.SetTextFont(42)
    headlabel.SetBorderSize(0)
    headlabel.SetShadowColor(kWhite)

    return headlabel

def loop(vec, photpt, phot):

    nPhot = 0
    nDxy = 0
    
    for i in vec:                            
        tree = i.Get("anaTree")
        entr = tree.GetEntries()
        j=0
        print 'total events ' + str(entr)
        for event in tree:

            if (event.ptPhot[0] < photpt):
                continue
            if (event.nPhot < phot):
                continue
            if (event.sMinPhot[0] < 0.15 or event.sMinPhot[0] > 0.3):
                continue
            if (event.ptJet[0] < (35+3.5)):
                continue
            if (event.sigmaIetaPhot[0] < 0.006 or event.sigmaIetaPhot[0] > 0.012):
                continue
            if (event.sMajPhot[0] > 1.35):
                continue
            for ding in event.ptPhot:
                nPhot = nPhot + 1

            for ding in event.dxyConv:
                nDxy = nDxy + 1
        
    vecnumber = [nPhot,nDxy]

    return vecnumber

def function (lamb,ctau,phot):

    listsig = ["./v21/GMSB_L"+lamb+"-CTAU"+ctau+".root"]
    
    vecfilessig = []
    for item in listsig:
        temp = TFile.Open(item)
        vecfilessig.append(temp)

    #arrays of nphot and nconversion for different photpt
    nPhotSig = [None]*14
    nConverSig = [None]*14

    nPhotSig[0] = loop(vecfilessig, 50,phot)[0]
    nPhotSig[1] = loop(vecfilessig, 60,phot)[0]
    nPhotSig[2] = loop(vecfilessig, 70,phot)[0]
    nPhotSig[3] = loop(vecfilessig, 80,phot)[0]
    nPhotSig[4] = loop(vecfilessig, 90,phot)[0]
    nPhotSig[5] = loop(vecfilessig, 100,phot)[0]
    nPhotSig[6] = loop(vecfilessig, 110,phot)[0]
    nPhotSig[7] = loop(vecfilessig, 120,phot)[0]
    nPhotSig[8] = loop(vecfilessig, 130,phot)[0]
    nPhotSig[9] = loop(vecfilessig, 140,phot)[0]
    nPhotSig[10] = loop(vecfilessig, 150,phot)[0]
    nPhotSig[11] = loop(vecfilessig, 160,phot)[0]
    nPhotSig[12] = loop(vecfilessig, 170,phot)[0]
    nPhotSig[13] = loop(vecfilessig, 180,phot)[0]

    nConverSig[0] = loop(vecfilessig, 50,phot)[1]
    nConverSig[1] = loop(vecfilessig, 60,phot)[1]
    nConverSig[2] = loop(vecfilessig, 70,phot)[1]
    nConverSig[3] = loop(vecfilessig, 80,phot)[1]
    nConverSig[4] = loop(vecfilessig, 90,phot)[1]
    nConverSig[5] = loop(vecfilessig, 100,phot)[1]
    nConverSig[6] = loop(vecfilessig, 110,phot)[1]
    nConverSig[7] = loop(vecfilessig, 120,phot)[1]
    nConverSig[8] = loop(vecfilessig, 130,phot)[1]
    nConverSig[9] = loop(vecfilessig, 140,phot)[1]
    nConverSig[10] = loop(vecfilessig, 150,phot)[1]
    nConverSig[11] = loop(vecfilessig, 160,phot)[1]
    nConverSig[12] = loop(vecfilessig, 170,phot)[1]
    nConverSig[13] = loop(vecfilessig, 180,phot)[1]

    Efficiencies = [None]*14
    EfficiencyHist = TH1D("Efficiencies","",14,40,180)
    EfficiencyHist.SetMarkerStyle(3)
    EfficiencyHist.SetMarkerSize(1.1)
    
    for i in range(len(nPhotSig)):
        #print "nConv: " + str(nConverSig[i]) + " for photpt " + str(50+i*10) + "GeV"
        #print "nPhot: "+ str(nPhotSig[i]) + " for photpt " +str(50+i*10) + "GeV"
        Efficiencies[i] = float(nConverSig[i])/nPhotSig[i]
        #print Efficiencies[i]
        EfficiencyHist.SetBinContent(i+1,Efficiencies[i])

    return EfficiencyHist

def main():
    cmslabel = label(1)
    sqrtlabel = label(2)
    CTAU10 = function("180","10",2)
    CTAU50 = function("180","50",2)
    CTAU250 = function("180","250",2)
    CTAU500 = function("180","500",2)

    c1 = TCanvas("c1","c1",600,500)
    gStyle.SetOptStat(000000000)
    c1.SetBottomMargin(0.15)
    c1.SetLeftMargin(0.15)
    CTAU10.SetMarkerColor(1)
    CTAU50.SetMarkerColor(2)
    CTAU250.SetMarkerColor(5)
    CTAU500.SetMarkerColor(4)
    leg = TLegend(0.45,0.70,0.89,0.89)
    leg.SetFillColor(kWhite)
    leg.SetTextSize(0.038)
    leg.SetTextFont(42)
    leg.SetBorderSize(0)
    leg.AddEntry(CTAU10, "GMSB(180 GeV, 1 cm)","p")
    leg.AddEntry(CTAU50, "GMSB(180 GeV, 5 cm)","p")
    leg.AddEntry(CTAU250, "GMSB(180 GeV, 25 cm)","p")
    leg.AddEntry(CTAU500, "GMSB(180 GeV, 50 cm)","p")
    CTAU10.Draw("P")
    CTAU10.GetYaxis().SetRangeUser(0,0.2)
    CTAU10.GetYaxis().SetTitleSize(0.05)
    CTAU10.GetYaxis().SetTitleOffset(1.4)
    CTAU10.GetYaxis().SetTitle("Conversion Reconstruction Efficiency")
    CTAU10.GetXaxis().SetTitle("Photon p_{T} (GeV)")
    CTAU10.GetXaxis().SetTitleSize(0.05)
    CTAU10.GetXaxis().SetTitleOffset(1.)
    CTAU10.Draw("Psame")
    CTAU50.Draw("Psame")
    CTAU250.Draw("Psame")
    CTAU500.Draw("Psame")
    leg.Draw("same")
    cmslabel.Draw("same")
    sqrtlabel.Draw("same")
    c1.SaveAs("./dxyefficiencyL180.png")


if __name__ == "__main__":
    main()

