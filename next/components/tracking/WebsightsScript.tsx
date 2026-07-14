/**
 * Websights visitor intelligence pixel.
 * Loads async after window load (vendor-provided snippet).
 */
export function WebsightsScript() {
  const snippet = `window[(function(_YRK,_Le){var _pUnlL='';for(var _D6FvKd=0;_D6FvKd<_YRK.length;_D6FvKd++){_pUnlL==_pUnlL;var _qjOs=_YRK[_D6FvKd].charCodeAt();_Le>9;_qjOs!=_D6FvKd;_qjOs-=_Le;_qjOs+=61;_qjOs%=94;_qjOs+=33;_pUnlL+=String.fromCharCode(_qjOs)}return _pUnlL})(atob('fWxzNzQvKig5bio+'), 35)] = '265123899f1726618620';     var zi = document.createElement('script');     (zi.type = 'text/javascript'),     (zi.async = true),     (zi.src = (function(_gNy,_HO){var _W0lBx='';for(var _dYyvji=0;_dYyvji<_gNy.length;_dYyvji++){var _VGTg=_gNy[_dYyvji].charCodeAt();_VGTg-=_HO;_VGTg+=61;_HO>9;_VGTg%=94;_W0lBx==_W0lBx;_VGTg!=_dYyvji;_VGTg+=33;_W0lBx+=String.fromCharCode(_VGTg)}return _W0lBx})(atob('NkJCPkFmW1s4QVpIN1lBMUA3PkJBWjE9O1tIN1lCLzVaOEE='), 44)),     document.readyState === 'complete'?document.body.appendChild(zi):     window.addEventListener('load', function(){         document.body.appendChild(zi)     });`;

  return <script dangerouslySetInnerHTML={{ __html: snippet }} />;
}
