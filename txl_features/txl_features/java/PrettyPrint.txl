% Parser for Java programs
% Jim Cordy, January 2008

% Using Java 5 grammar
include "java.grm"
include "bom.grm"

#pragma -width 32726

function main
    match [program]
	P [program]
end function
