//Francisco Rocha
import * as THREE from 'three'
//We import OrbitControls from three.js
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
//We import the stats.js library
import Stats from 'three/examples/jsm/libs/stats.module.js'
//We import the dat.gui library
import { GUI } from 'dat.gui'
//We import the GLTFLoader from three.js
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

var baseURL = "http://localhost:5000"
var gameLink: string | null = null; //The game link can be string or null

fetch(baseURL + "/games", {
  method: "POST"
}).then(response => {
  var location2 = response.headers.get('Location');
  if (location2 != null) {
    gameLink = location2;
  }
});

//We create a variable robotPath to store the robotPath to the assets folder
const robotPath = 'models/Roomba.glb'
const boxPath = 'models/Box.glb'
const palletPath = 'models/WoodenPallet.glb'
const zuckPath = 'models/ZuckHead.glb'
const doorPath = 'models/Door.glb'
const brickPath = 'models/Brick.glb'
const floorPath = 'img/Floor.png'
const songPath = 'sounds/Song.mp3'
const wallPath = 'img/Wall.png'


//We play a song
function playSong() {
  var audio = new Audio(songPath);
  audio.play();
}

//We create an array to store the robots generated with the GLTFLoader
const robots: THREE.Group[] = []
//We create an array to store the pallets generated with the GLTFLoader
const pallets: THREE.Group[] = []
//We create an array to store the boxes generated with the GLTFLoader
const boxes: THREE.Group[] = []
//We create an array to store the brick/Walls generated with the GLTFLoader
const bricks: THREE.Group[] = []
//Variable to store number of robots
var robotsNumber: number = 0;
var actRobot = 0;
var actY = 6;
//Variable to store the number of pallets
var palletsNumber: number = 0;
//Variable to store the number of bricks
var bricksNumber: number = 0;
//Variable to store the number of boxes
var boxesNumber: number = 0;

//Boolean for first frame
var firstFrame = true

//Boolean control of cameras
var cam1 = true
var cam2 = false
var cam3 = false

//HTML new object
const canvas = document.getElementById('frame') as HTMLCanvasElement;
const container = document.getElementById('frame-container') as HTMLDivElement;
const stats = Stats() //Stats
container.appendChild(stats.dom) //Add the stats to the body of the html

const scene = new THREE.Scene()
scene.background = new THREE.Color(0x0e1231)
//Add an axes helper to the scene
const axesHelper = new THREE.AxesHelper(1000)
//scene.add(axesHelper)

//We add models to the scene
// addModel(15,7,15,2,zuckPath) //We add the zuckHead to the scene
addModel(15, 0.1, 30, 2, doorPath) //We add the door to the scene
const camera = new THREE.PerspectiveCamera(
  100,
  parent.innerWidth / parent.innerHeight,
  0.1,
  1000
)
camera.position.x = 2;
camera.position.z = 28;
camera.position.y = 8;

const renderer = new THREE.WebGLRenderer({ canvas: canvas })
renderer.physicallyCorrectLights = true
renderer.setSize(container.offsetWidth, container.offsetHeight)
//htmlFrame.appendChild(renderer.domElement) //Add the renderer to the body of the html

//We add a directional light to the scene
addLight(15, 10, 15) //This is the light bulb

const controls = new OrbitControls(camera, renderer.domElement) //OrbitControls
//controls.addEventListener('change', render) // use if there is no animation loop. The first parameter is the event type, the second is the callback function.

//console.dir(scene)

// Control de cámaras
window.addEventListener('keydown',doKeyDown,true);
function doKeyDown(evt: { keyCode: any }) {
  switch (evt.keyCode) {
    case 49: //cámara 1
      //Se activa cámara 1
      cam1 = true
      cam2 = false
      cam3 = false
    break;
    case 50: //cámara 2
      //Se activa cámara 2
      cam1 = false
      cam2 = true
      cam3 = false
    break;
    case 51: //cámara 3
      //Se activa cámara 3
      cam1 = false
      cam2 = false
      cam3 = true
    break;
    //Cámara 3: robot anterior
    case 37:
      if(actRobot == 0){
        actRobot = robotsNumber - 1;
      }
      else{
        actRobot--;
      }
    break;
    //Cámara 3: robot anterior
    case 39:
      if(actRobot == robotsNumber - 1){
        actRobot = 0;
      }
      else{
        actRobot++;
      }
    break;
    //Cámara 3: bajamos y
    case 38:
      actY--;
    break;
    //Cámara 3: subimos y
    case 40:
      actY++;
    break;
    //Easter egg
    case 82:
      playSong();
    break;
  }
}

