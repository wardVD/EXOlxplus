from ROOT import *
from array import array
from math import fabs, sqrt
from tdrStyle import *

setTDRStyle()

def label(quadrant):
    if (quadrant!=1 and quadrant !=2):
        print "This quadrant is not defined, choose a value of 1 or 2!"
    else:
        if (quadrant == 1):
            x1 = 0.1
            x2 = 0.28
            y1 = 0.95
            y2 = 1.0
        if (quadrant == 2):
            x1 = 0.75
            x2 = 0.93
            y1 = 0.95
            y2 = 1.0
            
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


def loop(vec,vechisto,flag):
    for i in vec:
        tree = i.Get("anaTree")
        entr = tree.GetEntries()
        print 'total events ' + str(entr)
        for event in tree:
            if (event.nPhot < 1):
                continue
            if (event.nJet < 2):
                continue
            if(flag == 0):
                lum = 19300.
                for i in range(len(event.dxyConv)):
                    vechisto.Fill(abs(event.dxyConv[i]),(event.CrossSectionWeight*lum)/(event.EfficiencyScaleFactors) )
            else:
                for i in range(len(event.dxyConv)):
                    vechisto.Fill(abs(event.dxyConv[i]), 1./event.EfficiencyScaleFactors )

    return vechisto


def function():
    listgjet = ["./v21/G_Pt-50to80loose.root","./v21/G_Pt-80to120loose.root","./v21/G_Pt-120to170loose.root","./v21/G_Pt-170to300loose.root","./v21/G_Pt-300to470loose.root","./v21/G_Pt-470to800loose.root"]
    listgjetlowmet = ["./v21/G_Pt-50to80_lowmet.root","./v21/G_Pt-80to120_lowmet.root","./v21/G_Pt-120to170_lowmet.root","./v21/G_Pt-170to300_lowmet.root","./v21/G_Pt-300to470_lowmet.root","./v21/G_Pt-470to800_lowmet.root"]

    vecfilesgjet = []
    for item in listgjet:
        temp = TFile.Open(item)
        vecfilesgjet.append(temp)
    vecfilesgjetlowmet = []
    for item in listgjetlowmet:
        temp = TFile.Open(item)
        vecfilesgjetlowmet.append(temp)

    #xbins = array('d',[0.,0.1,0.2,0.6,2.5])
    xbins = array('d',[0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,2.5])

    dxygjet = TH1D("dXYgjet","",9,xbins)
    dxygjetlowmet = TH1D("dXYgjetlowmet","",9,xbins)
    #dxygjet = TH1D("dXYgjet","",25,0,2.5)
    #dxygjetlowmet = TH1D("dXYgjetlowmet","",25,0,2.5)
    dxygjet.Sumw2()
    dxygjetlowmet.Sumw2()

    dxygjet = loop(vecfilesgjet,dxygjet,0)
    dxygjetlowmet = loop(vecfilesgjetlowmet,dxygjetlowmet,0)

    dxygjet.SetBinContent(50,dxygjet.GetBinContent(51))
    dxygjetlowmet.SetBinContent(50,dxygjetlowmet.GetBinContent(51))

    #ratiogjet = dxyiso.GetBinContent(1)/dxygjet.GetBinContent(1)
    ratiogjetlowmet = dxygjet.GetBinContent(1)/dxygjetlowmet.GetBinContent(1)
    
    dxygjetlowmet.Scale(ratiogjetlowmet)
    
    dxy = [dxygjet,dxygjetlowmet]

    return dxy

def plot(dxy,cmslabel,sqrtlabel):
    dxy[1].SetFillStyle(3001)
    dxy[0].SetLineWidth(2)
    dxy[0].SetLineColor(kRed)
    dxy[1].SetFillColor(kOrange)
    dxy[0].SetMarkerColor(kRed)
    
    n = dxy[1].GetNbinsX()
    x = array('d',[])
    y = array('d',[])
    ex = array('d',[])
    ey = array('d',[])

    for km in range(n):
        conte = dxy[1].GetBinError(km)
        x.append(float(dxy[1].GetBinCenter(km)))
        y.append(float(dxy[1].GetBinContent(km)))
        ex.append(float(dxy[1].GetBinWidth(km)/2))
        ey.append(float(conte))

    errhist = TGraphErrors(n,x,y,ex,ey,)
    errhist.SetFillColor(1)
    errhist.SetLineWidth(3)
    errhist.SetFillStyle(3005)

    c1 = TCanvas("c1","c1",600,500)
    c1.SetLogy()
    leg = TLegend(0.55,0.75,0.89,0.89)
    leg.SetFillColor(kWhite)
    leg.SetTextSize(0.03)
    leg.SetTextFont(42)
    leg.SetBorderSize(0)
    leg.AddEntry(dxy[1], "#gamma + jets (CR 1 selection)","f")
    leg.AddEntry(dxy[0], "#gamma + jets (signal region selection)","l")

    dxy[1].GetXaxis().SetTitle("d_{XY} (cm)")
    dxy[1].GetYaxis().SetTitle("Events")
    #dxy[1].GetYaxis().SetRangeUser(1,1000)
    
    dxy[1].Draw("HIST")
    dxy[0].Draw("EsameHIST")
    errhist.Draw("2 sames")
    cmslabel.Draw("same")
    sqrtlabel.Draw("same")
    leg.Draw("same")
    c1.RedrawAxis()

    c1.SaveAs("dxycomparisongjet.png")
    c1.Close()
    
def main():
    dxy = function()
    cmslabel = label(1)
    sqrtlabel = label(2)
    plot(dxy,cmslabel,sqrtlabel)

if __name__ == "__main__":
    main()
