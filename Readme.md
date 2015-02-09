# Blender Camera exporter for Sketchfab

## Introduction

This is a proof of concept script that will publish a ready to use HTML file that contains a Sketchfab viewer and javascript code to animate the camera.

## TODO

A LOT :)

* Current state is broken. Please wait a while longer before using this.
* This code is UGLY and mixes the HTML and Javascript code with Python. I'd like to move it out to a template.
* Model ID is hardcoded.
* Player does not care about playback speed; on slow computers timing might be off. Suggested solution for this is to increase the FPS before exporting to 150 and then dropping frames during playback.
* I think the Javascript that actually plays the frames isn't exactly right either.

## How do use

* Select a camera
* Select File > Export > Sketchfab Camera Animation Export (.html)
* Edit the HTML
* Change the Model ID 