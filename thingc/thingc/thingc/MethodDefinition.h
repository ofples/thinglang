#pragma once

#include <vector>

#include "Symbol.h"

class MethodDefinition {
public:
	MethodDefinition() : frame_size(0), arguments(0) {};
	MethodDefinition(unsigned int frame_size, unsigned int arguments, std::vector<Symbol> symbols) : frame_size(frame_size), arguments(arguments), symbols(symbols) {};

	void execute();
	const unsigned int frame_size;
	const unsigned int arguments;

private:
	std::vector<Symbol> symbols;

};
