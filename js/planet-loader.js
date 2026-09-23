async function bootPlanet() {
  try {
    const adapter = navigator.gpu && await navigator.gpu.requestAdapter();
    if (!adapter) throw new Error('sin adapter WebGPU');
    await import('./earth-webgpu.js');
  } catch (err) {
    console.warn('[conecta+] WebGPU no disponible, se usa el planeta WebGL.', err);
    try {
      await import('./planet.js');
    } catch (e) {
      console.error('[conecta+] El planeta WebGL tampoco pudo cargarse.', e);
    }
  }
}
bootPlanet();