let scene, camera, renderer, avatar;
let mouthMesh = null;
let leftEye = null;
let rightEye = null;
let leftHand = null;
let rightHand = null;

init();
animate();

function init(){

scene = new THREE.Scene();

camera = new THREE.PerspectiveCamera(
45,
window.innerWidth/400,
0.1,
1000
);

/* camera angle (head → stomach view) */
camera.position.set(0,1.4,2.2);

renderer = new THREE.WebGLRenderer({
antialias:true,
alpha:true
});

renderer.setSize(window.innerWidth,400);

document.getElementById("avatarContainer")
.appendChild(renderer.domElement);


/* lights */

const light1 = new THREE.DirectionalLight(0xffffff,1);
light1.position.set(1,2,2);
scene.add(light1);

const light2 = new THREE.AmbientLight(0xffffff,0.6);
scene.add(light2);


/* load avatar */

const loader = new THREE.GLTFLoader();

loader.load("/static/models/avatar.glb", function(gltf){

avatar = gltf.scene;

avatar.scale.set(1.4,1.4,1.4);

/* move slightly down to show stomach */
avatar.position.set(0,-0.8,0);

scene.add(avatar);


/* detect parts */

avatar.traverse(function(node){

if(node.isMesh){

/* detect mouth */
if(node.morphTargetDictionary){
mouthMesh = node;
}

/* detect eyes */
if(node.name.toLowerCase().includes("eye")){

if(!leftEye){
leftEye=node;
}else{
rightEye=node;
}

}

/* detect hands */
if(node.name.toLowerCase().includes("hand")){

if(!leftHand){
leftHand=node;
}else{
rightHand=node;
}

}

}

});


startBlinking();
startHandMovement();

});

}


/* render loop */

function animate(){

requestAnimationFrame(animate);

renderer.render(scene,camera);

}


/* =========================
LIP SYNC (MOUTH MOVEMENT)
========================= */

let lipInterval;

function startLipSync(){

if(!mouthMesh) return;

lipInterval=setInterval(()=>{

let value=Math.random()*0.9;

/* animate mouth */
if(mouthMesh.morphTargetInfluences){

mouthMesh.morphTargetInfluences.forEach((v,i)=>{
mouthMesh.morphTargetInfluences[i]=value;
});

}

},100);

}


function stopLipSync(){

clearInterval(lipInterval);

if(mouthMesh && mouthMesh.morphTargetInfluences){

mouthMesh.morphTargetInfluences.forEach((v,i)=>{
mouthMesh.morphTargetInfluences[i]=0;
});

}

}


/* =========================
EYE BLINK
========================= */

function startBlinking(){

setInterval(()=>{

if(leftEye && rightEye){

leftEye.scale.y = 0.1;
rightEye.scale.y = 0.1;

setTimeout(()=>{

leftEye.scale.y = 1;
rightEye.scale.y = 1;

},150);

}

},3000 + Math.random()*2000);

}


/* =========================
HAND MOVEMENT
========================= */

function startHandMovement(){

setInterval(()=>{

if(leftHand){

leftHand.rotation.z += 0.15;

setTimeout(()=>{
leftHand.rotation.z -= 0.15;
},400);

}

if(rightHand){

rightHand.rotation.z -= 0.15;

setTimeout(()=>{
rightHand.rotation.z += 0.15;
},400);

}

},4000);

}


/* =========================
SPEAK FUNCTION
========================= */

function speak(text){

const speech = new SpeechSynthesisUtterance(text);

speech.rate = 1;

speech.onstart = function(){
startLipSync();
};

speech.onend = function(){
stopLipSync();
};

speechSynthesis.speak(speech);

}