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
const floorPath = 'img/Floor.png'
const songPath = 'sounds/Song.mp3'
const carPath = 'models/Car.glb'
const archPath = 'models/Arch.glb'
const building1Path = 'models/B1.glb'
const building2Path = 'models/B2.glb'
const beaglePath = 'models/Beagle.glb'
const flyDogPath = 'models/FlyDog.glb'
const treePath = 'models/Tree.glb'
const tree2Path = 'models/Tree2.glb'
const tree3Path = 'models/Tree3.glb'

//WE create a texture
function createTexture(path: string) {
  const texture = new THREE.TextureLoader().load(path)
  texture.wrapS = THREE.RepeatWrapping
  texture.wrapT = THREE.RepeatWrapping
  texture.magFilter = THREE.NearestFilter
  //texture.repeat.set(10, 10)
  return texture
}

const concreteTexture = createTexture('img/Concrete.png')
const marmolTexture = createTexture('img/Marmol.png')
const asphaltTexture = createTexture('img/Asphalt.png')

//We create an array to store the cars generated with the GLTFLoader
var cars: THREE.Group[] = []; //The array can be empty
//We create a variable to keep track of how many cars are in the actual frame
var carsNumber: number = 0;
//We create a variable to know which car the camera is focusing
var actCar: number = 0;
//We create a variable to keep track of 'Y' positions when we use the sky camera
var actY: number = 12;
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
//Add an axes helper to the scene
const axesHelper = new THREE.AxesHelper(180)
//scene.add(axesHelper)
//We change the background color of the scene to light blue
scene.background = new THREE.Color(0x87ceeb)
//We add a texture to the background
function addBackground() {
  const loader = new THREE.CubeTextureLoader()
  const texture = loader.load([
    'img/px.jpg',//right
    'img/nx.jpg',//left
    'img/py.jpg',//top
    'img/ny.png',//bottom
    'img/pz.jpg',//front
    'img/nz.jpg',//back
  ])
  scene.background = texture
}

addBackground()

//We add models to the scene
//Here we can add the static models of the scene, like buildings and stuff
addModel(87, 4, 55, 0.5, archPath, -Math.PI / 3)
addModel(0,0,10,1,treePath,0)
addModel(0,0,20,1,tree2Path,0)
addModel(0,0,30,1,tree3Path,0)
addModel(0,0,40,1,building1Path,0)
addModel(0,0,50,1,building2Path,0)
addModel(0,0,60,0.025,beaglePath,0)
addModel(0,0,70,1,flyDogPath,0)

const road1: number[][] = [[90.622, 1.585], [94.329, 1.721], [91.099, 38.503], [87.435, 38.154]]
const road2: number[][] = [[128.353, 1.465], [131.169, 4.111], [98.957, 42.941], [96.408, 40.173]]
const road3: number[][] = [[176.16, 20.491], [177.989, 23.823], [104.591, 50.407], [102.582, 46.941]]
const road4: number[][] = [[178.044, 58.276], [177.862, 62.112], [106.398, 59.087], [106.245, 55.074]]
const road5: number[][] = [[173.614, 115.479], [170.737, 118.024], [100.126, 66.821], [103.02, 64.223]]
const road6: number[][] = [[109.987, 117.077], [106.094, 117.768], [92.291, 71.466], [96.109, 70.577]]
const road7: number[][] = [[82.237, 117.517], [78.407, 117.14], [84.071, 72.443], [87.932, 72.73]]
const road8: number[][] = [[38.615, 118.593], [35.248, 117.086], [75.642, 68.172], [79.095, 69.975]]
const road9: number[][] = [[2.54, 88.206], [1.611, 84.849], [71.395, 60.181], [72.465, 63.863]]
const road10: number[][] = [[2.04, 52.163], [2.125, 48.563], [70.038, 51.043], [70.315, 54.819]]
const road11: number[][] = [[17.033, 4.006], [19.862, 1.521], [76.158, 41.044], [73.657, 43.544]]
const road12: number[][] = [[67.542, 2.178], [71.258, 0.978], [82.871, 38.019], [79.054, 38.889]]

function createPolygon(poly: number[][]) {
  var shape = new THREE.Shape();
  shape.moveTo(poly[0][0], poly[0][1]);
  for (var i = 1; i < poly.length; ++i)
    shape.lineTo(poly[i][0], poly[i][1]);
  shape.lineTo(poly[0][0], poly[0][1]);

  var geometry = new THREE.ShapeGeometry(shape);
  var material = new THREE.MeshBasicMaterial({
    color: 0X7c8a88
  });
  return new THREE.Mesh(geometry, material);
}

