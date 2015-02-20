# Blender Camera exporter for Sketchfab

## Introduction

This is a proof of concept script that will publish a ready to use HTML file that contains a Sketchfab viewer and javascript code to animate the camera.

The script works, but that's about all - it needs a lot of love to become usable.

## TODO

A LOT :)

* This code is UGLY and mixes the HTML and Javascript code with Python. I'd like to move the HTML/Javascript out to a template and only insert the camera location.
* Model ID is hardcoded.
* Player does not care about playback speed; on slow computers timing might be off. Suggested solution for this is to increase the FPS before exporting to 150 and then dropping frames during playback.
* I think the Javascript that actually plays the frames isn't exactly right either.
* The camera target is not updated; Blender stores a camera direction while the Sketchfab API expects a camera target location.

## How do use

* Select a camera
* Select File > Export > Sketchfab Camera Animation Export (.html)
* Edit the HTML
* Change the Model ID 