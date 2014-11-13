from ROOT import *
from tdrStyle import *
from array import *

setTDRStyle()
                
def Draw(vec):
    vec[0].SetLineColor(kBlue)
    vec[1].SetLineColor(kRed)
    vec[0].SetLineWidth(2)
    vec[1].SetLineWidth(2)
    #print vec[1].GetFillStyle()
    #vec[1].SetFillStyle(3004)
    vec[0].SetFillStyle(3005)
    vec[0].SetFillColor(kBlue)
    #vec[1].SetFillColor(kOrange)
    stack = THStack("stack","")
    stack.Add(vec[0])
    stack.Add(vec[1])
    c1 = TCanvas("c1","c1",600,500)
    #c1.SetLogy()
    leg = TLegend(0.65,0.70,0.89,0.89)
    leg.SetFillColor(kWhite)
    leg.SetTextSize(0.03)
    leg.SetTextFont(42)
    leg.SetBorderSize(0)
    leg.AddEntry(vec[0], "TTJets","f")
    leg.AddEntry(vec[1], "GMSB(180 GeV, 50 cm)","f")
    vec[0].Draw("")
    vec[0].GetXaxis().SetTitle("Photon Matched to Electron")
    vec[0].GetYaxis().SetTitle("Number of Events")
    vec[0].GetYaxis().SetRangeUser(10000,2000000)
    vec[1].Draw("same")
    #stack.Draw("same")
    leg.Draw("same")
    
    c1.SaveAs("phomatchedele.png")
    c1.Close()
    
def function():
    input1 = TFile.Open("../DPAnalysis/test/v21/TTJets.root")
    input2 = TFile.Open("../DPAnalysis/test/v21/GMSB_L180-CTAU500.root")
    tree1 = input1.Get("DPAnalysis")
    tree2 = input2.Get("DPAnalysis")
    xbins = array('d',[-0.5,0.,0.5,1.,1.5])
    h1 = TH1F("h1","",2,-0.5,1.5)
    h2 = TH1F("h2","",2,-0.5,1.5)
    h1.SetNdivisions(2)
    h2.SetNdivisions(2)
    tree1.Draw("phoMatchedEle>>h1")
    tree2.Draw("phoMatchedEle>>h2")
    vec = [h1,h2]
    
    Draw(vec)

     
function()
