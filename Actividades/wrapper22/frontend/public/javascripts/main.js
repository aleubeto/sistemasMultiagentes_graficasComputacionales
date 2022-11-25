var location2 = "";
var baseURL = "http://localhost:5000"

fetch(baseURL + "/games", {
  method: "POST"
}).then(response => {
  location2 = response.headers.get('Location');
});

var cam_zpos = 50.0;

function doKeyDown(evt){
    //console.log("Tecla presionada: "+evt.keyCode);
    switch (evt.keyCode) {
        case 38:  /* Up arrow pressed */

            break;
        case 40:  /* Down arrow pressed */

            break;
        case 37:  /* Left arrow pressed */

            break;
        case 39:  /* Right arrow pressed */

            break;
        case 87:  /* W was pressed */
            camera.position.y += 0.5;
        break;
        case 83:  /* S was pressed */
            camera.position.y -= 0.5;
        break;
        case 69:  /* E was pressed */

        break;
        case 68:  /* D was pressed */

        break;
    }
}

// three basic components of a scene
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 1, 1000);
var renderer = new THREE.WebGLRenderer();


var gs = new THREE.SphereGeometry( 8, 32, 16 );
var gslgb = new THREE.SphereGeometry( 8, 32, 16 );


var LambertMaterial2 = new THREE.MeshLambertMaterial(
            {
                color: 0xFFFF00
            });
var LambertMaterial2lgb = new THREE.MeshLambertMaterial(
            {
                color: 0xFF0000
            });
  

var object2 = new THREE.Mesh( gs, LambertMaterial2);
var object2lgb = new THREE.Mesh( gslgb, LambertMaterial2lgb);

group = new THREE.Object3D();           // create an empty container
group.add( object2 );                   // add a mesh with geometry to it

grouplgb = new THREE.Object3D();           // create an empty container
grouplgb.add( object2lgb );                   // add a mesh with geometry to it

groups = { 1: group, 2: grouplgb };

scene.add( group );                     // add the group to the scene
scene.add(grouplgb);

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

camera.position.z = cam_zpos;

// create some point lights
var pointLight = new THREE.PointLight( 0xFFFFFF );
var pointLight2 = new THREE.PointLight( 0xFFFFFF );

// set its position
pointLight.position.x = 10;
pointLight.position.y = 50;
pointLight.position.z = 130;

// add to the scene
scene.add(pointLight);

// set its position
pointLight2.position.x = 10;
pointLight2.position.y = -50;
pointLight2.position.z = -130;

// add to the scene
scene.add(pointLight2);

// set the background color
renderer.setClearColor(0x000022, 1);

const frame_rate = 250; // Refresh screen every 200 ms
var previous_time = Date.now();

var render = async function () {

  var now, elapsed_time;

  now = Date.now();
  elapsed_time = now - previous_time;

  //console.log("elapsed time", elapsed_time);

  if (elapsed_time >= frame_rate) {

    // var xg = 34;
    // var yg = 65;
    // var xglgb = 1;
    // var yglgb = 1;

    if (location2 != ""){ // if the game has been created
      var res = await fetch(baseURL + location2); // get the game state
      var data = await res.json(); // parse JSON to JS object that contains the positions of the 10 robots in every step
      //console.log(data);
      //We print the positions for the first robot
      console.log(data[0].x);
      console.log(data[0].y);

      //We assign the positions to the robots
      group.position.x = data[0].x;
      group.position.y = data[0].y;
      
      //console.log(groups);
      //data.map((d) => { // for each robot
      //  var g = groups[d.id]; 
      //  g.position.x = d.x * 3;
      //  g.position.y = d.y * 3;
      //  return;
      //});

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
