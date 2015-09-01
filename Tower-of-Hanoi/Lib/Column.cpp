//---------------------------------------------------------------------------

#pragma hdrstop

#include "Column.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
//---------------------------------------------------------------------------

double Dur=0.3;

Column::Column(TComponent *Owner,int X,int Y,short int Index,int Height,
	void __fastcall (__closure *pOnFinish)(TObject *Sender)
	)
{
	this->Index=Index;
	this->Y=Y;
	this->pOnFinish=pOnFinish;

	Line[0]=new TLine(Owner);
	Line[0]->Parent=(TFmxObject*)Owner;
	Line[0]->LineType=TLineType::Left;
	Line[0]->RotationAngle=0;
	Line[0]->Height=Height;
	Line[0]->Width=2;
	Line[0]->Stroke->Thickness=4;
	Line[0]->Position->X=X-Line[0]->Width;
	Line[0]->Position->Y=Y-Line[0]->Height;

	Line[1]=new TLine(Owner);
	Line[1]->Parent=(TFmxObject*)Owner;
	Line[1]->LineType=TLineType::Top;
	Line[1]->RotationAngle=0;
	Line[1]->Height=4;
	Line[1]->Width=150;
	Line[1]->Stroke->Thickness=4;
	Line[1]->Position->X=X-Line[1]->Width/2;
	Line[1]->Position->Y=Y-Line[0]->Height+Line[0]->Height;
}
//---------------------------------------------------------------------------
void Column::Put(TRectangle* Rect)
{
	Disk.Length++;
	Disk[Disk.Length-1]=Rect;
}
//---------------------------------------------------------------------------
void Column::Pop()
{
	Disk.Length--;
//	Disk.pop_back();
}
//---------------------------------------------------------------------------
/*short int Column::GetIndex()
{
	return Index;
}*/
//---------------------------------------------------------------------------
TRectangle* Column::GetLast()
{
	return Disk[Disk.Length-1];
}
//---------------------------------------------------------------------------
void Column::SetSize(int size)
{
	Disk.Length=size;
}
//---------------------------------------------------------------------------
void Column::Move(int ToX,int ToY)
{
	TRectangle *R=GetLast();
	this->ToX=ToX-R->Width/2;
	this->ToY=ToY-R->Height;

	FAni=new TFloatAnimation(R);
	FAni->Parent=R;
	FAni->Duration=Dur/3;
	FAni->PropertyName="Position.Y";
	FAni->StartFromCurrent=true;
	FAni->StopValue=Y-Line[0]->Height-R->Height;
	FAni->OnFinish=OnFinish;
	FAni->Start();

	MoveState=msHor;

}
//---------------------------------------------------------------------------
void __fastcall Column::OnFinish(TObject *Sender)
{
	switch(MoveState)	{
		case msHor	:
			FAni->Stop();
			FAni->Duration=Dur/3;
			FAni->PropertyName="Position.X";
			FAni->StartFromCurrent=true;
			FAni->StopValue=ToX;
			FAni->Start();

			MoveState=msDown;
			break;
		case msDown	:
			FAni->Stop();
			FAni->Duration=Dur/3;
			FAni->PropertyName="Position.Y";
			FAni->StartFromCurrent=true;
			FAni->StopValue=ToY;
			FAni->Start();

			MoveState=msEnd;
			break;
		case msEnd	:
			FAni->Stop();

			pOnFinish(NULL);
			break;
		}
}
//---------------------------------------------------------------------------

