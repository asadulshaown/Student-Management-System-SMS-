
// request.html file

const pend = document.getElementById('pending')
let req = document.getElementById('requests')

console.log(typeof(pend),pend);
console.log(req.innerText)

if (pend == "pending"){
  req.innerText = 'Your Request Is Pending'
  console.log('ok');
  
}
else if(pend == "approved"){
  req.innerText = 'Your Request Is Approved'
}

  
