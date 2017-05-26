#include <iostream>

#include "Symbol.h"
#include "Program.h"


void Symbol::execute() {
	std::cerr << "Executing symbol " << describe(this->opcode) << ": " << this->target << ", " << this->secondary << std::endl;
	switch (this->opcode) {

	case Opcode::NOP:
		break;

	case Opcode::PUSH: {
        Program::push(Program::frame()[this->target]);
        break;
    };

    case Opcode::SET_STATIC: {
        Program::frame()[this->target] = Program::data(secondary);
    }

	case Opcode::PUSH_STATIC: {
		Program::push(Program::data(target));
		break;
	};

	case Opcode::CALL_METHOD: {
		auto instance = Program::instance();
		auto method = instance->method(target);


		method.execute();
		break;
	}

	case Opcode::PRINT:
		std::cout << Program::pop()->text() << std::endl;
		break;

	case Opcode::CALL_INTERNAL: {
		Program::internals[this->target]->call_internal(this->secondary);
		break;
	}

	case Opcode::RETURN: {
		Program::pop_frame();
		break;
	}

	default: 
		throw RuntimeError("Cannot handle symbol " + std::to_string((int) this->opcode));
		break;

	}
}