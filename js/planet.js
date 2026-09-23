import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const canvas = document.getElementById("planetScene");
if (!canvas) throw new Error("No se encontró el canvas del planeta");

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 250);
camera.position.set(0, 1.5, 3.4);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.enablePan = false;
controls.enableZoom = false;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.8;
controls.minDistance = 2.2;
controls.maxDistance = 6;

scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const sun = new THREE.DirectionalLight(0xffffff, 1.7);
sun.position.set(6, 3, 2);
scene.add(sun);

/* ---------- Fondo estelar ---------- */
function makeStarField({ count = 1200, radius = 60, minSize = 0.03, maxSize = 0.11, opacity = 0.9, seed = 0 }) {
  const geom = new THREE.BufferGeometry();
  const pos = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const sizes = new Float32Array(count);
  const palette = [
    new THREE.Color(0xaaccff),
    new THREE.Color(0xffffff),
    new THREE.Color(0xfff8e7),
    new THREE.Color(0xffd699),
  ];
  for (let i = 0; i < count; i++) {
    const r = radius * (0.7 + Math.random() * 0.6);
    const theta = Math.random() * Math.PI * 2;
    const u = Math.random() * 2 - 1;
    const phi = Math.acos(u);
    pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    pos[i * 3 + 2] = r * Math.cos(phi);
    sizes[i] = THREE.MathUtils.lerp(minSize, maxSize, Math.pow(Math.random(), 2));
    const col = palette[Math.min(Math.floor(Math.pow(Math.random(), 0.7) * palette.length), palette.length - 1)];
    colors[i * 3] = col.r;
    colors[i * 3 + 1] = col.g;
    colors[i * 3 + 2] = col.b;
  }
  geom.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geom.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  const pts = new THREE.Points(geom, new THREE.PointsMaterial({
    size: maxSize, transparent: true, opacity, depthWrite: false, sizeAttenuation: true, vertexColors: true,
  }));
  pts.userData = { sp: 0.8 + Math.random() * 0.6, base: opacity };
  return pts;
}
const starsFar = makeStarField({ count: 2200, radius: 90, minSize: 0.02, maxSize: 0.07, opacity: 0.85, seed: 1 });
const starsNear = makeStarField({ count: 900, radius: 60, minSize: 0.05, maxSize: 0.13, opacity: 0.8, seed: 2 });
scene.add(starsFar, starsNear);

function twinkle(pts, t) {
  pts.material.opacity = pts.userData.base * (0.78 + 0.22 * Math.sin(t * pts.userData.sp) * Math.cos(t * pts.userData.sp * 0.7));
}

/* ---------- Nebulosas sutiles ---------- */
function makeNebula(x, y, z, scale, c1, c2, opacity) {
  const c = document.createElement("canvas");
  c.width = c.height = 256;
  const g = c.getContext("2d");
  const grad = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grad.addColorStop(0, c1);
  grad.addColorStop(1, "rgba(0,0,0,0)");
  g.fillStyle = grad;
  g.fillRect(0, 0, 256, 256);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({
    map: tex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, opacity,
  }));
  s.position.set(x, y, z);
  s.scale.set(scale, scale, 1);
  return s;
}
scene.add(
  makeNebula(-25, 12, -40, 70, "rgba(180,100,255,0.35)", "rgba(0,0,0,0)", 0.22),
  makeNebula(28, -18, -42, 60, "rgba(255,120,180,0.3)", "rgba(0,0,0,0)", 0.18),
  makeNebula(20, 26, -48, 55, "rgba(100,180,255,0.3)", "rgba(0,0,0,0)", 0.16)
);

/* ---------- Polvo cósmico ---------- */
const dustCount = 300;
const dustGeo = new THREE.BufferGeometry();
const dustPos = new THREE.BufferAttribute(new Float32Array(dustCount * 3), 3);
for (let i = 0; i < dustCount * 3; i++) dustPos.array[i] = (Math.random() - 0.5) * 30;
dustGeo.setAttribute("position", dustPos);
const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({
  size: 0.03, color: 0x8888aa, transparent: true, opacity: 0.4, depthWrite: false, blending: THREE.AdditiveBlending,
}));
scene.add(dust);