//Allow the polygon be seen the 2 sides
function doubleSideAndInclineToFloor(poly: number[][]) {
  var mesh = createPolygon(poly);
  //We rotate the polygon to be in the floor
  mesh.rotateX(Math.PI / 2)
  //We elevate the polygon to be in the floor
  mesh.position.y = 0.1
  mesh.material.side = THREE.DoubleSide;
  //From our already loaded textures we choose the one we want
  mesh.material.map = asphaltTexture
  scene.add(mesh);
}

doubleSideAndInclineToFloor(road1)
doubleSideAndInclineToFloor(road2)
doubleSideAndInclineToFloor(road3)
doubleSideAndInclineToFloor(road4)
doubleSideAndInclineToFloor(road5)
doubleSideAndInclineToFloor(road6)
doubleSideAndInclineToFloor(road7)
doubleSideAndInclineToFloor(road8)
doubleSideAndInclineToFloor(road9)
doubleSideAndInclineToFloor(road10)
doubleSideAndInclineToFloor(road11)
doubleSideAndInclineToFloor(road12)

//We draw and fill a circle
function drawCircle(x: number, y: number, z: number, radius: number, color: number,texture: THREE.Texture) {
  var circle = new THREE.Shape();
  circle.moveTo(0, 0);
  circle.absarc(0, 0, radius, 0, Math.PI * 2, false);
  var geometry = new THREE.ShapeGeometry(circle);
  var material = new THREE.MeshBasicMaterial({
    color: color
  });
  var mesh = new THREE.Mesh(geometry, material);
  mesh.position.x = x
  mesh.position.y = y
  mesh.position.z = z
  mesh.material.side = THREE.DoubleSide;
  mesh.rotateX(Math.PI / 2)
  //From our already loaded textures we choose the one we want
  mesh.material.map = texture
  scene.add(mesh);
}

drawCircle(87, 0.15, 55, 22, 0x7c8a88,asphaltTexture)
drawCircle(87, 0.17, 55, 7, 0xFFFFFF,concreteTexture)


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
addLight(90,20,60) //This is the sun
addLight(0,20,120)

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
      playSong(); //Here we can play a song
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
          x = await data[0][i].x / 10
          z = await data[0][i].y / 10
          x_next = await data[0][i].x_next / 10
          z_next = await data[0][i].y_next / 10
          carAngle = angleBetweenPoints(x, z, x_next, z_next)
          console.log("x ", x, "z ", z, "x_next: ", x_next, "z_next ", z_next/*, carAngle*/)
          loadModel(carPath, 1, x, 0.35, z, cars, carAngle)
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
        for (var i = 0; i < carsNumber; ++i) {
          x = await data[0][i].x / 10
          z = await data[0][i].y / 10
          x_next = await data[0][i].x_next / 10
          z_next = await data[0][i].y_next / 10
          carAngle = angleBetweenPoints(x, z, x_next, z_next)
          // console.log("x ",x,"z ",z,"x_next: ",x_next,"z_next ", z_next, carAngle)
          loadModel(carPath, 1, x, 0.35, z, cars, carAngle)
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
  return angle + (Math.PI / 2);
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
    color: 0xa1adac,
    side: THREE.DoubleSide,
  })
  //We add a texture to the floor
  const floorTexture = new THREE.TextureLoader().load(
    'Asphalt.png'
  )
  floorTexture.wrapS = THREE.RepeatWrapping
  floorTexture.wrapT = THREE.RepeatWrapping
  floorTexture.magFilter = THREE.NearestFilter
  //floorTexture.repeat.set(90, 60)
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

async function addModel(x: number, y: number, z: number, scale: number, path: string, rotation: number = 0) {
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
      if (rotation != 0) {
        model.rotation.y = rotation
      }
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

//Function to add a skybox to the scene taking as parameters the path to the skybox images
async function addSkyBox(path: string) {
  const loader = new THREE.CubeTextureLoader()
  const texture = loader.loadAsync(path).then((texture) => {
    path + 'px.jpg' //Right
    path + 'nx.jpg' //Left
    path + 'py.jpg' //Top
    path + 'ny.jpg' //Bottom
    path + 'pz.jpg' //Front
    path + 'nz.jpg' //Back
    scene.background = texture
  }
  )
    //We catch the error
    .catch((error) => {
      console.log(error);
    }
    );
  return texture;
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