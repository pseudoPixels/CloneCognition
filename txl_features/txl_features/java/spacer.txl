include "java_alt.grm"

#pragma -newline -raw -width 32767

redefine program
	[repeat programline]
	[repeat programelement] [NL] %in case no last endline
end define

define programline
	[repeat programelement] [newline]
end define

define programelement
	[not newline] [SP] [token] [SP]
|	[not newline] [SP] [key] [SP]
end define

function main
	replace [program]
		P [program]
	by
		P
end function
