// ------------------------------------NAVIGATION------------------------------

const tabs = document.querySelectorAll('.tab')
function activeTab(){
    tabs.forEach(tab=>{
        tab.classList.remove('active')
    })
    this.classList.add('active')
}
tabs.forEach(tab=>{
    tab.addEventListener('click', activeTab)
})

// ------------------------dashboard tab------------------------
const dashboardTabLink = document.querySelector('#dashboard')
const dashboardTab = document.querySelector('.dashboard-box')
dashboardTabLink.addEventListener('click', ()=>{
    if (dashboardTabLink.classList.contains('active')){

        dashboardTab.classList.add('online')
        usersTab.classList.remove('online')
        commentsTab.classList.remove('online')
        postTab.classList.remove('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.remove('online')

    }
})

// ------------------------users tab------------------------
const userTabLink = document.querySelector('#users')
const usersTab = document.querySelector('.users-tab')
userTabLink.addEventListener('click', ()=>{
    if (userTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.add('online')
        commentsTab.classList.remove('online')
        postTab.classList.remove('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.remove('online')

    }
})

// ------------------------comments tab------------------------
const commentTabLink = document.querySelector('#comments')
const commentsTab = document.querySelector('.comments-tab')
commentTabLink.addEventListener('click', ()=>{
    if (commentTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.remove('online')
        commentsTab.classList.add('online')
        postTab.classList.remove('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.remove('online')

    }
})

// ------------------------post tab------------------------
const postTabLink = document.querySelector('#post')
const postTab = document.querySelector('.post-tab')
postTabLink.addEventListener('click', ()=>{
    if (postTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.remove('online')
        commentsTab.classList.remove('online')
        postTab.classList.add('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.remove('online')

    }
})

// ------------------------deposit tab------------------------
const depositTabLink = document.querySelector('#deposit')
const depositTab = document.querySelector('.deposit-tab')
depositTabLink.addEventListener('click', ()=>{
    if (depositTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.remove('online')
        commentsTab.classList.remove('online')
        postTab.classList.remove('online')
        depositTab.classList.add('online')
        withdrawalTab.classList.remove('online')

    }
})

// ------------------------withdrawal tab------------------------
const withdrawalTabLink = document.querySelector('#withdrawal')
const withdrawalTab = document.querySelector('.withdrawal-tab')
withdrawalTabLink.addEventListener('click', ()=>{
    if (withdrawalTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.remove('online')
        commentsTab.classList.remove('online')
        postTab.classList.remove('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.add('online')
    }
})
