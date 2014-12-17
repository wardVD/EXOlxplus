from ROOT import *
from array import array
from math import fabs, sqrt
import CMS_lumi, tdrstyle

#set the tdr style                                                                                                                                                                                                                             
tdrstyle.setTDRStyle()

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

def plot(dxy):
    dxy[2].SetFillStyle(3001)
    dxy[0].SetLineWidth(2)
    dxy[1].SetLineWidth(2)
    dxy[0].SetLineColor(kBlack)
    dxy[1].SetLineColor(kRed)
    dxy[2].SetFillColor(kOrange)
    
    leg = TLegend(0.65,0.75,0.89,0.89)
    leg.SetFillColor(kWhite)
    leg.SetTextSize(0.03)
    leg.SetTextFont(42)
    leg.SetBorderSize(0)
    leg.AddEntry(dxy[2], "Control region 1","f")
    leg.AddEntry(dxy[1], "Control region 2","l")
    leg.AddEntry(dxy[0], "Control region 3","l")

    dxy[1].GetXaxis().SetTitle("Conversion d_{XY} (cm)")
    dxy[1].GetYaxis().SetTitle("Events")
    dxy[1].GetYaxis().SetRangeUser(1,10000)
    dxy[1].GetYaxis().SetTitleSize(0.05)
    dxy[1].GetXaxis().SetTitleSize(0.05)

    gStyle.SetOptStat(0)

    #change the CMS_lumi variables (see CMS_lumi.py)

    CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
    CMS_lumi.lumi_8TeV = "19.3 fb^{-1}"
    CMS_lumi.writeExtraText = 1
    CMS_lumi.extraText = "Simulation"

    iPos = 11
    if( iPos==0 ): CMS_lumi.relPosX = 0.12

    H_ref = 600;
    W_ref = 800;
    W = W_ref
    H  = H_ref

    #
    # Simple example of macro: plot with CMS name and lumi text
    #  (this script does not pretend to work in all configurations)
    # iPeriod = 1*(0/1 7 TeV) + 2*(0/1 8 TeV)  + 4*(0/1 13 TeV)                                                                                                                                                                                
    # For instance:
    #               iPeriod = 3 means: 7 TeV + 8 TeV
    #               iPeriod = 7 means: 7 TeV + 8 TeV + 13 TeV
    # references for T, B, L, R

    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.12*W_ref
    R = 0.04*W_ref

    canvas = TCanvas("c2","c2",50,50,W,H)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0)
    canvas.SetLogy()

    dxy[1].Draw("")
    dxy[0].Draw("same")
    dxy[2].Draw("same")
    dxy[1].Draw("same")
    dxy[0].Draw("same")
    leg.Draw("same")


    #draw the lumi text on the canvas
    CMS_lumi.CMS_lumi(canvas, 2, iPos)

    canvas.cd()
    canvas.Update()
    canvas.RedrawAxis()
    frame = canvas.GetFrame()
    frame.Draw()
    
    canvas.SaveAs("dxycomparisonfakehighfakelowisolow.png")
    canvas.Close()
    
def main():
    dxy = function()
    plot(dxy)

if __name__ == "__main__":
    main()