window.addEventListener('resize', onWindowResize, false)
function onWindowResize() {
  camera.aspect = container.offsetWidth / container.offsetHeight
  camera.updateProjectionMatrix()
  renderer.setSize(container.offsetWidth, container.offsetHeight)
  render()
}
const frame_rate = 100; // Refresh screen every 200 ms
var previous_time = Date.now();

var render = async function () {

  var now, elapsed_time;

  now = Date.now();
  elapsed_time = now - previous_time;

  //console.log("elapsed time", elapsed_time);

  if (elapsed_time >= frame_rate) {

    if (gameLink != null) { // if the game has been created
      var res = await fetch(baseURL + gameLink); // get the game state
      var data = await res.json(); // parse JSON to JS object that contains the positions of the 10 robots in every step

      if (firstFrame == true) {
        camera.lookAt(30, -5, 10)
        //From data we get how many robots are in the game
        robotsNumber = await data[0].length;
        //We instantiate the robots
        for (var i = 0; i < robotsNumber; i++) {
          //We use the importGLFT function to add the robot to the scene
          await importGLTFModel(i + 0.5, 0, i + 0.5, 0.030, robotPath, robots)
        }
        //From data we get how many pallets are in the game
        palletsNumber = await data[3].length;
        //We instantiate the pallets
        for (var i = 0; i < palletsNumber; i++) {
          //We use the importGLFT function to add the pallet to the scene
          await importGLTFModel(0.5, 0, 0.5, 0.125, palletPath, pallets)
        }
        //From data we get how many bricks are in the game
        bricksNumber = await data[1].length;
        //We instantiate the bricks
        for (var i = 0; i < bricksNumber; i++) {
          //We use the importGLFT function to add the bricks to the scene
          await importGLTFModel(data[1][i].x + 0.5, 0.5, data[1][i].y + 0.5, 0.48, brickPath, bricks)
          await addModel(data[1][i].x + 0.5, 1.5, data[1][i].y + 0.5, 0.48, brickPath)
        }
        //From data we get how many boxes are in the game
        boxesNumber = await data[2].length;
        //We instantiate the boxes
        for (var i = 0; i < boxesNumber; i++) {
          //We use the importGLFT function to add the boxes to the scene
          await importGLTFModel(data[2][i].x + 0.5, 0, data[2][i].y + 0.5, 3.2, boxPath, boxes)
        }
      }

      firstFrame = false;

      //console.log(robots)
      //console.log(pallets)
      //console.log(bricks)

      //If the robots array position is not undefined we update the position of the robots
      if (robots[0] != undefined && pallets[0] != undefined && boxes[0] != undefined && data[4][0].run == true) {
        for (var i = 0; i < robotsNumber; i++) {
          robots[i].position.x = await data[0][i].x + 0.5;
          robots[i].position.z = await data[0][i].y + 0.5;
          robots[i].position.y = 0.05;
        }
        for (var i = 0; i < palletsNumber; i++) {
          pallets[i].position.x = await data[3][i].x + 0.5;
          pallets[i].position.z = await data[3][i].y + 0.5;
          pallets[i].position.y = 0;
        }
        for (var i = 0; i < boxesNumber; i++) {
          //If the box is being carried by a robot we update the position of the box
          if (data[2][i].status == true) {
            boxes[i].position.x = await data[2][i].x + 0.5;
            boxes[i].position.z = await data[2][i].y + 0.5;
            boxes[i].position.y = 0.25;
          }
          if (data[2][i].stack != 0){ //It means that the box is stacked
            boxes[i].position.x = await data[2][i].x + 0.5;
            boxes[i].position.z = await data[2][i].y + 0.5;
            boxes[i].position.y = 0.15+((data[2][i].stack - 1)*0.75);
          }
        }
        // boxes[i].position.x = await data[2][i].x + 0.5;
        // boxes[i].position.z = await data[2][i].y + 0.5;
        // boxes[i].position.y = 0;
      }
      // console.log(robots)
      //await console.log(robots[0])
    }
    previous_time = now;
  }
  stats.update() //We update the stats
  requestAnimationFrame(render);
  renderer.render(scene, camera);
  if(cam1 == true){
    //nada, jeje
  }
  else if(cam2 == true){
    //Camara cenital
    camera.position.x = 15;
    camera.position.z = 15;
    camera.position.y = 13;
    //camera.lookAt(0, -150, 0)
    //camera.rotateX(-Math.PI/2);
  }
  else if(cam3 == true){
    //We set the camera to follow the robot
    camera.position.x = robots[actRobot].position.x;
    camera.position.z = robots[actRobot].position.z;
    camera.position.y = actY;
    camera.rotateX(-Math.PI/2);
    camera.lookAt(robots[actRobot].position.x, robots[actRobot].position.y, robots[actRobot].position.z)
  }
};

