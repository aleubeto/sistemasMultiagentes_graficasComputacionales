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
//const floorPath = 'https://threejsfundamentals.org/threejs/resources/images/checker.png'
const floorPath = 'img/Paris.png'
const songPath = 'sounds/Song.mp3'
const carPath = 'models/Car.glb'


//We create an array to store the cars generated with the GLTFLoader
var cars: THREE.Group[] = []; //The array can be empty
//We create a variable to keep track of how many cars are in the actual frame
var carsNumber: number = 0;
//We create a variable to know which car the camera is focusing
var actCar: number = 0;
//We create a variable to keep track of 'Y' positions when we use the sky camera
var actY: number = 12;
//We create a global array to keep track of the cars IDs, last frame
var globalCarsIds: number[] = [];
//We create a global array to keep track of the cars IDs in every frame
var actCarsIds: number[] = [];
//We create a global boolean to know if the cars are the same as the last frame
var changedCars: boolean = false;
var x: number = 0;
var z: number = 0;
var x_next: number = 0;
var z_next: number = 0;
var carAngle: number = 0;

//We load the model
//loadModel('models/Car.glb', 0.0025, 0, 0, 0, cars)
// for (let i = 0; i < carsNumber; i++) {
//   loadModel('models/Car2.glb', 1, i, 0, 0, cars/*, Math.PI / 2*/);
// }
// console.log(cars)
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
const axesHelper = new THREE.AxesHelper(180)
scene.add(axesHelper)

//We add a cube to the scene with a for loop
// function addCube(x:number,y:number,z:number) {
//   const geometry = new THREE.BoxGeometry(1, 1, 1)
//   const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 })
//   const cube = new THREE.Mesh(geometry, material)
//   scene.add(cube)
//   cube.position.x = x
//   cube.position.y = y
//   cube.position.z = z
// }

// addCube(0.5,0.5,0.5)

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
const frame_rate = 400; // Refresh screen every 200 ms
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
      var data = await res.json(); // parse JSON to JS object that contains the positions of the car


      if (firstFrame == true) {
        camera.lookAt(30, -5, 10) //This is the first position the camera will look at
        carsNumber = await data[0].length;
        console.log(carsNumber)
        for (var i = 0; i < carsNumber; ++i) {
          x = await data[0][i].x/10
          z = await data[0][i].y/10
          x_next = await data[0][i].x_next/10
          z_next = await data[0][i].y_next/10
          carAngle = angleBetweenPoints(x,z,x_next,z_next)
          console.log("x ",x,"z ",z,"x_next: ",x_next,"z_next ", z_next/*, carAngle*/)
          loadModel(carPath,1,x,0,z,cars,carAngle)
          console.log("1st frame: ", cars)
          //loadModel(carPath,10,x_next,2,z_next,cars,carAngle)
        }
      }

      firstFrame = false;


      //If the cars array position is not undefined we update the position of the car
      if (cars[0] != undefined && data[2][0].run == true) {
        // console.log("Loop: ", cars)
        //Here we update the cars position every frame
        console.log("Here")
        //We clean the scene
        for (var i = 0; i < carsNumber; ++i) {
          scene.remove(cars[i])
        }
        carsNumber = await data[0].length;
        cars = []
        for (var i=0;i<carsNumber;++i){
          x = await data[0][i].x/10
          z = await data[0][i].y/10
          x_next = await data[0][i].x_next/10
          z_next = await data[0][i].y_next/10
          carAngle = angleBetweenPoints(x,z,x_next,z_next)
          // console.log("x ",x,"z ",z,"x_next: ",x_next,"z_next ", z_next, carAngle)
          loadModel(carPath,1,x,0,z,cars,carAngle)
        }
        console.log("Cars Number: ", carsNumber)
        console.log(cars)
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

// Load a glTF resource
async function loadModel(path: string, scale: number, x: number, y: number, z: number, array: THREE.Group[], rotation: number = 0) {
  const loader = new GLTFLoader();
  // console.log('===== start loadGltf async')
  let gltf = await loader.loadAsync(path).then((gltf) => {
    console.log('===== loadGltf async done')
    //console.log(gltf.scene)
    gltf.scene.scale.set(scale, scale, scale);
    gltf.scene.position.set(x, y, z);
    if (rotation != 0) {
      gltf.scene.rotateY(rotation);
    }
    scene.add(gltf.scene);
    array.push(gltf.scene);
    console.log('===== loadGltf async end')
  }
  )
    //We catch the error
    .catch((error) => {
      console.log(error);
    });
  return gltf;
}

//Function to calculate angle between two points
function angleBetweenPoints(x1: number, y1: number, x2: number, y2: number) {
  var angle = Math.atan2(y2 - y1, x2 - x1);
  return angle+(Math.PI/2);
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
  const floorGeometry = new THREE.PlaneGeometry(180, 120, 1, 1)
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
  //floorTexture.repeat.set(90, 60)
  floorMaterial.map = floorTexture
  const floor = new THREE.Mesh(floorGeometry, floorMaterial)
  floor.rotation.x = Math.PI / 2
  // //We move the floor 30 units to the right
  floor.position.x = 90
  // //We move the floor 30 units to the front
  floor.position.z = 60
  scene.add(floor)
}

//We play a song
function playSong() {
  var audio = new Audio(songPath);
  audio.play();
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

// GUI
const gui = new GUI() //Dat.gui
const cameraFolder = gui.addFolder('Camera') //Add a cameraFolder to the dat.gui
cameraFolder.add(camera.position, 'x', -100, 100, 0.01) //Add the x position to the dat.gui
cameraFolder.add(camera.position, 'y', -100, 100, 0.01) //Add the y position to the dat.gui
cameraFolder.add(camera.position, 'z', -100, 100, 0.01) //Add the z position to the dat.gui
cameraFolder.add(camera.rotation, 'x', 0, 2 * Math.PI, 0.01) //Add the x rotation to the dat.gui
cameraFolder.add(camera.rotation, 'y', 0, 2 * Math.PI, 0.01) //Add the y rotation to the dat.gui
cameraFolder.add(camera.rotation, 'z', 0, 2 * Math.PI, 0.01) //Add the z rotation to the dat.gui

setFloor();
render();