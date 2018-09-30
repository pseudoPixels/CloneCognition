include "CFragmentGrammar.txl"

#pragma -width 32726

% Main function
	% Pretty print the given java fragment
function main
	replace [program]
		P [program]
	by
		P
end function
