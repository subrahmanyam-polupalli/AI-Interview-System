
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

    camera = new THREE.PerspectiveCamera(45, window.innerWidth/400, 0.1, 1000);
    camera.position.set(0, 1.6, 2.2);
    camera.lookAt(0, 1.4, 0);           

    renderer = new THREE.WebGLRenderer({ antialias:true, alpha:true });
   renderer.setSize(document.getElementById("avatarContainer").clientWidth, 400);
    const container = document.getElementById("avatarContainer");
    if (container) {
        container.appendChild(renderer.domElement);
    }

    const light1 = new THREE.DirectionalLight(0xffffff, 1);
    light1.position.set(1,2,2);
    scene.add(light1);

    const light2 = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(light2);

    const loader = new THREE.GLTFLoader();
    loader.load("/static/models/avatar.glb", function(gltf){
        avatar = gltf.scene;
        avatar.scale.set(1.4, 1.4, 1.4);
        avatar.position.set(0, -1.2, 0);
        scene.add(avatar);
        avatar.position.x = 0;

        avatar.traverse(function(node){
            if(node.isMesh){
                if(node.morphTargetDictionary){
                    mouthMesh = node;
                }
                if(node.name && node.name.toLowerCase().includes("eye")){
                    if(!leftEye){ leftEye = node; }
                    else { rightEye = node; }
                }
                if(node.name && node.name.toLowerCase().includes("hand")){
                    if(!leftHand){ leftHand = node; }
                    else { rightHand = node; }
                }
            }
        });

        startBlinking();
        startHandMovement();
    });
}

function animate(){
    requestAnimationFrame(animate);
    if (renderer && scene && camera) renderer.render(scene, camera);
}

let lipInterval;

function startLipSync(){
    if(!mouthMesh) return;
    lipInterval = setInterval(() => {
        let value = Math.random() * 0.9;
        if(mouthMesh.morphTargetInfluences){
            mouthMesh.morphTargetInfluences.forEach((_, i) => {
                mouthMesh.morphTargetInfluences[i] = value;
            });
        }
    }, 100);
}

function stopLipSync(){
    clearInterval(lipInterval);
    if(mouthMesh && mouthMesh.morphTargetInfluences){
        mouthMesh.morphTargetInfluences.forEach((_, i) => {
            mouthMesh.morphTargetInfluences[i] = 0;
        });
    }
}

function startBlinking(){
    setInterval(() => {
        if(leftEye && rightEye){
            leftEye.scale.y = 0.1;
            rightEye.scale.y = 0.1;
            setTimeout(() => {
                leftEye.scale.y = 1;
                rightEye.scale.y = 1;
            }, 150);
        }
    }, 3000 + Math.random()*2000);
}

function startHandMovement(){
    setInterval(() => {
        if(leftHand){
            leftHand.rotation.z += 0.15;
            setTimeout(() => { leftHand.rotation.z -= 0.15; }, 400);
        }
        if(rightHand){
            rightHand.rotation.z -= 0.15;
            setTimeout(() => { rightHand.rotation.z += 0.15; }, 400);
        }
    }, 4000);
}

function speak(text){
    const speech = new SpeechSynthesisUtterance(text);
    speech.rate = 1;
    speech.onstart = function(){ startLipSync(); };
    speech.onend = function(){ stopLipSync(); };
    speechSynthesis.cancel();
    speechSynthesis.speak(speech);
}

function toggleMenu(){
    let sidebar = document.getElementById("sidebar");
    if(!sidebar) return;
    if(sidebar.style.left === "0px"){
        sidebar.style.left = "-220px";
    } else {
        sidebar.style.left = "0px";
    }
}
