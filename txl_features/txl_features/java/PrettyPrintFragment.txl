include "JavaFragmentGrammar.txl"

#pragma -width 32767

% Main function
	% Pretty print the given java fragment
function main
	replace [program]
		P [program]
	by
		P
end function
