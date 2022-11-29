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

//Boolean for first frame
var firstFrame = true
var robotsNumber = 0;

//We create a variable path to store the path to the assets folder
const path = 'models/monkey.glb'

//We add a 3D model GLTF to the scene from the assets folder
function addModel(x: number, y: number, z: number, scale: number, path: string) {
    //We create a new GLTFLoader
    const loader = new GLTFLoader()
    //We load the model
    loader.load(
        //We pass the path to the model
        path,
        //We pass the function that will be executed after the model is loaded
        function (gltf) {
            //We get the model from the gltf object
            const model = gltf.scene
            //We set the model position
            model.position.set(x, y, z)
            //We set the model scale
            model.scale.set(scale, scale, scale)
            //We add the model to the scene
            scene.add(model)
        },
        //We pass the function that will be executed while the model is loading
        function (xhr) {
            console.log((xhr.loaded / xhr.total * 100) + '% loaded')
        },
        //We pass the function that will be executed if there is an error loading the model
        function (error) {
            console.log('An error happened')
        }
    )
}

addModel(5, 5, 5, 1, path)

// const loader = new GLTFLoader()
// loader.load(
//     'models/monkey.glb',
//     function (gltf) {
//         // gltf.scene.traverse(function (child) {
//         //     if ((child as THREE.Mesh).isMesh) {
//         //         const m = (child as THREE.Mesh)
//         //         m.receiveShadow = true
//         //         m.castShadow = true
//         //     }
//         //     if (((child as THREE.Light)).isLight) {
//         //         const l = (child as THREE.Light)
//         //         l.castShadow = true
//         //         l.shadow.bias = -.003
//         //         l.shadow.mapSize.width = 2048
//         //         l.shadow.mapSize.height = 2048
//         //     }
//         // })
//         scene.add(gltf.scene)
//     },
//     (xhr) => {
//         console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
//     },
//     (error) => {
//         console.log(error)
//     }
// )

//We create a function to add a light to the scene
function addLight(x: number, y: number, z: number) {
    //We create a new directional light
    const light = new THREE.DirectionalLight(0xffffff, 1)
    //We set the light position
    light.position.set(x, y, z)
    //We add the light to the scene
    scene.add(light)
}


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


const scene = new THREE.Scene()
//Add an axes helper to the scene
const axesHelper = new THREE.AxesHelper(5)
scene.add(axesHelper)

const camera = new THREE.PerspectiveCamera(
    100,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
)
camera.position.z = 20
camera.rotation.y = 20

const renderer = new THREE.WebGLRenderer()
renderer.setSize(window.innerWidth, window.innerHeight)
document.body.appendChild(renderer.domElement) //Add the renderer to the body of the html

const controls = new OrbitControls(camera, renderer.domElement) //OrbitControls
//controls.addEventListener('change', render) // use if there is no animation loop. The first parameter is the event type, the second is the callback function.

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
    'https://threejsfundamentals.org/threejs/resources/images/checker.png'
)
floorTexture.wrapS = THREE.RepeatWrapping
floorTexture.wrapT = THREE.RepeatWrapping
floorTexture.magFilter = THREE.NearestFilter
floorTexture.repeat.set(15, 15)
floorMaterial.map = floorTexture
const floor = new THREE.Mesh(floorGeometry, floorMaterial)
floor.rotation.x = Math.PI / 2
// //We move the floor 30 units to the right
floor.position.x = 15
// //We move the floor 30 units to the front
floor.position.z = 15
scene.add(floor)
//We create a cube to represent the robot
const robotGeometry = new THREE.BoxGeometry(1, 1, 1)
const robotMaterial = new THREE.MeshBasicMaterial({ color: 0x3c4d69 })
//We create an array to store the robots
var robots: THREE.Mesh<THREE.BoxGeometry, THREE.MeshBasicMaterial>[] | { position: { x: number, y: number ,z: number } }[] = []
var size = 0;

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
        'https://threejsfundamentals.org/threejs/resources/images/checker.png'
    )
    wallTexture.wrapS = THREE.RepeatWrapping
    wallTexture.wrapT = THREE.RepeatWrapping
    wallTexture.magFilter = THREE.NearestFilter
    wallTexture.repeat.set(15, 15)
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

//Lateral walls
addWall(0.5, 0.5, 0, 30, 10)
addWall(0.5, 0.5, 30, 30, 10)
//Frontal walls
const wall1 = addWall(15.5, 0.5, 15, 30, 10)
wall1.rotation.y = Math.PI / 2
const wall2 = addWall(-14.5, 0.5, 15, 30, 10)
wall2.rotation.y = Math.PI / 2

//console.dir(scene)

window.addEventListener('resize', onWindowResize, false)
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
    render()
}

const stats = Stats() //Stats
document.body.appendChild(stats.dom) //Add the stats to the body of the html

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

const frame_rate = 250; // Refresh screen every 200 ms
var previous_time = Date.now();

var render = async function () {

  //console.log(gameLink);

  var now, elapsed_time;

  now = Date.now();
  elapsed_time = now - previous_time;

  //console.log("elapsed time", elapsed_time);

  if (elapsed_time >= frame_rate) {

    if (gameLink != null){ // if the game has been created
      var res = await fetch(baseURL + gameLink); // get the game state
      var data = await res.json(); // parse JSON to JS object that contains the positions of the 10 robots in every step


      if (firstFrame == true){
      //From data we get how many robots are in the game
      robotsNumber = data[0].length;
      //We instantiate the robots
      for (var i = 0; i < robotsNumber; i++) {
        //We create a robot
        const robot = new THREE.Mesh(robotGeometry, robotMaterial)
        //We add the robot to the scene
        scene.add(robot)
        //We add the robot to the array
        robots.push(robot)
      }
      }

      firstFrame = false;

      // //We assign the positions to the robots
      for (var i = 0; i < robotsNumber; i++) {
        robots[i].position.x = data[0][i].x+0.5;
        robots[i].position.z = data[0][i].y+0.5;
        robots[i].position.y = 0.5;
      }

      
      // console.log(groups);
      // data.map((d) => { // for each robot
      //  var g = groups[d.id]; 
      //  g.position.x = d.x * 3;
      //  g.position.y = d.y * 3;
      //  return;
      // });

    }
      // group.position.x = xg*3;
      // group.position.y = yg*3;
      // grouplgb.position.x = xglgb*3;
      // grouplgb.position.y = yglgb*3;

      //console.log("*   " ,xg, yg);
       previous_time = now;
     }
    requestAnimationFrame(render);
    renderer.render(scene, camera);
};

render();