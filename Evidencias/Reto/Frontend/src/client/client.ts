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

//Here we create all the paths to the assets
const floorPath = 'img/Floor.png'
const songPath = 'sounds/Song.mp3'


//We create an array to store the cars generated with the GLTFLoader
const cars: THREE.Group[] = []; //The array can be empty
//We create a variable that will save a car model
const car: THREE.Group | null = null; //The car starts being a null
//We create a variable to keep track of how many cars are in the actual frame
var carsNumber: number = 0;
//We create a variable to know which car the camera is focusing
var actCar: number = 0;
//We create a variable to keep track of 'Y' positions when we use the sky camera
var actY: number = 6;
//We create a global array to keep track of the cars IDs, last frame
var globalCarsIds: number[] = [];
//We create a global array to keep track of the cars IDs in every frame
var actCarsIds: number[] = [];
//We create a global boolean to know if the cars are the same as the last frame
var changedCars: boolean = false;

modelToVariable(0, 0, 0, 1, 'models/Car.glb', car!) //We load the car model

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
scene.add(axesHelper)

//We add models to the scene
//Here we can add the static models of the scene, like buildings and stuff.


const camera = new THREE.PerspectiveCamera(
  100,
  parent.innerWidth / parent.innerHeight,
  0.1,
  1000
)

//These are the camera first positions
camera.position.x = 2;
camera.position.z = 28;
camera.position.y = 8;

const renderer = new THREE.WebGLRenderer({ canvas: canvas })
renderer.physicallyCorrectLights = true
renderer.setSize(container.offsetWidth, container.offsetHeight)
//htmlFrame.appendChild(renderer.domElement) //Add the renderer to the body of the html

//We add a directional light to the scene
addLight(15, 10, 15) //This is the sun

const controls = new OrbitControls(camera, renderer.domElement) //OrbitControls
//controls.addEventListener('change', render) // use if there is no animation loop. The first parameter is the event type, the second is the callback function.

//console.dir(scene)

// Control de cámaras
window.addEventListener('keydown', doKeyDown, true);
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
    //Cámara 3: carro anterior
    case 37:
      if (actCar == 0) {
        actCar = carsNumber - 1;
      }
      else {
        actCar--;
      }
      break;
    //Cámara 3: carro anterior
    case 39:
      if (actCar == carsNumber - 1) {
        actCar = 0;
      }
      else {
        actCar++;
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
      //playSong(); //Here we can play a song
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
const frame_rate = 250; // Refresh screen every 200 ms
var previous_time = Date.now();
var last_check = true;

var render = async function () {

  var now, elapsed_time;

  now = Date.now();
  elapsed_time = now - previous_time;

  //console.log("elapsed time", elapsed_time);

  if (elapsed_time >= frame_rate) {

    if (gameLink != null) { // if the game has been created
      var res = await fetch(baseURL + gameLink); // get the game state
      var data = await res.json(); // parse JSON to JS object that contains the positions of the cars

      //console.log(data[0][0].id);

      //If the cars array position is not undefined we update the position of the car
      if (data[0] != undefined && data[2][0].run == true) {
        if (firstFrame == true) {
          camera.lookAt(30, -5, 10) //This is the first position the camera will look at
          //We set the array with the cars IDs
          for (var i = 0; i < data[0].length; i++) {
            globalCarsIds.push(data[0][i].id);
          }
          firstFrame = false;
        }
        //Here we update the cars position every frame
        //We set the array with the cars IDs
        actCarsIds = [];
        for (var i = 0; i < data[0].length; i++) {
          actCarsIds.push(data[0][i].id);
        }
        //We compare globalCarsIds with actCarsIds
        changedCars = !compareArrays(globalCarsIds, actCarsIds); //If the cars are the same, changedCars is false
        //We empty the cars ids array to update it
        globalCarsIds = [];
        for (var i = 0; i < data[0].length; i++) {
          cars[i].position.x = data[0][i].position[0];
          cars[i].position.y = data[0][i].position[1];
          cars[i].position.z = data[0][i].position[2];
          cars[i].rotation.x = data[0][i].rotation[0];
          cars[i].rotation.y = data[0][i].rotation[1];
          cars[i].rotation.z = data[0][i].rotation[2];
          globalCarsIds.push(data[0][i].id);
        }
      }
      else if (data[2][0].run == false && last_check == true) {
        //Here we can execute the last frame of the simulation
        last_check = false;
      }
      // console.log(cars)
      //await console.log(cars[0])
    }
    previous_time = now;
  }
  stats.update() //We update the stats
  requestAnimationFrame(render);
  renderer.render(scene, camera);
  if (cam1 == true) {
    //nada, jeje
  }
  else if (cam2 == true) {
    //Camara cenital
    camera.position.x = 15;
    camera.position.z = 15;
    camera.position.y = 13;
    //camera.lookAt(0, -150, 0)
    //camera.rotateX(-Math.PI/2);
  }
  else if (cam3 == true) {
    //We set the camera to follow the car
    camera.position.x = cars[actCar].position.x;
    camera.position.z = cars[actCar].position.z;
    camera.position.y = actY;
    camera.rotateX(-Math.PI / 2);
    camera.lookAt(cars[actCar].position.x, cars[actCar].position.y, cars[actCar].position.z)
  }
};

// Functions that are useful

//Function to import GLTF model and save it in an array
async function modelToArray(x: number, y: number, z: number, scale: number, modelPath: string, array: THREE.Group[]) {
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

//Function to import GLTF model and assign it to a variable
async function modelToVariable(x: number, y: number, z: number, scale: number, modelPath: string, variable: THREE.Group) {
  const loader = new GLTFLoader()
  loader.load(modelPath, async (gltf) => { //We load the model
    //We get the model from the gltf object
    const model = gltf.scene
    //We scale the model
    model.scale.set(scale, scale, scale)
    //We set the model position
    model.position.set(x, y, z)
    //We add the model to the variable
    variable = model
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

//Function to set the floor
function setFloor() {
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
}

//We play a song
function playSong() {
  var audio = new Audio(songPath);
  audio.play();
}

//Function to compare two arrays, if it is the same it returns true, if not it returns false
function compareArrays(array1: any[], array2: any[]) {
  //We check if the arrays have the same length
  if (array1.length !== array2.length) {
    return false
  }
  //We loop through the arrays
  for (let i = 0; i < array1.length; i++) {
    //We check if the elements are the same
    if (array1[i] !== array2[i]) {
      return false
    }
  }
  return true
}


// GUI
const gui = new GUI() //Dat.gui
const cameraFolder = gui.addFolder('Camera') //Add a cameraFolder to the dat.gui
cameraFolder.add(camera.position, 'x', -100, 100, 0.01) //Add the x position to the dat.gui
cameraFolder.add(camera.position, 'y', -100, 100, 0.01) //Add the y position to the dat.gui
cameraFolder.add(camera.position, 'z', -100, 100, 0.01) //Add the z position to the dat.gui
cameraFolder.add(camera.rotation, 'x', 0, 2 * Math.PI, 0.01) //Add the x rotation to the dat.gui
cameraFolder.add(camera.rotation, 'y', 0, 2 * Math.PI, 0.01) //Add the y rotation to the dat.gui
cameraFolder.add(camera.rotation, 'z', 0, 2 * Math.PI, 0.01) //Add the z rotation to the dat.gui

//setFloor();
render();