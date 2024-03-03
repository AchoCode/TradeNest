
//---------BACK TO TOP BUTTON------------
const backToTop = document.querySelector('#backToTopBtn');

backToTop.addEventListener('click', ()=>{
    // When the user clicks on the button, scroll to the top of the document
    window.scrollTo({
        top: 0,
        behavior: 'smooth'

    });
});

window.addEventListener('scroll', ()=>{
     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    backToTop.classList.add('showBtn');
  } else {
    backToTop.classList.remove('showBtn');
  }
});

// ----------MODAL LOGIN/SIGNUP FORM--------------------


const ModalLoginBtn = document.querySelector('#login-link');
const Modalregistertn = document.querySelector('#signup-link');

const loginForm = document.querySelector('.login');
const SignupForm = document.querySelector('.register');

const FormPopup = document.querySelector('.form-wrapper');

function Modal(){
    loginForm.classList.toggle('hide');
    SignupForm.classList.toggle('active');
    FormPopup.classList.toggle('register');

}
function HidePassword(){
    let passwordInput = document.querySelectorAll('.pwd');
    passwordInput.forEach(pwd =>{
        pwd.type = 'password';
    })
}

//----------RESPONSIVE CSS MENU--------------------

const showMenu = document.querySelector('.showMenu');
const hideMenu = document.querySelector('.hideMenu');
const navLinks = document.querySelector('.nav-links');

showMenu.addEventListener('click', ()=>{
    navLinks.style.right = '0';
})
hideMenu.addEventListener('click', ()=>{
    navLinks.style.right = '-230px';
})

//---------CONTENT 1 FADE ANIMATION-----------------

const H1 = document.querySelector('.hero .hero-text h1');
const H2 = document.querySelector('.hero .hero-text .heading');
const cryptoTab = document.querySelector('.cryptotab');
const herobtn1 = document.querySelector('.hero-btn1');
const herobtn2 = document.querySelector('.hero-btn2');


window.addEventListener('load', ()=>{
    H1.style.opacity = '1';
    setTimeout(()=>{
        H2.style.opacity = '1';
    }, 5000)
    setTimeout(()=>{
        cryptoTab.style.opacity = '1';
  }, 3000);
    setTimeout(()=>{
        herobtn1.classList.remove('slideh1');
        herobtn2.classList.remove('slideh2');
   }, 6000) ;
})

//-----------------OUR PRICES SLIDE ON SCROLL----------------------

function BeginnerPlan(){
    const BPlan = document.querySelector('#beginner-plan');
     
    let top = window.scrollY;
    let offset = BPlan.offsetTop - 250;
    let height = BPlan.offsetHeight;

    if (top >= offset && top < offset + height){
        BPlan.classList.remove('slide-beginner');
    }
    else{
        BPlan.classList.add('slide-beginner') ;
    }
}
window.addEventListener('scroll', BeginnerPlan)

function AdvancedPlan(){
    const APlan = document.querySelector('#Advanced-plan')
     
    let top = window.scrollY;
    let offset = APlan.offsetTop - 250;
    let height = APlan.offsetHeight;

    if (top >= offset && top < offset + height){
        APlan.classList.remove('slide-advanced')
    }
    else{
        APlan.classList.add('slide-advanced') 
    }
}
window.addEventListener('scroll', AdvancedPlan)

window.addEventListener('scroll',()=>{
    const SPlan = document.querySelector('#standard-plan')
        
    let top = window.scrollY;
    let offset = SPlan.offsetTop - 250;
    let height = SPlan.offsetHeight;

    if (top >= offset && top < offset + height){
        SPlan.classList.remove('fade-standard')
    }
    else{
        SPlan.classList.add('fade-standard') 
    }
})

//-----------------OUR BENEFITS SLIDE ON SCROLL----------------------

window.addEventListener('scroll',()=>{
    const benefitCol = document.querySelectorAll('.indiv-col');
    const ImgCol = document.querySelector('.img-col')

    benefitCol.forEach(col=>{
        let top = window.scrollY;
        let offset = col.offsetTop - 50;
        let height = col.offsetHeight;

        if (top >= offset && top < offset + height){
            col.classList.add('showcol')
        }
        else{
            col.classList.remove('showcol') 
        }
    })

})

//------------------FIXED NAVBAR ON SCROLL----------------------

window.addEventListener('scroll', ()=>{

let navbar = document.querySelector('nav');
let bars = document.querySelector('.fa-bars')
    if (window.scrollY > 150) {
        navbar.classList.add('nav-fixed');
        bars.style.top = '-11px'
    } else{
        navbar.classList.remove('nav-fixed');
        bars.style.top = '-16px'
    }
})

//-----------------------ABOUT US WRITE UP FADE------------------------------------

const AUwriteup = document.querySelector('.info .write-up');
function WriteUp(){
    setInterval(()=>{
        AUwriteup.classList.toggle('show');
    }, 4000)
}

window.addEventListener('load', WriteUp)

window.addEventListener('scroll',()=>{
    const AUcontent2 = document.querySelector('.about-us .content2')
        
    let top = window.scrollY;
    let offset = AUcontent2.offsetTop - 500;
    let height = AUcontent2.offsetHeight;

    if (top >= offset && top < offset + height){
        AUcontent2.classList.add('slide')
    }
});

//------------------HERO CONTENT CHANGE----------------------

const content1 = document.querySelector('.content-1')
const content2 = document.querySelector('.content-2')
function FadeContent(){
    content1.classList.toggle('fade-content-1')
    content2.classList.toggle('fade-content-2')

}

window.addEventListener('load', setTimeout(()=>{
  setInterval(FadeContent, 6000), 17000})
)
