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
var cars: THREE.Group[] = []; //The array can be empty
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

//We load the model
loadModel('models/Car.glb', 0.0025, 0, 0, 0, cars).then((array) => {
  carsNumber = 10;
  // //We create a loop to add the cars to the scene
  // for (let i = 0; i < carsNumber; i++) {
  //   scene.add(cars[i]);
  // }
  console.log(cars)
});
// car.then((car) => {
//   //We add the car to the array
//   cars.push(car)
//   //We add the car to the scene
//   scene.add(car)
//   //We add the car to the global array
//   globalCarsIds.push(0)
//   //We add the car to the actual array
//   actCarsIds.push(0)
//   //We add the car to the scene
//   //scene.add(car)
//   //We add the car to the global array
//   globalCarsIds.push(0)
//   //We add the car to the actual array
//   actCarsIds.push(0)
//   //We add the car to the scene
// })
// //If not we catch the error
// .catch((error) => {
//   console.log(error)
// })



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
const axesHelper = new THREE.AxesHelper(1)
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
camera.position.x = 0;
camera.position.z = 5;
camera.position.y = 2;

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
      if (firstFrame == true) {
        //camera.lookAt(30, -5, 10) //This is the first position the camera will look at
        //We set the array with the cars IDs
        for (var i = 0; i < await data[0].length; i++) {//We fill the array with the cars IDs
          globalCarsIds.push(await data[0][i].id);
          console.log("Cars array created");
        }
        //We create the array of cars
        // console.log(cars);
        // We position the cars
        // for (var i = 0; i < data[0].length; i++) {
        //   //We update the position of the car
        //   cars[i].position.x = await data[0][i].x;
        //   cars[i].position.z = await data[0][i].y;
        //   cars[i].position.y = 0;
        //   // //We update the rotation of the car
        //   // cars[i].rotation.x = data[0][i].rx;
        //   // cars[i].rotation.z = data[0][i].rz;
        //   // cars[i].rotation.y = data[0][i].ry;
        // }
        firstFrame = false;
      }
      // console.log(cars)
      //If the cars array position is not undefined we update the position of the car
      // if (data[0] != undefined && data[2][0].run == true && cars[0] != undefined) {
      //   console.log("Here");
      //   //Here we update the cars position every frame
      //   //We set the array with the cars IDs
      //   actCarsIds = [];
      //   for (var i = 0; i < await data[0].length; i++) {
      //     actCarsIds.push(await data[0][i].id);
      //   }
      //   //We compare globalCarsIds with actCarsIds
      //   changedCars = !compareArrays(globalCarsIds, actCarsIds); //If the cars are the same, changedCars is false

      //   //If the cars are the same, we update the position of the cars
      //   if (changedCars == false) {
      //     // for (var i = 0; i < await data[0].length; i++) {
      //     //   //We update the position of the car
      //     //   cars[i].position.x = await data[0][i].x;
      //     //   cars[i].position.z = await data[0][i].y;
      //     //   cars[i].position.y = 0;
      //     //   // //We update the rotation of the car
      //     //   // cars[i].rotation.x = data[0][i].rx;
      //     //   // cars[i].rotation.z = data[0][i].rz;
      //     //   // cars[i].rotation.y = data[0][i].ry;
      //     // }
      //   }
      //   //If the cars are not the same, we update the cars array
      //   else {
      //     await modelToArray(0,0,0,1,'models/Car.glb',cars)
      //     //We update the position of the cars
      //     // for (var i = 0; i < await data[0].length; i++) {
      //     //   //We update the position of the car
      //     //   cars[i].position.x = await data[0][i].x;
      //     //   cars[i].position.z = await data[0][i].Y;
      //     //   cars[i].position.y = 0;
      //     //   // //We update the rotation of the car
      //     //   // cars[i].rotation.x = data[0][i].rx;
      //     //   // cars[i].rotation.z = data[0][i].rz;
      //     //   // cars[i].rotation.y = data[0][i].ry;
      //     // }
      //     //We update the globalCarsIds array
      //     globalCarsIds = actCarsIds;
      //   }
      // }
      // else if (data[2][0].run == false && last_check == true) {
      //   //Here we can execute the last frame of the simulation
      //   last_check = false;
      // }
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

  // Load a glTF resource
  async function loadModel(path: string, scale: number, x: number, y: number, z: number, array: THREE.Group[]) {
    const loader = new GLTFLoader();
    // console.log('===== start loadGltf async')
    let gltf = await loader.loadAsync(path)
    // console.log('========== end loadGltf')
    const model = gltf.scene;
    //scene.add(model);
    model.scale.set(scale, scale, scale);
    model.position.set(x, y, z);
    array = []
    array.push(model)
    return array
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