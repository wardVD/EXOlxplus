#include "TColor.h"
#include "TStyle.h"
#include "TMath.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TTree.h"
#include "TGraph.h"
#include "TMultiGraph.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TPolyLine.h"
#include "TROOT.h"
#include "setTDRStyle.C"
#include "TF1.h"
#include "TGaxis.h"

using namespace std;
void rootlogon();

void plot_limit_mass(){

  rootlogon();

  gStyle->SetOptStat(0);

  Double_t ctau160[4] = {1.2,100,100,1.2};
  Double_t ctau180[4] = {3.5,60,60,3.5};

  Double_t mTh[2] = {160,180};

  Double_t x_pdf[5] = {160,180,180,160,160};

  
  Double_t y_pdf_exp[5] = {  ctau160[0],
			     ctau180[0],
			     ctau180[1],
			     ctau160[1],
                             ctau160[0]};

  Double_t y_pdf_obs[5] = {  ctau160[3],
                             ctau180[3],
                             ctau180[2],
                             ctau160[2],
                             ctau160[3]};


  TGraph* Exp_graph;
  Exp_graph = new TGraph(5, x_pdf, y_pdf_exp );

  TGraph* Obs_graph;
  Obs_graph = new TGraph(5, x_pdf, y_pdf_obs );

  Obs_graph->SetFillColor(kGreen);
  Exp_graph->SetLineColor(kRed);
  Exp_graph->SetLineWidth(2);
  Exp_graph->SetFillColor(kRed);
  
  TCanvas* c0 = new TCanvas("exclusion limit", "exclusion limit", 1);
  c0->cd();
  c0->SetLogy();
  c0->Range(83.19049,-3.60972,185.6367,1.040413);
  c0->SetFillColor(0);
  c0->SetBorderMode(0);
  c0->SetBorderSize(2);
  c0->SetTickx(1);
  c0->SetTicky(1);
  c0->SetLeftMargin(0.159396);
  c0->SetRightMargin(0.05033557);
  c0->SetTopMargin(0.07342657);
  c0->SetBottomMargin(0.1311189);
  c0->SetFrameFillStyle(0);
  c0->SetFrameBorderMode(0);
  c0->SetFrameFillStyle(0);
  c0->SetFrameBorderMode(0); 


  Exp_graph->SetTitle("");
  Exp_graph->GetXaxis()->SetTitle("#Lambda [TeV]");
  Exp_graph->GetYaxis()->SetTitle("c#tau_{#tilde{#chi^{0}_{1}} #rightarrow #tilde{G}#gamma} (cm)");
  Exp_graph->GetYaxis()->SetRangeUser(0.1, 2000);
  Exp_graph->GetXaxis()->SetRangeUser(140, 200);
  Exp_graph->GetXaxis()->SetTitleSize(0.048);
  Exp_graph->GetXaxis()->SetTitleOffset(1.24);
  Exp_graph->GetYaxis()->SetTitleSize(0.048);
  Exp_graph->GetYaxis()->SetTitleOffset(1.6);

  Exp_graph->Draw("AL");
  //Obs_graph->Draw("Fsame");

  c0->Update();
  c0->RedrawAxis();

  // integrated luminosity
  std::string s_lumi;
  s_lumi = "19.3";
  std::string lint = "#intL = "+s_lumi+" fb^{-1}";
  TLatex l1;
  l1.SetTextAlign(12);
  l1.SetTextSize(0.027);
  l1.SetTextFont(22);
  l1.SetNDC();
  l1.DrawLatex(0.155, 0.964, "CMS Preliminary");
  l1.DrawLatex(0.75, 0.958, lint.c_str());
  
   
  TLegend* leg = new TLegend(0.55,0.8,0.9,0.93);
  leg->SetFillStyle(0); leg->SetBorderSize(0);
  leg->SetFillColor(0);

 
  leg->SetHeader("");
  leg->SetTextFont(22);
  leg->SetTextSize(0.04);
  //leg->AddEntry(Obs_graph, "#pm 1 #sigma Expected", "F");
  leg->AddEntry(Exp_graph, "Expected exclusion", "L");
  leg->Draw("same");

  c0->SaveAs("2Dexclusion_limit.pdf");

}

void rootlogon() {
  gROOT->SetStyle("Plain");
  gStyle->SetPalette(1);
  gStyle->SetOptStat(1111111);  // Show overflow, underflow + SumOfWeights 
  gStyle->SetOptFit(111110);
  gStyle->SetOptFile(1);
  gStyle->SetMarkerStyle(20);
  gStyle->SetMarkerSize(2.);
  gStyle->SetMarkerColor(1);
  gStyle->SetTitleOffset(1.20,"Y");

  //define high def color palette
  const Int_t NRGBs = 5;
  const Int_t NCont = 255;

  Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
  Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
  Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
  Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
  TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
  gStyle->SetNumberContours(NCont);

  cout << "loading TDR style and setting as default" << endl;
  gROOT->ProcessLine(".L tdrstyle.C");
  setTDRStyle();

}
