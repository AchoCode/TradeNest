// TODO: write a javascript function that deletes notifications and transactions  after a certain period of time


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

const depositSection = document.querySelectorAll('.deposit-details');
const Wrapper = document.querySelector('.wrapper');
const depositForm = document.querySelector('.deposit-details .withdraw-form-wrapper')

function copyText() {
    // fetch('/deposit',{
    //     method: 'POST',
    //     body: JSON.stringify({usrId: usrId})
    // })
    // console.log(usrId)
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
  
function user(usrId){
    fetch('/deposit',{
        method: 'POST',
        body: JSON.stringify({usrId: usrId})
    })    
    .then(response => {
        if(!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Parse the JSON response
        return response.json();
    })
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

const popUp = document.querySelector('.pop-up');
function PopUpAlert(){

    popUp.classList.add('alert')
    Overlay.classList.add('Blurred')
}

function CloseAlert(){
    popUp.classList.remove('alert')
    Overlay.classList.remove('Blurred')

}
// function deposit() {
//     let depositAmount = document.querySelector('#deposit-amount')
//     if(depositAmount.value === ""){

//     }else{
//         event.preventDefault()
//         Wrapper.classList.add('active');
//         depositForm.classList.add('inactive')
//     }
// }

