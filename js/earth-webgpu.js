import * as THREE from 'three/webgpu';
import { step, normalWorldGeometry, output, texture, vec3, vec4, normalize, positionWorld, bumpMap, cameraPosition, color, uniform, mix, uv, max } from 'three/tsl';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const canvas = document.getElementById('planetScene');
if (!canvas) throw new Error('No se encontró el canvas del planeta');

const renderer = new THREE.WebGPURenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setAnimationLoop(animate);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(25, 1, 0.1, 100);
camera.position.set(4.5, 2, 3);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.enablePan = false;
controls.enableZoom = false;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.minDistance = 1.7;
controls.maxDistance = 6;

/* Sol */
const sun = new THREE.DirectionalLight('#ffffff', 2);
sun.position.set(0, 0, 3);
scene.add(sun);
scene.add(new THREE.AmbientLight('#ffffff', 0.75));

/* Uniforms */
const atmosphereDayColor = uniform(color('#4db2ff'));
const atmosphereTwilightColor = uniform(color('#bc490b'));
const roughnessLow = uniform(0.25);
const roughnessHigh = uniform(0.35);

/* Texturas */
const textureLoader = new THREE.TextureLoader();
const T = 'https://threejs.org/examples/textures/planets/';

const dayTexture = textureLoader.load(T + 'earth_day_4096.jpg');
dayTexture.colorSpace = THREE.SRGBColorSpace;
dayTexture.anisotropy = 8;

const bumpRoughnessCloudsTexture = textureLoader.load(T + 'earth_bump_roughness_clouds_4096.jpg');
bumpRoughnessCloudsTexture.anisotropy = 8;

/* Fresnel */
const viewDirection = positionWorld.sub(cameraPosition).normalize();
const fresnel = viewDirection.dot(normalWorldGeometry).abs().oneMinus().toVar();

/* Orientación del sol */
const sunOrientation = normalWorldGeometry.dot(normalize(sun.position)).toVar();

/* Color de la atmósfera */
const atmosphereColor = mix(atmosphereTwilightColor, atmosphereDayColor, sunOrientation.smoothstep(-0.25, 0.75));

/* Planeta */
const globeMaterial = new THREE.MeshStandardNodeMaterial();

const cloudsStrength = texture(bumpRoughnessCloudsTexture, uv()).b.smoothstep(0.2, 1);
globeMaterial.colorNode = mix(texture(dayTexture), vec3(1), cloudsStrength.mul(2));

const roughness = max(texture(bumpRoughnessCloudsTexture).g, step(0.01, cloudsStrength));
globeMaterial.roughnessNode = roughness.remap(0, 1, roughnessLow, roughnessHigh);

globeMaterial.outputNode = vec4(output.rgb, output.a);

const bumpElevation = max(texture(bumpRoughnessCloudsTexture).r, cloudsStrength);
globeMaterial.normalNode = bumpMap(bumpElevation);

const sphereGeometry = new THREE.SphereGeometry(1, 64, 64);
const globe = new THREE.Mesh(sphereGeometry, globeMaterial);
scene.add(globe);

/* Anillo de atmósfera */
const atmosphereMaterial = new THREE.MeshBasicNodeMaterial({ side: THREE.BackSide, transparent: true });
let alpha = fresnel.remap(0.73, 1, 1, 0).pow(3);
alpha = alpha.mul(sunOrientation.smoothstep(-0.5, 1));
atmosphereMaterial.outputNode = vec4(atmosphereColor, alpha);

const atmosphere = new THREE.Mesh(sphereGeometry, atmosphereMaterial);
atmosphere.scale.setScalar(1.04);
scene.add(atmosphere);

/* Fondo estelar sutil */
function makeStars(count, radius, minSize, maxSize, opacity) {
  const geom = new THREE.BufferGeometry();
  const pos = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const palette = [new THREE.Color(0xaaccff), new THREE.Color(0xffffff), new THREE.Color(0xfff8e7)];
  for (let i = 0; i < count; i++) {
    const r = radius * (0.7 + Math.random() * 0.5);
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(Math.random() * 2 - 1);
    pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    pos[i * 3 + 2] = r * Math.cos(phi);
    const c = palette[Math.floor(Math.pow(Math.random(), 0.7) * palette.length)];
    colors[i * 3] = c.r;
    colors[i * 3 + 1] = c.g;
    colors[i * 3 + 2] = c.b;
  }
  geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  return new THREE.Points(geom, new THREE.PointsMaterial({
    size: maxSize, transparent: true, opacity, depthWrite: false,
    sizeAttenuation: true, vertexColors: true, blending: THREE.AdditiveBlending,
  }));
}
scene.add(makeStars(900, 60, 0.04, 0.12, 0.8));

/* Reloj para la animación */
const clock = new THREE.Clock();

function animate() {
  const delta = clock.getDelta();
  globe.rotation.y += delta * 0.025;
  controls.update();
  renderer.render(scene, camera);
}

/* Resize al contenedor */
function resize() {
  const w = Math.max(1, canvas.clientWidth);
  const h = Math.max(1, canvas.clientHeight);
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
if (typeof ResizeObserver !== 'undefined') {
  new ResizeObserver(resize).observe(canvas);
} else {
  window.addEventListener('resize', resize);
}
resize();