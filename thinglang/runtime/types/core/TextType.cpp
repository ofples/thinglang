/**
    TextType.cpp
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/


#include "../InternalTypes.h"

/**
Methods of TextType
**/


void TextType::__constructor__() {
    Program::push(Program::create<TextInstance>());
}


void TextType::__addition__() {
		auto other = Program::argument<TextInstance>();
		auto self = Program::argument<TextInstance>();

		Program::push(Program::create<TextInstance>(self->val + other->val));
        
    }


void TextType::__equals__() {
		auto other = Program::argument<TextInstance>();
		auto self = Program::argument<TextInstance>();

		
        if(self->val == other->val) {
			Program::push(BOOL_TRUE);
        }

		
        else {
			Program::push(BOOL_FALSE);
    }

        
    }


void TextType::contains() {
		auto substring = Program::argument<TextInstance>();
		auto self = Program::argument<TextInstance>();

		auto found = self->val.find(substring->val) != std::string::npos;
		
        if(found) {
			Program::push(BOOL_TRUE);
        }

		
        else {
			Program::push(BOOL_FALSE);
    }

        
    }


void TextType::length() {
		auto self = Program::argument<TextInstance>();

		Program::push(Program::create<NumberInstance>(self->val.size()));
        
    }


void TextType::to_bytes() {
		auto self = Program::argument<TextInstance>();

		auto byte_array = Program::create<ListInstance>();
		byte_array->val.resize(self->val.size());
		for(auto i = 0; i < self->val.size(); i++) byte_array->val[i] = Program::create<NumberInstance>(self->val[i]);
		Program::push(byte_array);
        
    }


void TextType::convert_number() {
		auto num = Program::argument<TextInstance>();

		Program::push(Program::create<NumberInstance>(to_number(num->val)));
        
    }


/**
Mixins of TextInstance
**/

std::string TextInstance::text() {
    return to_string(val);
}

bool TextInstance::boolean() {
    return to_boolean(val);
}

