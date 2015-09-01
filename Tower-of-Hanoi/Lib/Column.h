//---------------------------------------------------------------------------

#ifndef ColumnH
#define ColumnH

#include <System.Classes.hpp>
#include <FMX.Objects.hpp>
#include <FMX.Ani.hpp>
//---------------------------------------------------------------------------
class Column
{
int Y,ToX,ToY;

TLine *Line[2];
TFloatAnimation *FAni;

enum TMoveState{
msHor,
msDown,
msEnd
};

TMoveState MoveState;
void __fastcall (__closure *pOnFinish)(TObject *Sender);

public:
DynamicArray<TRectangle*> Disk;
//short int  Index;
AnsiString Index;

	Column(TComponent *Owner,int X,int Y,short int Index,int Height,
		void __fastcall (__closure *pOnFinish)(TObject *Sender)
		);

	void Put(TRectangle* Rect);
	void Pop();
//	short int GetIndex();
	TRectangle* GetLast();
	void SetSize(int size);
	void Move(int ToX,int ToY);
	void __fastcall OnFinish(TObject *Sender);
};

extern double Dur;

#endif
