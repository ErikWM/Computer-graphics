# eindopdracht
# You can use W A S D to controll the cube
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image
import random
SPEED = 0.02
#square x,z,y
mx, my, mz = 0, 0, 0
#sphere x,y,z
sx, sy, sz = 3, 0, 2
#snelheid x,y,z
vx, vz,= 0.03, 0.02

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    drawPlane()
    glPushMatrix()
    botsing()
    glTranslate(sx,sy,sz)
    gluSphere(sphere, 0.5, 100, 100) # straal, aantal partjes, aantal schijven
    glPopMatrix()
    glPushMatrix()
    glTranslatef(mx, my, mz)
    glutSolidCube(1)
    glPopMatrix()
    glutSwapBuffers()
# Deze functie zorgt ervoor dat de sphere van richting verandert wanneer die met ede cube of wal botst
def botsing():
    global sx, sy, sz, vx, vz, mx, my, mz
    # check if sphere is within collision distance of cube
    if abs(sx - mx) <= 0.5 and abs(sz - mz) <= 0.5:
        # change velocity in opposite direction
        vx = -vx
        vz = -vz
    # check if sphere is out of bounds
    if sx < -5 or sx > 5:
        vx = -vx * random.uniform(0.8, 1.2)
    if sz < -5 or sz > 5:
        vz = -vz * random.uniform(0.8, 1.2)
    sx += vx
    sz += vz
    print(vx, "-", vz)
# Deze functie maakt een wal die ervoor zorgt dat de cube en sphere niet weg van het platform gaan
def drawPlane():
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-5.5, -0.5, -5.5)
    glTexCoord2f(1, 0); glVertex3f(5.5, -0.5, -5.5)
    glTexCoord2f(1, 1); glVertex3f(5.5, -0.5, 5.5)
    glTexCoord2f(0, 1); glVertex3f(-5.5, -0.5, 5.5)
    glEnd()

def end(key, x, y):
    os._exit(0)
# Here is my keyboard input code
def buttons(key,x,y):
    global mx, my, mz
    if key == b'a' and mx > -5:
        mx -= 1
    if key == b'd' and mx < 5:
        mx += 1
    if key == b'w' and mz > -5:
        mz -= 1
    if key == b's' and mz < 5:
        mz += 1
    #print (mx, " ",my , " ", mz)
	
glutInit()
glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(640, 480)
glutCreateWindow("Perspective view".encode("ascii"))
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_BLEND)
glEnable(GL_LINE_SMOOTH)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
glFrustum(-1.333, 1.333, -1, 1, 5, 20)
glMatrixMode(GL_MODELVIEW)
gluLookAt(9, 10, 11, 0, 0, 0, 0, 1, 0)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLight(GL_LIGHT0, GL_POSITION, [-3, 4, 5])
glLight(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5])
glLight(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5])
glLight(GL_LIGHT0, GL_SPECULAR, [1, 1, 1])
glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 1, 0, 1])
glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 50)
SIZE = 64 # grootte in texels
img = Image.open("bb.jpg") # laad plaatje
glPixelStorei(GL_UNPACK_ALIGNMENT, 1) # voor plaatjes met oneven aantal pixels
texture = glGenTextures(1) # maak een ID voor 1 textuur
glBindTexture(GL_TEXTURE_2D, texture) # gebruik de ID
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) # specificeer hoe de textuur geschaald moet worden
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img.tobytes()) # laad het plaatje
sphere = gluNewQuadric() # maak een nieuw quadrics-object
gluQuadricTexture(sphere, GLU_TRUE) # zet het genereren van texture-coördinaten aan
glEnable(GL_TEXTURE_2D) # zet textuur aan
glutDisplayFunc(display)
glutKeyboardFunc(buttons)
glutIdleFunc(glutPostRedisplay)
glutMainLoop()
