//---------------------------------------------------------------------------

#include <fmx.h>
#pragma hdrstop

#include "Unit1.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.fmx"
TForm1 *Form1;

const int X1=100;
const int X2=300;
const int X3=500;
const int Y=400;

//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
	Height=300;
}
//---------------------------------------------------------------------------
inline void TForm1::Put(Column &From,Column &To,Column &Free,int CountMoveFrom)
{
	CountMoves++;
	if(CountMoveFrom!=1)	{
		Put(From,Free,To,CountMoveFrom-1);


		Moves.Length++;
		Moves[Moves.Length-1]=From.Index+To.Index;

		Put(Free,To,From,CountMoveFrom-1);
		}
	else	{

		Moves.Length++;
		Moves[Moves.Length-1]=From.Index+To.Index;
		}

}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonSetClick(TObject *Sender)
{
	CountMoves=0;
	Col[0]->SetSize(0);
	Col[1]->SetSize(0);
	Col[2]->SetSize(0);

	for(int i=0;i!=Disk.Length;i++)	{
		Disk[i]->~TRectangle();
		}

	if(Edit1->Text!="" && Edit1->Text.ToInt()>0)	{
		if(Edit1->Text.ToInt()>15)	{
			ShowMessage("Прекаляваш!");
			Edit1->Text!="0";
			Disk.Length=0;
			return;
			}
		ButtonMove->Enabled=true;

		Disk.Length=Edit1->Text.ToInt();

		for(int i=0;i!=Disk.Length;i++)	{
			Disk[i]=new TRectangle(this);
			Disk[i]->Parent=this;
			Disk[i]->Height=20;
			Disk[i]->Width=150-i*10;
			Disk[i]->Position->X=25+i*5;
			Disk[i]->Position->Y=400-(i+1)*20;
			Disk[i]->XRadius=10;
			Disk[i]->YRadius=10;
			Col[0]->Put(Disk[i]);
			}

		Put(*Col[0],*Col[2],*Col[1],Disk.Length);
		LabelCountMoves->Text=CountMoves;
		}
	else	{
		Disk.Length=0;
		LabelCountMoves->Text=0;
		ButtonMove->Enabled=false;
		}
}
//---------------------------------------------------------------------------
void __fastcall TForm1::FormCreate(TObject *Sender)
{
	ButtonMove->Enabled=false;
	Col[0]=new Column(this,X1,Y,1,Height,Move);
	Col[1]=new Column(this,X2,Y,2,Height,Move);
	Col[2]=new Column(this,X3,Y,3,Height,Move);

	Dur=LabelSpeed->Text.ToDouble();
	LabelCountMoves->Text=0;
	LabelLeftMoves->Text=0;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonMoveClick(TObject *Sender)
{
//	Put(*Col[0],*Col[2],*Col[1],Disk.Length);

	Dur=LabelSpeed->Text.ToDouble();
	Move(NULL);
	ButtonMove->Enabled=false;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Move(TObject *Sender)
{
	LabelLeftMoves->Text=CountMoves;
	if(CountMoves>0)	{
		int Index1,Index2;
		Index1=Moves[Moves.Length-CountMoves].SubString(1,1).ToInt();
		Index2=Moves[Moves.Length-CountMoves].SubString(2,1).ToInt();

		int ToX,ToY;

		switch(Index2)	{
			case 1	: ToX=X1;	break;
			case 2	: ToX=X2;	break;
			case 3	: ToX=X3;	break;
			}

		ToY=Y-Col[Index2-1]->Disk.Length*20;

		Col[Index1-1]->Move(ToX,ToY);

		Col[Index2-1]->Put(Col[Index1-1]->GetLast());
		Col[Index1-1]->Pop();


		CountMoves--;
		}
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonSpeedUpClick(TObject *Sender)
{
	if(RoundTo(Dur-0.1,-4)>=0)	{
		LabelSpeed->Text=LabelSpeed->Text.ToDouble()+0.1;
		Dur+=0.1;
		}
	else	{
		LabelSpeed->Text=LabelSpeed->Text.ToDouble()+0.01;
		Dur+=0.01;
		}

	if(RoundTo(Dur,-2)>0.01)
		ButtonSpeedDown->Enabled=true;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonSpeedDownClick(TObject *Sender)
{
	if(!ButtonSpeedDown->Enabled)
		return;

	if(RoundTo(Dur-0.1,-4)>0)	{
		LabelSpeed->Text=LabelSpeed->Text.ToDouble()-0.1;
		Dur-=0.1;
		}
	else	{
		LabelSpeed->Text=LabelSpeed->Text.ToDouble()-0.01;
		Dur-=0.01;
		}

	if(RoundTo(Dur,-2)<0.01)
		ButtonSpeedDown->Enabled=false;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::Edit1Typing(TObject *Sender)
{
	if(
		Edit1->Text.SubString(Edit1->Text.Length(),1)<'0' ||
		Edit1->Text.SubString(Edit1->Text.Length(),1)>'9'
		)
		Edit1->Text=Edit1->Text.SubString(1,Edit1->Text.Length()-1);
}
//---------------------------------------------------------------------------