/* ---------- Texturas del planeta ---------- */
const loader = new THREE.TextureLoader();
const aniso = renderer.capabilities.getMaxAnisotropy();
const colorTex = (u) => { const t = loader.load(u); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = aniso; return t; };
const dataTex = (u) => { const t = loader.load(u); t.anisotropy = aniso; return t; };
const url = (name) => `https://threejs.org/examples/textures/planets/${name}`;
const earthColor = colorTex(url("earth_atmos_2048.jpg"));
const earthLights = dataTex(url("earth_lights_2048.png"));
const earthNormal = dataTex(url("earth_normal_2048.jpg"));
const earthSpec = dataTex(url("earth_specular_2048.jpg"));
const cloudsAlpha = dataTex(url("earth_clouds_1024.png"));
const moonTex = colorTex(url("moon_1024.jpg"));

/* ---------- Planeta + nubes + atmósfera ---------- */
const planet = new THREE.Mesh(
  new THREE.SphereGeometry(1, 96, 96),
  new THREE.MeshPhongMaterial({
    map: earthColor, normalMap: earthNormal, specularMap: earthSpec,
    specular: new THREE.Color(0x333333), shininess: 18,
    emissiveMap: earthLights, emissive: 0xffffff, emissiveIntensity: 0.5, dithering: true,
  })
);
planet.rotation.z = THREE.MathUtils.degToRad(23.4);
scene.add(planet);

const clouds = new THREE.Mesh(
  new THREE.SphereGeometry(1.012, 96, 96),
  new THREE.MeshPhongMaterial({ alphaMap: cloudsAlpha, transparent: true, depthWrite: false, opacity: 0.55, side: THREE.DoubleSide })
);
clouds.rotation.z = planet.rotation.z;
scene.add(clouds);

const clouds2 = new THREE.Mesh(
  new THREE.SphereGeometry(1.018, 64, 64),
  new THREE.MeshPhongMaterial({ alphaMap: cloudsAlpha, transparent: true, depthWrite: false, opacity: 0.22 })
);
clouds2.rotation.z = planet.rotation.z;
scene.add(clouds2);

const vs = `varying vec3 vN; varying vec3 vP; void main(){ vN=normalize(normalMatrix*normal); vP=(modelViewMatrix*vec4(position,1.0)).xyz; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}`;
const fs = `uniform vec3 glowColor; uniform float intensity; uniform float power; varying vec3 vN; varying vec3 vP; void main(){ vec3 vd=normalize(-vP); float f=pow(1.0-abs(dot(vd,vN)),power); gl_FragColor=vec4(glowColor,f*intensity);}`;
const atmo = new THREE.Mesh(new THREE.SphereGeometry(1.15, 64, 64), new THREE.ShaderMaterial({
  vertexShader: vs, fragmentShader: fs,
  uniforms: { glowColor: { value: new THREE.Color(0x00b4ff) }, intensity: { value: 0.75 }, power: { value: 3.5 } },
  side: THREE.BackSide, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false,
}));
scene.add(atmo);
const atmo2 = new THREE.Mesh(new THREE.SphereGeometry(1.02, 64, 64), new THREE.ShaderMaterial({
  vertexShader: vs, fragmentShader: fs,
  uniforms: { glowColor: { value: new THREE.Color(0x88ddff) }, intensity: { value: 0.35 }, power: { value: 2 } },
  side: THREE.FrontSide, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false,
}));
scene.add(atmo2);

const glowCanvas = document.createElement("canvas");
glowCanvas.width = glowCanvas.height = 256;
{
  const g = glowCanvas.getContext("2d");
  const grad = g.createRadialGradient(128, 128, 40, 128, 128, 128);
  grad.addColorStop(0, "rgba(100,200,255,0.15)");
  grad.addColorStop(0.5, "rgba(50,150,255,0.05)");
  grad.addColorStop(1, "rgba(0,100,200,0)");
  g.fillStyle = grad;
  g.fillRect(0, 0, 256, 256);
}
const glowTex = new THREE.CanvasTexture(glowCanvas);
glowTex.colorSpace = THREE.SRGBColorSpace;
const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
glow.scale.set(4, 4, 1);
scene.add(glow);

/* ---------- Luna ---------- */
const moonPivot = new THREE.Object3D();
scene.add(moonPivot);
const moon = new THREE.Mesh(
  new THREE.SphereGeometry(0.32, 48, 48),
  new THREE.MeshPhongMaterial({ map: moonTex, shininess: 8 })
);
moon.position.set(3.4, 0, 0);
moonPivot.add(moon);
moonPivot.rotation.x = THREE.MathUtils.degToRad(5);
moonPivot.rotation.z = THREE.MathUtils.degToRad(6);
let moonAngle = 0;

