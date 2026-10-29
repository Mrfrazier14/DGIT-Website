document.addEventListener('DOMContentLoaded',()=>{const t=document.querySelector('.nav-toggle'),n=document.querySelector('.nav-links');if(t&&n){t.addEventListener('click',()=>{const open=n.classList.toggle('open');t.setAttribute('aria-expanded',String(open));});n.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{n.classList.remove('open');t.setAttribute('aria-expanded','false');}));}const y=document.querySelector('#year');if(y)y.textContent=new Date().getFullYear();});

document.addEventListener('DOMContentLoaded',()=>{
 const field=document.getElementById('service');
 if(!field)return;
 const requested=new URLSearchParams(location.search).get('service');
 const aliases={
 'cybersecurity-consulting':'remote-it-support','microsoft-365':'remote-it-support','onboarding':'remote-it-support','network-systems':'remote-it-support','it-consulting':'remote-it-support','deployment':'remote-it-support','vendor-onboarding':'remote-it-support',
 'websites':'software-development','reporting':'software-development',
 'business-ai':'ai-workflows','gray-fox':'ai-workflows','govcon-pulse':'ai-workflows','ai-pilot':'ai-workflows',
 'workshops':'training','webinar-production':'training','podcast-production':'training','content-collaboration':'training',
 'micro-purchase':'government-subcontracting','signage':'government-subcontracting','govcon-readiness':'government-subcontracting','nationwide':'government-subcontracting'
 };
 const value=aliases[requested]||requested;
 if(value&&Array.from(field.options).some(o=>o.value===value)){
 field.value=value;
 const text=document.getElementById('message');
 if(text)text.placeholder='Tell us your goal, team size, current tools and target timeline for '+field.selectedOptions[0].textContent+'. Do not include passwords, API keys or sensitive records.';
 }
});
