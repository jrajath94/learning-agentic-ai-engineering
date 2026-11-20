document.querySelectorAll('pre').forEach(function(pre){
  var btn=document.createElement('button'); btn.type='button'; btn.textContent='Copy';
  btn.style.cssText='float:right;font-size:12px;padding:2px 10px;cursor:pointer';
  btn.addEventListener('click', function(){
    navigator.clipboard.writeText(pre.innerText).then(function(){ btn.textContent='Copied'; setTimeout(function(){btn.textContent='Copy';},1500); });
  });
  pre.parentNode.insertBefore(btn, pre);
});
