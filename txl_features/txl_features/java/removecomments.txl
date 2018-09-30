include "java.grm"

#pragma -raw -char -newline -comment -width 32767

redefine program
	[repeat programelement]
end define

define programelement
	[newline]
|	[comment]
|	[token]
|	[key]
|	[newline]
end define

function main
	replace [program]
		P [program]
	by
		P [fixNLComments][fixOtherComments]
end function

rule fixNLComments
	construct Newline [newline]
		_[parse ""]
	replace $ [programelement]
		Comment [comment]
	construct CEnd [number]
		_[# Comment]
	construct CIndex [number]
		CEnd
	construct Last [comment]
		Comment [: CEnd CEnd]
	where
		Last [= Newline]
	by
		Newline
end rule


rule fixOtherComments
	construct Newline [newline]
		_[parse ""]
	replace $ [comment]
		Comment [comment]
	construct CEnd [number]
		_[# Comment]
	construct CIndex [number]
		CEnd
	construct Last [comment]
		Comment [: CEnd CEnd]
	where not
		Last [= Newline]
	by
		_[+ " "]
end rule
