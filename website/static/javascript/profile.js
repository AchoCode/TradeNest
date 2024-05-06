// TODO: write a javascript function that deletes notifications and transactions  after a certain period of time
let alertMsg = document.getElementById('alert-msg')
if(alertMsg){
    setTimeout(()=>{
        alertMsg.classList.remove('show')
    },2000)
}
let dates = document.querySelectorAll('.dates')
dates.forEach(date=>{
    const newdate = new Date(date.textContent)
    let options ={
        year: '2-digit', 
        month: 'short', 
        day: 'numeric', 
        hour: 'numeric', 
        minute: 'numeric', 
        // second: 'numeric', 
    }

    let formattedDate = newdate.toLocaleDateString('en-US', options)
    date.textContent = formattedDate
})
//------------------PROFILE NAVIGAITON CHANGE----------------------

const list = document.querySelectorAll('.list');
function activeLink(){
    list.forEach((item)=>{
        item.classList.remove('active')});
        this.classList.add('active');
}
list.forEach((item)=>{
    item.addEventListener('click', activeLink);
})


const dashBtn = document.querySelectorAll('.dash-link');
function liveBtn(){
    dashBtn.forEach((btn)=>{
        btn.classList.remove('live')});
        this.classList.add('live');
}
dashBtn.forEach((btn)=>{
    btn.addEventListener('click', liveBtn);
})


// -------------------------Deposit overlay---------------------------

let amountInput = document.querySelector('#deposit-amount')
function proceedDeposit(){
    const Wrapper = document.querySelector('.wrapper');
    const depositForm = document.querySelector('.deposit-details .withdraw-form-wrapper')

    if (amountInput.value ===''){
        event.preventDefault()
    }else{
        Wrapper.classList.add('active')
        depositForm.classList.add('inactive')
    }

}
function copyText(usrId) {
    fetch('/deposit',{
        method: 'POST',
        body: JSON.stringify({usrId: usrId,
                              Amount: amountInput.value})
    })
    .then(response => {
        if(!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Parse the JSON response
        return response.json();
    })
    var copyText = document.getElementById("deposit-address")
    let alert = document.querySelector('.copy-alert')
    navigator.clipboard.writeText(copyText.innerHTML).then(function() {
      alert.classList.add('copied');
      setTimeout(()=>{
        alert.classList.remove('copied');
    },2000)
    }).catch(function(err) {
      console.error('Unable to copy text', err);
    });
}
  
function Active(){
    const PwdInput = document.querySelector('.password-input');
    const detailBox = document.querySelector('.pwd-wrapper .details');
    const spinner = document.querySelector('.spinner-border')
    Overlay.classList.add('Blurred')
    spinner.style.display = 'block'
    
    setTimeout(()=>{
        PwdInput.classList.add('active')
        spinner.style.display = 'none';

    }, 900)
}
const Overlay = document.querySelector('.Overlay')
const popUp = document.querySelector('.pop-up');
function PopUpAlert(){

    popUp.classList.add('alert')
    Overlay.classList.add('Blurred')
}

function CloseAlert(){
    popUp.classList.remove('alert')
    Overlay.classList.remove('Blurred')

}

let withdrawalInput = document.getElementById('w-amount')
withdrawalInput.addEventListener('blur', ()=>{
    let inputValue = withdrawalInput.value
    if(inputValue.includes('.')){
        withdrawalInput.style.border = '2px solid red'
        document.getElementById('w-btn').disabled = true
        document.getElementById('w-label').style.color = 'red'
        document.getElementById('float').style.display = 'block'
        document.getElementById('w-address').disabled = true
    }else{
        withdrawalInput.style.border = ''
        document.getElementById('w-btn').disabled = false
        document.getElementById('w-label').style.color = ''
        document.getElementById('float').style.display = 'none'
        document.getElementById('w-address').disabled = false

    }
})

function pinActive(){
    document.getElementById('pin-form').classList.toggle('active')
    document.getElementById('pwd-form').classList.remove('active')

}
function pwdActive(){
    document.getElementById('pwd-form').classList.toggle('active')
    document.getElementById('pin-form').classList.remove('active')
}

function verifyEmail(usrEmail){
    fetch('/verify-email', {
        method: 'POST',
        body: JSON.stringify({usrEmail:usrEmail})
    }).then(response =>{
            if(!response.ok){
                throw new Error('Network response was not ok');
            }
            // Parse the JSON response
            return response.json();
    })
    document.querySelector('.email-msg').classList.add('active')
    setTimeout(()=>{
        document.querySelector('.email-msg').classList.remove('active')
    },2500)
}