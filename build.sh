#!/usr/bin/env sh

PATH=~/src/panda3d/built_tmp_rt/bin:$PATH

if [ -d "build" ]; then
    rm -rf "build";
fi

panda3d ~/src/panda3d/built_tmp/stage/ppackage1.10.p3d -i build hydrogen.pdef
panda3d ~/src/panda3d/built_tmp/stage/pdeploy1.10.p3d -o build -s -v 0.0.0 build/hydrogen.p3d installer
