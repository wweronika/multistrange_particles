{
//   macro to read xi data from an ascii file and
//   create a root file with an histogram and an ntuple.
   gROOT->Reset();
#include "Riostream.h"
#include "TH1F.h"
#include <TMath.h>
#include <TROOT.h>
#include <TStyle.h>
#include "TF1.h"

   ifstream in;
// we assume a file Xi.data in the current directory
// this file has 3 columns of float data
//   in.open("MC-xi-data.file");
   in.open("real-xi-data.file");
//in.open("MC-xi-data.file");


   Int_t icand;
   Float_t ximass,vmass,v0radius,casradius,cascos,v0cos,dacneg,dcapos,dcabach,dcaV0,dcacas,dcav0,dOverM,NsigPion,NsigProton,NsigBach;
   Int_t nlines = 0;
   TFile *f = new TFile("Xi-real.root","RECREATE");
   // Book histogram (one 1D and one 2D)
   TH1F *ximass1 = new TH1F("ximass1", "xi effective mass",100,1.31,1.33);
   ximass1->GetXaxis()->SetTitle("Effective #Lambda #pi  mass (GeV/c^{2})");
   ximass1->GetYaxis()->SetTitle("Events / 4 MeV");
   
   //vmass
   TH1F *vmass1 = new TH1F("vmass1", "v0 daughters effective mass",100,1.105,1.126);
   ximass1->GetXaxis()->SetTitle("Effective v0 daughters  mass (GeV/c^{2})");
   ximass1->GetYaxis()->SetTitle("Events / 4 MeV");
   
   
   TH2F *ximassNsigProton = new TH2F("ximassNsigProton","effective mass vs No. of Sigmas for proton", 50,1.2,1.6,50,-20.,20.);
   // book ntuples 
    TNtuple *ntuple = new TNtuple("ntuple","geometric data","icand:ximass:vmass:v0radius:casradius:cascos:v0cos:dacneg:dcapos:dcabach:dcaV0:dcacas:dcav0");
    TNtuple *ntuple2 = new TNtuple("ntuple2","other data","icand:ximass:dOverM:NsigPion:NsigProton:NsigBach");

   while (1) {
      in >> icand >> ximass >> vmass >> v0radius >> casradius >> cascos >> v0cos >> dacneg >> dcapos >> dcabach >> dcaV0 >> dcacas >> dcav0 >> dOverM >> NsigPion >> NsigProton >> NsigBach;
      if (!in.good()) break;
      if (icand < 5) printf("icand=%i, ximass=%8f, vmass=%8fn",icand,ximass,vmass);
      vmass1->Fill(vmass);
      ximassNsigProton->Fill(ximass,NsigProton);
      ximassNsigProton->SetOption("Box");
      ntuple->Fill(icand,ximass,vmass,v0radius,casradius,cascos,v0cos,dacneg,dcapos,dcabach,dcaV0,dcacas,dcav0);
      ntuple2->Fill(icand,ximass,dOverM,NsigPion,NsigProton,NsigBach);
      nlines++;
   }
   printf(" found %d pointsn",nlines);

   in.close();

// do the fitting
   TF1 *func=new TF1("fit","[0]*exp(-(x-[1])^2/(2*[2]^2))+[3]",1.00,1.5);
// set inital values of parameters in the fit
   func->SetParameter(0,100.);
   func->SetParameter(1,1.32);
   func->SetParameter(2,0.001);
   func->SetParameter(3,100.);
// set limits for parameters   
   func->SetParLimits(0,  50., 200.);
   func->SetParLimits(1, 1.11, 1.120);
   func->SetParLimits(2, 0.0003, 0.002);
   func->SetParLimits(3, 10., 150.);
//   func->SetParameter(4,40);
//
   func->SetParNames("constant","mean","sigma");
   vmass1->Fit("fit");    // do the fit
   cout<<"mean is: "<<func->GetParameter(1)<<endl;
   cout<<"sigma is: "<<func->GetParameter(2)<<endl;
   vmass1->Draw();
   func->Draw("same");

   f->Write();
}
