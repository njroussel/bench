#!/usr/bin/env bash

# Setup repository
git submodule update --init --recursive

# Build mitsuba
cd ext/mitsuba3
mkdir build
cd build
cmake -GNinja ..
ninja
cd ../../../

# Build luisa
cd ext/LuisaRender
mkdir build
cd build
cmake -GNinja -D CMAKE_BUILD_TYPE=Release ..
ninja
cd ../../../
