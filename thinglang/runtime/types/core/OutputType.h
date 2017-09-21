/**
    OutputType.h
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

#pragma once

#include "../../utils/TypeNames.h"
#include "../../execution/Globals.h"
#include "../../utils/Formatting.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"
#include "../../execution/Program.h"

namespace OutputNamespace {


class OutputInstance : public BaseThingInstance {
    
    public:
    explicit OutputInstance() = default; // empty constructor
    
    
    
    /** Mixins **/
    
    
    
    /** Members **/
    
    
};


typedef OutputInstance this_type;

class OutputType : public ThingTypeInternal {
    
    public:
    OutputType() : ThingTypeInternal({ &__constructor__, &write }) {}; // constructor
 
    
    static Thing __constructor__() {
        return Thing(new this_type());
    }


    static Thing write() {
		auto message = Program::pop();

		std::cout << message->text() << std::endl;
		return nullptr;
    }

    
};

}