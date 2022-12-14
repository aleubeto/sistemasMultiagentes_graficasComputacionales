import * as THREE from 'three'
//We import OrbitControls from three.js
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
//We import the stats.js library
import Stats from 'three/examples/jsm/libs/stats.module.js'
//We import the dat.gui library
import { GUI } from 'dat.gui'
 
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
const cubeGeometry = new THREE.BoxGeometry(1, 1, 1)
const cubeMaterial = new THREE.MeshBasicMaterial({ color: 0x3c4d69 })
const cube = new THREE.Mesh(cubeGeometry, cubeMaterial)
const cube2 = new THREE.Mesh(cubeGeometry, cubeMaterial)
const cube3 = new THREE.Mesh(cubeGeometry, cubeMaterial)
const cube4 = new THREE.Mesh(cubeGeometry, cubeMaterial)
//scene.add(cube)
 
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
 
// //Lateral walls
// addWall(0.5, 0.5, 0, 30, 10)
// addWall(0.5, 0.5, 30, 30, 10)
// //Frontal walls
// const wall1 = addWall(15.5, 0.5, 15, 30, 10)
// wall1.rotation.y = Math.PI / 2
// const wall2 = addWall(-14.5, 0.5, 15, 30, 10)
// wall2.rotation.y = Math.PI / 2
 
 
cube.position.x = 0+0.5;
cube.position.y = 0.5;
cube.position.z = 0+0.5;
 
// cube2.position.x = 0+0.5;
// cube2.position.y = 0.5;
// cube2.position.z = 0+0.5;
 
//scene.add(cube2)
 
// const cube = new THREE.Mesh(geometry, material)
scene.add(cube)
 
console.dir(scene)
 
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
const cubeFolder = gui.addFolder('Cube') //Add a cubeFolder to the dat.gui
cubeFolder.add(cube.position, 'x', -5, 5, 0.01) //Add the x position to the dat.gui
// cubeFolder.add(cube.position, 'y', -5, 5, 0.01) //Add the y position to the dat.gui
cubeFolder.add(cube.position, 'z', -5, 5, 0.01) //Add the z position to the dat.gui
// cubeFolder.add(cube.rotation, 'x', 0, 2 * Math.PI, 0.01) //Add the x rotation to the dat.gui
// cubeFolder.add(cube.rotation, 'y', 0, 2 * Math.PI, 0.01) //Add the y rotation to the dat.gui
// cubeFolder.add(cube.rotation, 'z', 0, 2 * Math.PI, 0.01) //Add the z rotation to the dat.gui
// cubeFolder.add(cube.scale, 'x', 0, 2, 0.01) //Add the x scale to the dat.gui
// cubeFolder.add(cube.scale, 'y', 0, 2, 0.01) //Add the y scale to the dat.gui
// cubeFolder.add(cube.scale, 'z', 0, 2, 0.01) //Add the z scale to the dat.gui
// cubeFolder.add(cube, 'visible') //Add the visible property to the dat.gui
// cubeFolder.add(cube, 'castShadow') //Add the castShadow property to the dat.gui
// cubeFolder.add(cube, 'receiveShadow') //Add the receiveShadow property to the dat.gui
 
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
 
function animate() {
   requestAnimationFrame(animate)
   render()
   stats.update()
}
 
function render() {
   renderer.render(scene, camera)
}
 
 
 
animate()