// Functions that are useful

//Function to import GLTF model and save it in an array
async function importGLTFModel(x: number, y: number, z: number, scale: number, modelPath: string, array: THREE.Group[]) {
  const loader = new GLTFLoader()
  loader.load(modelPath, async (gltf) => { //We load the model
    //We get the model from the gltf object
    const model = gltf.scene
    //We scale the model
    model.scale.set(scale, scale, scale)
    //We set the model position
    model.position.set(x, y, z)
    //We add the model to the array
    array.push(model)
    gltf.scene.traverse(function (child) { //We traverse the model
      if ((child as THREE.Mesh).isMesh) { //If the child is a mesh we set the shadow properties
        const m = child as THREE.Mesh //We cast the child to a mesh
        m.receiveShadow = true //We set the receiveShadow property to true
        m.castShadow = true //We set the castShadow property to true
      }
      if ((child as THREE.Light).isLight) { //If the child is a light we set the shadow properties
        const l = child as THREE.Light //We cast the child to a light
        l.castShadow = true //We set the castShadow property to true
        l.shadow.bias = -0.003 //We set the bias property to -0.003
        l.shadow.mapSize.width = 2048 //We set the width of the shadow map to 2048
        l.shadow.mapSize.height = 2048 //We set the height of the shadow map to 2048
      }
    })
    //We add the model to the scene
    scene.add(model)
  })
}

async function addModel(x: number, y: number, z: number, scale: number, path: string) {
  //We create a new GLTFLoader
  const loader = new GLTFLoader()
  //We load the model
  loader.load(
    //We pass the path to the model
    path,
    //We pass the function that will be executed after the model is loaded
    async function (gltf) {
      //We get the model from the gltf object
      const model = gltf.scene
      //We set the model position
      model.position.set(x, y, z)
      //We set the model scale
      model.scale.set(scale, scale, scale)
      gltf.scene.traverse(function (child) {
        if ((child as THREE.Mesh).isMesh) {
          const m = child as THREE.Mesh
          m.receiveShadow = true
          m.castShadow = true
        }
        if ((child as THREE.Light).isLight) {
          const l = child as THREE.Light
          l.castShadow = true
          l.shadow.bias = -0.003
          l.shadow.mapSize.width = 2048
          l.shadow.mapSize.height = 2048
        }
      })
      //We add the model to the scene
      scene.add(model)
    },
    //We pass the function that will be executed while the model is loading
    //function (xhr) {
    //console.log((xhr.loaded / xhr.total * 100) + '% loaded')
    //},
    //We pass the function that will be executed if there is an error loading the model
    //function (error) {
    //console.log('An error happened')
    //}
  )
}

//We create a function to add a light to the scene
function addLight(x: number, y: number, z: number) {
  //We create a new directional light
  const light = new THREE.DirectionalLight(0xffffff, 10)
  //We set the light position
  light.position.set(x, y, z)
  //We add the light to the scene
  scene.add(light)
}

//We create a function to add a point light over each robot
function addPointLight(x: number, y: number, z: number) {
  var pointLight = new THREE.PointLight(0xff0000, 1, 100)
  pointLight.position.set(x, y, z)
  scene.add(pointLight)
}

