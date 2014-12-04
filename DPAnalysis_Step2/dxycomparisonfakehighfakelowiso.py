
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
            if(flag == 0):
                lum = 19300.
                if(event.dxyConv.size() > 0):
                    vechisto.Fill(event.dxyConv[0],(event.CrossSectionWeight*lum)/(event.EfficiencyScaleFactors) )
            else:
                if(event.dxyConv.size() > 0):
                    vechisto.Fill(event.dxyConv[0], 1./event.EfficiencyScaleFactors )

    return vechisto


def function():
    listhigh = ["./v21_2/Run2012Afakehigh.root","./v21_2/Run2012Bfakehigh.root","./v21_2/Run2012C_1fakehigh.root","./v21_2/Run2012C_2fakehigh.root","./v21_2/Run2012C_3fakehigh.root","./v21_2/Run2012D_1fakehigh.root","./v21_2/Run2012D_2fakehigh.root","./v21_2/Run2012D_3fakehigh.root"]
    listlow = ["./v21_2/Run2012Afakelow.root","./v21_2/Run2012Bfakelow.root","./v21_2/Run2012C_1fakelow.root","./v21_2/Run2012C_2fakelow.root","./v21_2/Run2012C_3fakelow.root","./v21_2/Run2012D_1fakelow.root","./v21_2/Run2012D_2fakelow.root","./v21_2/Run2012D_3fakelow.root"]
    listiso = ["./v21_2/Run2012Aisolow.root","./v21_2/Run2012Bisolow.root","./v21_2/Run2012C_1isolow.root","./v21_2/Run2012C_2isolow.root","./v21_2/Run2012C_3isolow.root","./v21_2/Run2012D_1isolow.root","./v21_2/Run2012D_2isolow.root","./v21_2/Run2012D_3isolow.root"]

    vecfileshigh = []
    for item in listhigh:
        temp = TFile.Open(item)
        vecfileshigh.append(temp)
    vecfileslow = []
    for item in listlow:
        temp = TFile.Open(item)
        vecfileslow.append(temp)
    vecfilesiso = []
    for item in listiso:
        temp = TFile.Open(item)
        vecfilesiso.append(temp)

    dxyhigh = TH1D("dXYhigh","",25,0,2.5)
    dxylow = TH1D("dXYlow","",25,0,2.5)
    dxyiso = TH1D("dXYiso","",25,0,2.5)

    dxyhigh = loop(vecfileshigh,dxyhigh,1)
    dxylow = loop(vecfileslow,dxylow,1)
    dxyiso = loop(vecfilesiso,dxyiso,1)

    dxyhigh.SetBinContent(50,dxyhigh.GetBinContent(51))
    dxylow.SetBinContent(50,dxylow.GetBinContent(51))
    dxyiso.SetBinContent(50,dxyiso.GetBinContent(51))

    """
    ratiolow = dxyhigh.Integral()/dxylow.Integral()
    ratioiso = dxyhigh.Integral()/dxyiso.Integral()
    """

    ratiolow = dxyiso.GetBinContent(1)/dxylow.GetBinContent(1)
    ratiohigh = dxyiso.GetBinContent(1)/dxyhigh.GetBinContent(1)
    
    dxylow.Scale(ratiolow)
    dxyhigh.Scale(ratiohigh)

    dxy = [dxyhigh,dxylow,dxyiso]

    return dxy

def plot(dxy,cmslabel,sqrtlabel):
    dxy[2].SetFillStyle(3001)
    dxy[0].SetLineWidth(2)
    dxy[1].SetLineWidth(2)
    dxy[0].SetLineColor(kBlack)
    dxy[1].SetLineColor(kRed)
    dxy[2].SetFillColor(kOrange)
    

    c1 = TCanvas("c1","c1",600,500)
    c1.SetLogy()
    leg = TLegend(0.65,0.75,0.89,0.89)
    leg.SetFillColor(kWhite)
    leg.SetTextSize(0.03)
    leg.SetTextFont(42)
    leg.SetBorderSize(0)
    leg.AddEntry(dxy[2], "Control region 1","f")
    leg.AddEntry(dxy[1], "Control region 2","l")
    leg.AddEntry(dxy[0], "Control region 3","l")

    dxy[1].GetXaxis().SetTitle("d_{XY} (cm)")
    dxy[1].GetYaxis().SetTitle("Events")
    
    dxy[1].Draw("")
    dxy[0].Draw("same")
    dxy[2].Draw("same")
    dxy[1].Draw("same")
    dxy[0].Draw("same")
    cmslabel.Draw("same")
    sqrtlabel.Draw("same")
    leg.Draw("same")
    c1.RedrawAxis()

    c1.SaveAs("dxycomparisonfakehighfakelowisolow.png")
    c1.Close()
    
def main():
    dxy = function()
    cmslabel = label(1)
    sqrtlabel = label(2)
    plot(dxy,cmslabel,sqrtlabel)

if __name__ == "__main__":
    main()
