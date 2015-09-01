//---------------------------------------------------------------------------

#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <FMX.Controls.hpp>
#include <FMX.Forms.hpp>

#include "Column.h"
#include <FMX.StdCtrls.hpp>
#include <FMX.Types.hpp>
#include <FMX.Objects.hpp>
#include <FMX.Controls.Presentation.hpp>
#include <FMX.Edit.hpp>
#include <FMX.Ani.hpp>
//---------------------------------------------------------------------------
class TForm1 : public TForm
{
__published:	// IDE-managed Components
	TButton *ButtonSet;
	TEdit *Edit1;
	TButton *ButtonMove;
	TSpeedButton *ButtonSpeedUp;
	TLabel *LabelSpeed;
	TSpeedButton *ButtonSpeedDown;
	TLabel *Label1;
	TLabel *Label2;
	TRectAnimation *RectAnimation1;
	TLabel *Label3;
	TLabel *LabelCountMoves;
	TLabel *Label4;
	TLabel *LabelLeftMoves;
	void __fastcall ButtonSetClick(TObject *Sender);
	void __fastcall FormCreate(TObject *Sender);
	void __fastcall ButtonMoveClick(TObject *Sender);
	void __fastcall ButtonSpeedUpClick(TObject *Sender);
	void __fastcall ButtonSpeedDownClick(TObject *Sender);
	void __fastcall Edit1Typing(TObject *Sender);
private:	// User declarations

int CountMoves,Height,CountDisks;
Column *Col[3];
DynamicArray<TRectangle*> Disk;
DynamicArray<AnsiString> Moves;

	inline void Put(Column &From,Column &To,Column &Free,int CountMoveFrom);
	void __fastcall Move(TObject *Sender);


public:		// User declarations
	__fastcall TForm1(TComponent* Owner);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif
