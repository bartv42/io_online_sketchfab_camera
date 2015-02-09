# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Export Camera to Sketchfab Viewer Javascript",
    "author": "Bart Veldhuizen", #based on Export Cameras & Markers export script by Campbell Barton
    "version": (0, 1),
    "blender": (2, 7, 3),
    "api": 60995,
    "location": "File > Export > Camera Export to Sketchfab Javascript",
    "description": "TODO",
    "warning": "",
    "wiki_url": "TODO",
    "tracker_url": "TODO",
    'category': 'Import-Export'}

import bpy
import bpy_extras
import mathutils
from mathutils import *
from math import *


def writeCameras(context, filepath, frame_start, frame_end, scaling_factor):

#   For future use: data_attrs = ['lens', 'shift_x', 'shift_y', 'dof_distance', 'clip_start', 'clip_end', 'draw_size']

    c={} #the holding variable
    obj=[]

    scene = bpy.context.scene

    obj = scene.objects.active

    if obj != None:
        if obj.type != 'CAMERA':
            print("Not camera")
            return

    frame_range = range(frame_start, frame_end + 1)

#set up scene

    c["startframe"]=frame_start
    c["endframe"]=frame_end

    c["focal"]=obj.data.lens/1000 #mm to metres
    c["sensorv"]=obj.data.sensor_height/1000
    c["sensorh"]=obj.data.sensor_width/1000

    c["posx"]={}
    c["posy"]={}
    c["posz"]={}

    c["rotx"]={}
    c["roty"]={}
    c["rotz"]={}

#Frame based object settings
    for f in frame_range:
        scene.frame_set(f)

        c["posx"][f]=obj.location[0]*scaling_factor
        c["posy"][f]=obj.location[2]*scaling_factor
        c["posz"][f]=obj.location[1]*scaling_factor

        c["rotx"][f]=(obj.rotation_euler[0]*180/pi)-90
        c["roty"][f]=(obj.rotation_euler[2]*180/pi)
        c["rotz"][f]=-1*(obj.rotation_euler[1]*180/pi)

    writescript(filepath,c)
    return



def writescript(filename,c):

    startframe=c["startframe"]
    endframe=c["endframe"]
    sensorh=c["sensorh"]
    sensorv=c["sensorv"]
    focal=c["focal"]

    # Now write the script
    ixScript=open (filename,'w')

    ixScript.write('<html>\n')
    ixScript.write('<head>\n')
    ixScript.write('<script type="text/javascript" src="https://d2f25wgezub9nf.cloudfront.net/api/sketchfab-viewer-1.0.0.js"></script>\n')
    ixScript.write('</head>\n')
    ixScript.write('<body>\n')

    ixScript.write('<iframe class="developer-full-player" id="api-frame" height="640px" width="480px" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>\n')

    ixScript.write('<script>\n')

    ixScript.write("var iframe = document.getElementById( 'api-frame' );\n")
    ixScript.write("var version = '1.0.0';\n")
    ixScript.write("var urlid = '26de2fb597c04085ba70c57b61c546d6';\n")

    ixScript.write("var client = new Sketchfab( version, iframe );\n")

    ixScript.write("var error = function () {\n")
    ixScript.write("    console.error( 'Error api Sketchfab !' );\n")
    ixScript.write("}\n");

    ixScript.write("var success = function ( api ) {\n")

    ixScript.write("var target = [ 0.0, 0.0, 1.0 ];\n")
        
    ixScript.write("var cameraList = [ \n")

    for frame in range(int(startframe),int(endframe)+1):

        ixScript.write('    { eye: [ %f, ' %c["posx"][frame] )
        ixScript.write(' %f, ' %c["posz"][frame])
        ixScript.write(' %f ] ' %c["posy"][frame])

        if frame == endframe:
            ixScript.write(' }] \n')
        else:
            ixScript.write(' }, \n')    

    #ixScript.write('ix.set_current_frame(%s) \n' %startframe)

    ixScript.write("var currentCamera = 0;\n")

    ixScript.write("    var loop = function () {\n")
    ixScript.write("        currentCamera++;\n")
    ixScript.write("        api.lookat( cameraList[ currentCamera ].eye, target, 0.01 );\n")
    ixScript.write("        setTimeout( loop, 50 );\n")
    
    # animation loop
    ixScript.write("        if( currentCamera >= %d ) {\n" %endframe-1 )
    ixScript.write("            currentCamera = 0;\n")
    ixScript.write("        }\n")
    
    ixScript.write("    }\n")

    ixScript.write("    api.start( loop );\n")

    ixScript.write("};\n")

    ixScript.write("client.init( urlid, {\n")
    ixScript.write("    success: success,\n")
    ixScript.write("    error: error\n")
    ixScript.write("} );\n")

    ixScript.write('</script>\n')

    ixScript.close()

    return


#--------------------------

from bpy.props import *
from bpy_extras.io_utils import ExportHelper


class CameraExporter(bpy.types.Operator, ExportHelper):
    '''Save a python script which exports camera to Clarisse'''
    bl_idname = "export_animation.cameras"
    bl_label = "Export Camera to Sketchfab Javascript"

    filename_ext = ".html"
    filter_glob = StringProperty(default="*.html", options={'HIDDEN'})

    scaling_factor = FloatProperty(name="Scaling factor",
            description="Multiply camera position by this factor",
            default=1, min=0.0001, max=100000)


    frame_start = IntProperty(name="Start Frame",
            description="Start frame for export",
            default=0, min=0, max=300000)
    frame_end = IntProperty(name="End Frame",
            description="End frame for export",
            default=250, min=1, max=300000)


    def execute(self, context):
        writeCameras(context, self.filepath, self.frame_start, self.frame_end, self.scaling_factor)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.frame_start = context.scene.frame_start
        self.frame_end = context.scene.frame_end

        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_export(self, context):
    import os
    default_path = os.path.splitext(bpy.data.filepath)[0] + ".py"
    self.layout.operator(CameraExporter.bl_idname, text="Sketchfab Camera Animation Export (.html)").filepath = default_path


def register():
    bpy.types.INFO_MT_file_export.append(menu_export)
    bpy.utils.register_class(CameraExporter)

def unregister():
    bpy.types.INFO_MT_file_export.remove(menu_export)
    bpy.utils.unregister_class(CameraExporter)

if __name__ == "__main__":
    register()