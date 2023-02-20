#include "widgets/Button.h"
#include <utility>
#include <iostream>

TDT4102::Button::Button(TDT4102::Point location, unsigned int width, unsigned int height, std::string label) :
    TDT4102::Widget(location, width, height),
    label{std::move(label)} {}

void TDT4102::Button::update(nk_context *context) {
    if (nk_button_label(context, label.c_str())) {
        fire();
    }
}