/* ---------- Satélites ---------- */
const shipGlowCanvas = document.createElement("canvas");
shipGlowCanvas.width = shipGlowCanvas.height = 128;
{
  const g = shipGlowCanvas.getContext("2d");
  const gr = g.createRadialGradient(64, 64, 4, 64, 64, 64);
  gr.addColorStop(0, "rgba(100,220,255,0.6)");
  gr.addColorStop(0.4, "rgba(50,180,255,0.25)");
  gr.addColorStop(1, "rgba(0,100,200,0)");
  g.fillStyle = gr;
  g.fillRect(0, 0, 128, 128);
}
const shipGlowTex = new THREE.CanvasTexture(shipGlowCanvas);
shipGlowTex.colorSpace = THREE.SRGBColorSpace;

function makeSatellite(r, spd) {
  const pivot = new THREE.Object3D();
  pivot.rotation.x = THREE.MathUtils.degToRad((Math.random() * 20) - 10);
  pivot.rotation.z = THREE.MathUtils.degToRad((Math.random() * 20) - 10);
  const ship = new THREE.Group();
  const body = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.12, 0.12), new THREE.MeshStandardMaterial({ color: 0xd9d9d9, metalness: 0.7, roughness: 0.3 }));
  const panelMat = new THREE.MeshStandardMaterial({ color: 0x1a2c66, metalness: 0.2, roughness: 0.5, emissive: 0x0a1733, emissiveIntensity: 0.2 });
  const p1 = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 0.1), panelMat);
  p1.rotation.y = Math.PI / 2;
  p1.position.z = 0.12;
  const p2 = p1.clone();
  p2.position.z = -0.12;
  p2.rotation.y = -Math.PI / 2;
  const g = new THREE.Sprite(new THREE.SpriteMaterial({ map: shipGlowTex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, opacity: 0.25 }));
  g.scale.set(0.9, 0.9, 1);
  ship.add(body, p1, p2, g);
  ship.position.set(r, 0, 0);
  pivot.add(ship);
  const pts = [];
  for (let k = 0; k < 96; k++) {
    const a = (k / 95) * Math.PI * 2;
    pts.push(new THREE.Vector3(Math.cos(a) * r, 0, Math.sin(a) * r));
  }
  pivot.add(new THREE.LineLoop(
    new THREE.BufferGeometry().setFromPoints(pts),
    new THREE.LineBasicMaterial({ color: 0x2a4a7a, transparent: true, opacity: 0.16 })
  ));
  scene.add(pivot);
  return { pivot, r, ang: Math.random() * Math.PI * 2, spd, dir: Math.random() < 0.4 ? -1 : 1 };
}
const satellites = [];
for (let i = 0; i < 4; i++) {
  const r = 1.7 + i * 0.5;
  satellites.push(makeSatellite(r, (0.5 / Math.pow(r, 1.5)) * THREE.MathUtils.lerp(0.7, 1.4, Math.random())));
}

/* ---------- Animación ---------- */
let t = 0;
let last = performance.now();
function animate() {
  requestAnimationFrame(animate);
  const now = performance.now();
  const dt = Math.min(0.1, (now - last) / 1000);
  last = now;
  t += 0.005;

  planet.rotation.y += 0.0016;
  clouds.rotation.y += 0.0022;
  clouds2.rotation.y += 0.0015;

  moonAngle += 0.07 * dt;
  moonPivot.rotation.y = moonAngle;
  moon.rotation.y += 0.003;

  satellites.forEach((s) => {
    s.ang += s.dir * s.spd * dt;
    s.pivot.rotation.y = s.ang;
  });

  twinkle(starsFar, t);
  twinkle(starsNear, t * 0.8);
  dust.rotation.y += 0.0004;

  controls.update();
  renderer.render(scene, camera);
}
animate();

/* ---------- Resize ---------- */
function resize() {
  const w = Math.max(1, canvas.clientWidth);
  const h = Math.max(1, canvas.clientHeight);
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
if (typeof ResizeObserver !== "undefined") {
  new ResizeObserver(resize).observe(canvas);
} else {
  window.addEventListener("resize", resize);
}
resize();