//We create a function to add a wall with texture to the scene
function addWall(x: number, y: number, z: number, width: number, height: number) {
  const wallGeometry = new THREE.PlaneGeometry(width, height)
  const loader = new THREE.TextureLoader();
  const wallMaterial = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    side: THREE.DoubleSide,
  })
  //We set the texture of the wall from a file
  const wallTexture = new THREE.TextureLoader().load(
    wallPath
  )
  //wallTexture.wrapS = THREE.RepeatWrapping
  //wallTexture.wrapT = THREE.RepeatWrapping
  wallTexture.magFilter = THREE.NearestFilter
  wallTexture.repeat.set(1, 1)
  wallMaterial.map = wallTexture
  const wall = new THREE.Mesh(wallGeometry, wallMaterial)
  wall.position.x = x
  wall.position.y = y
  wall.position.z = z
  //We translate the wall to the right by half its width - 0.5
  wall.translateX(width / 2 - 0.5)
  //We translate the wall up by half its height - 0.5
  wall.translateY(height / 2 - 0.5)
  scene.add(wall)
  return wall
}

//Function to set the walls
function setWalls() {
  // //We create a grid plane
  // const gridHelper = new THREE.GridHelper(60, 60)
  // scene.add(gridHelper)
  //We create the floor
  const floorGeometry = new THREE.PlaneGeometry(30, 30, 30, 30)
  const floorMaterial = new THREE.MeshBasicMaterial({
    //We set the color of the floor to white
    color: 0xffffff,
    side: THREE.DoubleSide,
  })
  //We add a texture to the floor
  const floorTexture = new THREE.TextureLoader().load(
    floorPath
  )
  floorTexture.wrapS = THREE.RepeatWrapping
  floorTexture.wrapT = THREE.RepeatWrapping
  floorTexture.magFilter = THREE.NearestFilter
  floorTexture.repeat.set(4, 4)
  floorMaterial.map = floorTexture
  const floor = new THREE.Mesh(floorGeometry, floorMaterial)
  floor.rotation.x = Math.PI / 2
  // //We move the floor 30 units to the right
  floor.position.x = 15
  // //We move the floor 30 units to the front
  floor.position.z = 15
  scene.add(floor)
  //Lateral walls
  addWall(0.5, 0.5, 0, 30, 10)
  addWall(0.5, 0.5, 30, 30, 10)
  //Frontal walls
  const wall1 = addWall(15.5, 0.5, 15, 30, 10)
  wall1.rotation.y = Math.PI / 2
  const wall2 = addWall(-14.5, 0.5, 15, 30, 10)
  wall2.rotation.y = Math.PI / 2
}

//Function to add a skybox to the scene taking as parameters the path to the skybox images
function addSkyBox(path: string) {
  const loader = new THREE.CubeTextureLoader()
  const texture = loader.load([
    path + 'px.jpg', //Right
    path + 'nx.jpg', //Left
    path + 'py.jpg', //Top
    path + 'ny.jpg', //Bottom
    path + 'pz.jpg', //Front
    path + 'nz.jpg', //Back
  ])
  scene.background = texture
}

// GUI
const gui = new GUI() //Dat.gui
const cameraFolder = gui.addFolder('Camera') //Add a cameraFolder to the dat.gui
cameraFolder.add(camera.position, 'x', -5, 5, 0.01) //Add the x position to the dat.gui
cameraFolder.add(camera.position, 'y', -5, 5, 0.01) //Add the y position to the dat.gui
cameraFolder.add(camera.position, 'z', -5, 100, 0.01) //Add the z position to the dat.gui
cameraFolder.add(camera.rotation, 'x', 0, 2 * Math.PI, 0.01) //Add the x rotation to the dat.gui
cameraFolder.add(camera.rotation, 'y', 0, 2 * Math.PI, 0.01) //Add the y rotation to the dat.gui
cameraFolder.add(camera.rotation, 'z', 0, 2 * Math.PI, 0.01) //Add the z rotation to the dat.gui
cameraFolder.add(camera, 'fov', 0, 180, 0.01) //Add the fov to the dat.gui
cameraFolder.add(camera, 'near', 0, 5, 0.01) //Add the near to the dat.gui
cameraFolder.add(camera, 'far', 0, 5, 0.01) //Add the far to the dat.gui
cameraFolder.add(camera, 'zoom', 0, 5, 0.01) //Add the zoom to the dat.gui
cameraFolder.add(camera, 'focus', 0, 5, 0.01) //Add the focus to the dat.gui
cameraFolder.add(camera, 'aspect', 0, 5, 0.01) //Add the aspect to the dat.gui

setWalls();
render();